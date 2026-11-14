"""대량 데이터 성능 측정 (scripts/14_scale.sh 에서 호출)

1) 케이스 수 늘리기: 5×5 패턴 1,000 / 10,000 / 100,000개를 담은 data.json을 만들어
   불러오기(json) / 검증 / MAC+판정 각각의 시간을 잰다. → 케이스 수에 비례(O(케이스 수))하는지 확인
2) 크기 늘리기: N = 25, 50, 100, 200 에서 MAC 1회 시간 → N이 2배면 시간이 약 4배(O(N²))인지 확인

사용: python3 scripts/bench_scale.py [저장 폴더]   (기본 .demo)
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import dataset, generator, perf  # noqa: E402
from app.judge import judge  # noqa: E402
from app.mac import mac  # noqa: E402


def build_file(path, count, n=5):
    cross, x = generator.make_cross(n).rows(), generator.make_x(n).rows()
    patterns = {}
    for i in range(count):
        is_cross = i % 2 == 0
        patterns["size_{}_{}".format(n, i + 1)] = {
            "input": cross if is_cross else x,
            "expected": "+" if is_cross else "x",
        }
    data = {"filters": {"size_{}".format(n): {"cross": cross, "x": x}}, "patterns": patterns}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return os.path.getsize(path)


def run_cases(path):
    t0 = time.perf_counter()
    data = dataset.load_json(path)
    t1 = time.perf_counter()
    filters, _ = dataset.parse_filters(data["filters"])
    cases = [dataset.prepare_case(k, v, filters) for k, v in dataset.iter_cases(data["patterns"])]
    t2 = time.perf_counter()
    passed = 0
    for n, pattern, expected in cases:
        result = judge(mac(pattern, filters[n]["Cross"]), mac(pattern, filters[n]["X"]), "Cross", "X", "UNDECIDED")
        passed += result == expected
    t3 = time.perf_counter()
    return (t1 - t0) * 1000, (t2 - t1) * 1000, (t3 - t2) * 1000, passed, len(cases)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else ".demo"
    os.makedirs(out_dir, exist_ok=True)

    print("[1] 케이스 수 늘리기 (5×5 패턴)")
    print("| 케이스 수 | 파일 크기 | 불러오기(ms) | 검증(ms) | MAC+판정(ms) | 통과 |")
    print("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for count in (1000, 10000, 100000):
        path = os.path.join(out_dir, "scale_{}.json".format(count))
        size = build_file(path, count)
        load_ms, check_ms, mac_ms, passed, total = run_cases(path)
        print("| {:,} | {:.1f} MB | {:.1f} | {:.1f} | {:.1f} | {:,}/{:,} |".format(
            count, size / 1e6, load_ms, check_ms, mac_ms, passed, total))
        os.remove(path)

    print()
    print("[2] 크기 늘리기 (MAC 1회, 평균/{}회)".format(perf.repeat_count()))
    print("| N | 연산 횟수 N² | 평균(ms) | 앞 줄 대비 시간 배수 |")
    print("| ---: | ---: | ---: | ---: |")
    before = None
    for n in (25, 50, 100, 200):
        m = generator.make_cross(n)
        ms = perf.measure_ms(mac, (m, m))
        ratio = "-" if before is None else "×{:.1f}".format(ms / before)
        print("| {} | {:,} | {:.3f} | {} |".format(n, n * n, ms, ratio))
        before = ms


if __name__ == "__main__":
    main()
