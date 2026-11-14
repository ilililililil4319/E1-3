"""실행 흐름 (요구사항 10)

모드 1 사용자 입력(3×3): 필터 A, B 입력 → 저장 확인 → 패턴 입력 → MAC 연산 → 판정 → 성능 분석(3×3)
모드 2 data.json 분석 : 필터 로드 → 패턴 로드/검증 → MAC/판정/PASS-FAIL → 성능 분석 → 결과 요약
보너스 1 성능 비교   : 같은 입력·같은 반복 횟수로 2차원 MAC vs 1차원 MAC
보너스 2 패턴 생성기 : N 입력 → N×N Cross/X 생성 → 판정 확인 → 성능 분석에 재활용
"""

from . import console, dataset, generator, perf
from .judge import EPSILON, judge
from .labels import CROSS, UNDECIDED, X
from .mac import mac
from .matrix import Matrix
from .report import Summary

# 성능 분석에 쓰는 크기 (3×3은 data.json에 없으므로 패턴 생성기로 만든다)
PERF_SIZES = (3, 5, 13, 25)
BONUS_SIZES = (3, 5, 13, 25, 51, 101)


# =========================================================== 모드 1
def run_user_mode(reader=None):
    reader = reader or console.ask

    console.header("[1] 필터 입력")
    filter_a = Matrix.from_rows(console.read_matrix_rows("필터 A", 3, reader))
    print()
    filter_b = Matrix.from_rows(console.read_matrix_rows("필터 B", 3, reader))
    print()
    print("✓ 필터 A, B 저장 완료")
    print("필터 A:\n" + filter_a.pretty())
    print("필터 B:\n" + filter_b.pretty())
    print()

    console.header("[2] 패턴 입력")
    pattern = Matrix.from_rows(console.read_matrix_rows("패턴", 3, reader))
    print()

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    avg_ms = perf.measure_ms(mac, (pattern, filter_a))
    result = judge(score_a, score_b, "A", "B", "판정 불가")

    title = "[3] MAC 결과" + (" (판정 불가)" if result == "판정 불가" else "")
    console.header(title)
    print("A 점수: {!r}".format(score_a))
    print("B 점수: {!r}".format(score_b))
    print("연산 시간(평균/{}회): {:.4f} ms".format(perf.repeat_count(), avg_ms))
    if result == "판정 불가":
        print("판정: 판정 불가 (|A-B| < {:g})".format(EPSILON))
    else:
        print("판정: {}".format(result))
    print()

    console.header("[4] 성능 분석 (3×3, 평균/{}회)".format(perf.repeat_count()))
    print(perf.format_table(perf.measure_sizes([(3, pattern, filter_a)])))
    print()


# =========================================================== 모드 2
def run_json_mode(path):
    console.header("[1] 필터 로드")
    try:
        data = dataset.load_json(path)
    except dataset.DataError as error:
        print("✗ data.json을 읽을 수 없습니다: {}".format(error))
        print("  → 파일 위치와 형식을 확인하세요. (메뉴로 돌아갑니다)")
        return None
    filters, messages = dataset.parse_filters(data["filters"])
    for ok, text in messages:
        print(("✓ " if ok else "✗ ") + text)
    print()

    console.header("[2] 패턴 분석 (라벨 정규화 적용)")
    summary = Summary()
    for key, item in dataset.iter_cases(data["patterns"]):
        print("--- {} ---".format(key))
        try:
            n, pattern, expected = dataset.prepare_case(key, item, filters)
        except ValueError as error:
            print("FAIL ({})".format(error))
            summary.add_fail(key, str(error))
            print()
            continue

        score_cross = mac(pattern, filters[n][CROSS])
        score_x = mac(pattern, filters[n][X])
        result = judge(score_cross, score_x, CROSS, X, UNDECIDED)
        print("Cross 점수: {!r}".format(score_cross))
        print("X 점수: {!r}".format(score_x))

        if result == expected:
            print("판정: {} | expected: {} | PASS".format(result, expected))
            summary.add_pass()
        elif result == UNDECIDED:
            gap = abs(score_cross - score_x)
            print("판정: {} | expected: {} | FAIL (동점 규칙: |차이| {:.1e} < {:g})".format(
                result, expected, gap, EPSILON))
            summary.add_fail(key, "동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = {:.1e})".format(gap))
        else:
            print("판정: {} | expected: {} | FAIL (판정 불일치)".format(result, expected))
            summary.add_fail(key, "판정 불일치: 판정 {}, expected {}".format(result, expected))
        print()

    console.header("[3] 성능 분석 (평균/{}회)".format(perf.repeat_count()))
    pairs = []
    for n in PERF_SIZES:
        if n in filters:
            pair = filters[n]                     # data.json의 필터
        else:
            pair = generator.make_pair(n)         # 3×3 등 data.json에 없는 크기는 생성기로
        pairs.append((n, generator.make_cross(n), pair[CROSS]))
    print(perf.format_table(perf.measure_sizes(pairs)))
    print()

    console.header("[4] 결과 요약")
    for line in summary.lines():
        print(line)
    print("(상세 원인 분석과 복잡도 설명은 README.md의 \"결과 리포트\" 장에 있습니다)")
    print()
    return summary


# =========================================================== 보너스 1
COMPARE_REPEAT = 100   # 차이가 작아서 10회로는 측정 흔들림이 더 크다 → 두 방식 모두 100회로 같게


def run_compare_mode():
    console.header("[보너스 1] 2차원 vs 1차원 MAC (같은 입력, 같은 반복 {}회)".format(COMPARE_REPEAT))
    pairs = [(n, generator.make_cross(n), generator.make_cross(n)) for n in BONUS_SIZES]
    print(perf.format_compare_table(perf.compare_2d_1d(pairs, COMPARE_REPEAT)))
    print("※ 1차원/2차원이 100%보다 작으면 1차원이 더 빠르다는 뜻입니다.")
    print()


# =========================================================== 보너스 2
def run_generator_mode(reader=None):
    reader = reader or console.ask
    console.header("[보너스 2] 패턴 생성기")
    while True:
        raw = reader("크기 N (3 이상 정수): ").strip()
        try:
            n = int(raw)
            if n < 3:
                raise ValueError
            break
        except ValueError:
            print("  ⚠ 3 이상의 정수를 입력하세요.")
    pair = generator.make_pair(n)
    if n <= 13:
        print("Cross {0}×{0}:\n{1}".format(n, pair[CROSS].pretty()))
        print("X {0}×{0}:\n{1}".format(n, pair[X].pretty()))
    else:
        print("(N이 13보다 커서 그림은 생략합니다)")
    print()
    print("생성 패턴을 생성 필터로 판정:")
    for name in (CROSS, X):
        pattern = pair[name]
        sc, sx = mac(pattern, pair[CROSS]), mac(pattern, pair[X])
        result = judge(sc, sx, CROSS, X, UNDECIDED)
        mark = "PASS" if result == name else "FAIL"
        print("- {} 패턴 → Cross 점수 {!r}, X 점수 {!r} → {} | {}".format(name, sc, sx, result, mark))
    print()
    console.header("성능 분석 ({0}×{0}, 평균/{1}회)".format(n, perf.repeat_count()))
    print(perf.format_table(perf.measure_sizes([(n, pair[CROSS], pair[CROSS])])))
    print()



