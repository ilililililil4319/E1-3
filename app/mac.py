"""MAC(Multiply-Accumulate) 연산: 같은 위치끼리 곱하고(Multiply) 모두 더한다(Accumulate).

요구사항 5: NumPy 등 외부 라이브러리 없이 반복문으로 직접 구현한다.
"""

from .matrix import Matrix


def mac(pattern, filt):
    """2차원 MAC: 이중 for문으로 N×N번 곱하고 더한다. 결과는 float 점수.

    pattern, filt: Matrix 또는 2차원 리스트
    """
    p = pattern.rows() if isinstance(pattern, Matrix) else pattern
    f = filt.rows() if isinstance(filt, Matrix) else filt
    n = len(p)
    if n != len(f):
        raise ValueError("크기 불일치: 패턴 {0}×{0}, 필터 {1}×{1}".format(n, len(f)))

    total = 0.0
    for r in range(n):          # 행(가로줄)을 하나씩
        p_row = p[r]
        f_row = f[r]
        for c in range(n):      # 그 행의 칸을 하나씩
            total += p_row[c] * f_row[c]   # 곱해서(M) 누적(A)
    return total


def mac_flat(pattern_flat, filter_flat):
    """보너스 1: 1차원(길이 N²) MAC. for문 1개로 N²번 곱하고 더한다."""
    length = len(pattern_flat)
    if length != len(filter_flat):
        raise ValueError("길이 불일치: {} vs {}".format(length, len(filter_flat)))
    total = 0.0
    for i in range(length):
        total += pattern_flat[i] * filter_flat[i]
    return total
