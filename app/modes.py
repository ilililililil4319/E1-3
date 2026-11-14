"""실행 흐름 (요구사항 10)

모드 1 사용자 입력(3×3): 필터 A, B 입력 → 저장 확인 → 패턴 입력 → MAC 연산 → 판정
"""

from . import console
from .judge import EPSILON, judge
from .mac import mac
from .matrix import Matrix


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
