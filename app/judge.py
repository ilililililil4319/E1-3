"""점수 비교 정책: 허용오차(epsilon) 기반으로 동점을 판단한다.

요구사항 6: abs(score_a - score_b) < 1e-9 이면 동점(UNDECIDED)으로 본다.
부동소수점은 0.1 + 0.2 == 0.30000000000000004 처럼 아주 작은 오차가 생기므로
== 로 비교하면 "사실상 같은 점수"가 다르다고 판정될 수 있다.
"""

EPSILON = 1e-9


def is_tie(score_a, score_b, epsilon=EPSILON):
    return abs(score_a - score_b) < epsilon


def judge(score_a, score_b, label_a, label_b, undecided, epsilon=EPSILON):
    """두 점수를 비교해 더 큰 쪽의 라벨을 돌려준다. 차이가 epsilon보다 작으면 undecided."""
    if is_tie(score_a, score_b, epsilon):
        return undecided
    return label_a if score_a > score_b else label_b
