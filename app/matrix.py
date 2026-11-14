"""n×n 2차원 숫자 배열(패턴·필터)을 저장하는 Matrix 클래스.

요구사항 1 "데이터 구조":
- n×n 크기의 2차원 패턴 및 필터를 저장할 수 있어야 한다.
- 특정 위치의 값을 저장(set)하고 읽어올(get) 수 있어야 한다.
- 최소 3×3, 5×5, 13×13, 25×25 크기를 처리할 수 있어야 한다. (크기 제한 없음)
"""


import math


def _is_number(value):
    # bool은 int의 자식이라 True/False가 1/0으로 통과되는 것을 막는다.
    # NaN(숫자 아님)·Infinity(무한대)는 비교가 깨지므로 받지 않는다.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


class Matrix:
    """정사각형(n×n) 숫자 배열.

    내부에는 "줄(list) 안에 숫자(list)" 형태로 저장한다: self._rows[행][열]
    """

    def __init__(self, size, fill=0.0):
        if not isinstance(size, int) or size < 1:
            raise ValueError("크기는 1 이상의 정수여야 합니다: {!r}".format(size))
        self.size = size
        self._rows = [[float(fill)] * size for _ in range(size)]

    # ------------------------------------------------------------ 만들기
    @classmethod
    def from_rows(cls, rows):
        """[[0, 1, 0], [1, 1, 1], [0, 1, 0]] 같은 2차원 리스트로 Matrix를 만든다.

        정사각형이 아니거나 숫자가 아닌 값이 있으면 ValueError (이유를 메시지로).
        """
        if not isinstance(rows, list) or not rows:
            raise ValueError("2차원 배열(리스트 안의 리스트)이 아닙니다")
        size = len(rows)
        matrix = cls(size)
        for r, row in enumerate(rows):
            if not isinstance(row, list):
                raise ValueError("{}번째 행이 리스트가 아닙니다".format(r + 1))
            if len(row) != size:
                raise ValueError(
                    "정사각형이 아닙니다: {}행인데 {}번째 행의 열 수가 {}".format(size, r + 1, len(row))
                )
            for c, value in enumerate(row):
                if not _is_number(value):
                    raise ValueError("{}행 {}열 값이 숫자가 아닙니다: {!r}".format(r + 1, c + 1, value))
                matrix.set(r, c, value)
        return matrix

    # ------------------------------------------------------------ 읽기/쓰기
    def get(self, row, col):
        """(row, col) 위치의 값을 읽는다. 0부터 센다."""
        return self._rows[row][col]

    def set(self, row, col, value):
        """(row, col) 위치에 값을 저장한다. 0부터 센다."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError("위치 ({}, {})가 {}×{} 범위를 벗어났습니다".format(row, col, self.size, self.size))
        if not _is_number(value):
            raise ValueError("숫자만 저장할 수 있습니다: {!r}".format(value))
        self._rows[row][col] = float(value)

    def rows(self):
        """MAC 연산이 빠르게 읽을 수 있도록 내부 2차원 리스트를 돌려준다."""
        return self._rows

    # ------------------------------------------------------------ 보여 주기
    def pretty(self, indent="  "):
        lines = []
        for row in self._rows:
            lines.append(indent + " ".join(_fmt(v) for v in row))
        return "\n".join(lines)

    def __eq__(self, other):
        return isinstance(other, Matrix) and self._rows == other._rows

    def __repr__(self):
        return "Matrix({}×{})".format(self.size, self.size)


def _fmt(value):
    # 1.0 → "1", 0.5 → "0.5" 처럼 보기 좋게
    return str(int(value)) if float(value).is_integer() else repr(value)
