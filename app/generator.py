"""보너스 2: 패턴 생성기. 크기 N을 주면 N×N 십자가(Cross)와 X 패턴을 만든다.

- Cross: 가운데 행 전체 + 가운데 열 전체가 1
- X    : 왼쪽 위→오른쪽 아래 대각선 + 오른쪽 위→왼쪽 아래 대각선이 1
N이 짝수면 정확한 가운데가 없으므로 가운데 두 줄 중 아래/오른쪽 줄(N // 2)을 쓴다.
"""

from .matrix import Matrix


def make_cross(n):
    m = Matrix(n)
    mid = n // 2
    for i in range(n):
        m.set(mid, i, 1)   # 가운데 행
        m.set(i, mid, 1)   # 가운데 열
    return m


def make_x(n):
    m = Matrix(n)
    for i in range(n):
        m.set(i, i, 1)           # \ 대각선
        m.set(i, n - 1 - i, 1)   # / 대각선
    return m


def make_pair(n):
    """{'Cross': 십자가, 'X': X} 필터 한 쌍"""
    return {"Cross": make_cross(n), "X": make_x(n)}
