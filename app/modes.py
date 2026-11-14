"""실행 흐름 (요구사항 10)

모드 1 사용자 입력(3×3): 필터 A, B 입력 → 저장 확인 → 패턴 입력 → MAC 연산 → 판정
모드 2 data.json 분석 : 필터 로드 → 패턴 로드/검증 → MAC/판정/PASS-FAIL → 결과 요약
"""

from . import console, dataset
from .judge import EPSILON, judge
from .labels import CROSS, UNDECIDED, X
from .mac import mac
from .matrix import Matrix
from .report import Summary


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
    result = judge(score_a, score_b, "A", "B", "판정 불가")

    title = "[3] MAC 결과" + (" (판정 불가)" if result == "판정 불가" else "")
    console.header(title)
    print("A 점수: {!r}".format(score_a))
    print("B 점수: {!r}".format(score_b))
    if result == "판정 불가":
        print("판정: 판정 불가 (|A-B| < {:g})".format(EPSILON))
    else:
        print("판정: {}".format(result))
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

    console.header("[3] 결과 요약")
    for line in summary.lines():
        print(line)
    print("(상세 원인 분석과 복잡도 설명은 README.md의 \"결과 리포트\" 장에 있습니다)")
    print()
    return summary
