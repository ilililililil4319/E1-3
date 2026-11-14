"""04_schema_errors.sh 실습용: 진짜 data.json을 복사해 일부러 망가뜨린 파일들을 .demo/ 에 만든다.

사용: python3 scripts/make_broken.py .demo
만드는 파일
- broken_cases.json : 정상 케이스 6개 + 망가진 케이스 5개 (케이스 단위 FAIL 확인)
- broken_filter.json: size_13 필터의 x를 12×12로 잘라 둠 (필터 로드 실패 → size_13 패턴 FAIL)
- broken_syntax.json: 쉼표가 빠진 JSON (파일 단위 오류 → 메뉴로 복귀)
"""

import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else ".demo"
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(ROOT, "data.json"), encoding="utf-8") as f:
        data = json.load(f)

    cases = copy.deepcopy(data)
    p = cases["patterns"]
    cross5 = p["size_5_2"]["input"]
    p["size_5_3"] = {"input": [row[:3] for row in cross5[:3]], "expected": "+"}   # 3×3인데 키는 5
    p["size_7_1"] = {"input": cross5, "expected": "+"}                             # size_7 필터 없음
    p["pattern_A"] = {"input": cross5, "expected": "+"}                            # 키 형식 오류
    p["size_5_4"] = {"input": cross5, "expected": "o"}                             # 모르는 라벨
    p["size_5_5"] = {"input": [[0, "1", 0, 0, 0]] + cross5[1:], "expected": "x"}   # 숫자 아닌 값
    _write(os.path.join(out, "broken_cases.json"), cases)

    bad_filter = copy.deepcopy(data)
    bad_filter["filters"]["size_13"]["x"] = [row[:12] for row in bad_filter["filters"]["size_13"]["x"][:12]]
    _write(os.path.join(out, "broken_filter.json"), bad_filter)

    with open(os.path.join(out, "broken_syntax.json"), "w", encoding="utf-8") as f:
        f.write('{\n  "filters": {}\n  "patterns": {}\n}\n')

    for name in sorted(os.listdir(out)):
        if name.startswith("broken_"):
            print("만듦: {}/{}".format(out, name))


def _write(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
