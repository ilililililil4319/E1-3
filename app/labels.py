"""라벨 정규화(표준화): 여러 모양의 이름을 표준 라벨 2개(Cross, X)로 통일한다.

요구사항 4
- expected 값: '+' → Cross, 'x' → X
- filter 키 : 'cross' → Cross, 'x' → X
콘솔 출력과 PASS/FAIL 비교는 항상 표준 라벨로 한다.
"""

CROSS = "Cross"
X = "X"
UNDECIDED = "UNDECIDED"
STANDARD_LABELS = (CROSS, X)

# 앞뒤 공백을 지우고 소문자로 바꾼 뒤 이 표에서 찾는다. ("Cross", "CROSS", " x " 모두 처리)
_ALIASES = {
    "+": CROSS,
    "cross": CROSS,
    "x": X,
}


def normalize_label(raw):
    """'+' / 'cross' / 'x' (대소문자·공백 무관) → 'Cross' / 'X'.

    해석할 수 없으면 ValueError. (호출한 쪽에서 해당 케이스를 FAIL로 처리한다)
    """
    if not isinstance(raw, str):
        raise ValueError("라벨이 문자열이 아닙니다: {!r}".format(raw))
    key = raw.strip().lower()
    if key not in _ALIASES:
        raise ValueError("알 수 없는 라벨: {!r} (허용: '+', 'cross', 'x')".format(raw))
    return _ALIASES[key]
