"""성능 분석: 크기별 MAC 연산 시간(ms)을 반복 측정해 평균을 낸다.

요구사항 8
- 각 크기별로 MAC 연산을 10회 반복 측정 후 평균 시간을 출력한다.
- 입력·출력·파일 읽기 시간은 빼고 "연산 함수 호출 구간"만 잰다.
- 표: 크기(N×N) / 평균 시간(ms) / 연산 횟수(N²)
"""

import os
import time

from .console import pad
from .mac import mac, mac_flat

DEFAULT_REPEAT = 10


def repeat_count():
    """반복 횟수. 기본 10회 (환경 변수 NPU_REPEAT로 바꿀 수 있음, 최소 10)"""
    try:
        value = int(os.environ.get("NPU_REPEAT", DEFAULT_REPEAT))
    except ValueError:
        value = DEFAULT_REPEAT
    return max(DEFAULT_REPEAT, value)


def measure_ms(func, args, repeat=None):
    """func(*args)를 repeat번 호출해 1회 평균 시간(ms)을 돌려준다.

    time.perf_counter(): 짧은 구간을 재는 데 쓰는 가장 정밀한 표준 시계.
    준비 작업(패턴 만들기, 출력)은 시계 바깥에 둔다.
    """
    repeat = repeat or repeat_count()
    func(*args)  # 워밍업 1회 (첫 호출의 준비 비용이 평균에 섞이지 않게) - 측정 제외
    total = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        func(*args)
        total += time.perf_counter() - start
    return total / repeat * 1000.0


def measure_sizes(pairs, repeat=None):
    """pairs: [(n, pattern, filter), ...] → [(n, 평균 ms, N²), ...]"""
    rows = []
    for n, pattern, filt in pairs:
        rows.append((n, measure_ms(mac, (pattern, filt), repeat), n * n))
    return rows


def compare_2d_1d(pairs, repeat=None):
    """보너스 1: 같은 입력·같은 반복 횟수로 2차원 MAC과 1차원 MAC을 비교한다."""
    rows = []
    for n, pattern, filt in pairs:
        t2 = measure_ms(mac, (pattern, filt), repeat)
        pf, ff = pattern.to_flat(), filt.to_flat()   # 변환은 측정 바깥에서 한 번만
        t1 = measure_ms(mac_flat, (pf, ff), repeat)
        rows.append((n, t2, t1))
    return rows


def format_table(rows):
    lines = [
        pad("크기", 10) + pad("평균 시간(ms)", 16, "right") + pad("연산 횟수(N²)", 16, "right"),
        "-" * 42,
    ]
    for n, ms, ops in rows:
        lines.append(
            pad("{0}×{0}".format(n), 10) + pad("{:.4f}".format(ms), 16, "right") + pad(str(ops), 16, "right")
        )
    return "\n".join(lines)


def format_compare_table(rows):
    lines = [
        pad("크기", 10) + pad("2차원(ms)", 12, "right") + pad("1차원(ms)", 12, "right")
        + pad("1차원/2차원", 14, "right"),
        "-" * 48,
    ]
    for n, t2, t1 in rows:
        ratio = t1 / t2 if t2 > 0 else 0.0
        lines.append(
            pad("{0}×{0}".format(n), 10) + pad("{:.4f}".format(t2), 12, "right")
            + pad("{:.4f}".format(t1), 12, "right") + pad("{:.0%}".format(ratio), 14, "right")
        )
    return "\n".join(lines)
