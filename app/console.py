"""콘솔 입출력 도우미: 질문하기, 제목 줄, 3×3 행렬 입력과 검증, 한글 폭 맞추기."""

import math
import sys
import unicodedata

LINE = "#" + "-" * 40


def ask(prompt):
    """input()과 같지만, 키보드가 아닌 파이프 입력이면 입력값을 화면에 다시 보여 준다.

    (printf '1\\n' | python3 main.py 로 실행한 로그만 봐도 무엇을 입력했는지 보이게)
    """
    value = input(prompt)
    if not sys.stdin.isatty():
        print(value)
    return value


def header(title):
    print(LINE)
    print("# " + title)
    print(LINE)


def display_width(text):
    """터미널에서 한글은 2칸, 영문·숫자는 1칸을 차지한다."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def pad(text, width, align="left"):
    gap = max(0, width - display_width(text))
    return text + " " * gap if align == "left" else " " * gap + text


FORMAT_ERROR = "입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요."


def parse_row(line, n):
    """한 줄을 숫자 n개로 바꾼다. 실패하면 ValueError(안내 문구).

    - 기본: 공백 구분 "0 1 0"
    - 편의: 0/1만으로 된 n글자 "010" 도 허용 (미션 출력 예시가 이 모양이라서)
    """
    tokens = line.split()
    if len(tokens) == 1 and len(tokens[0]) == n and n > 1 and set(tokens[0]) <= {"0", "1"}:
        tokens = list(tokens[0])
    if len(tokens) != n:
        raise ValueError(
            FORMAT_ERROR.format(n=n) + " (입력한 숫자 {}개)".format(len(tokens))
        )
    values = []
    for token in tokens:
        try:
            value = float(token)
            if not math.isfinite(value):      # 'nan', 'inf'도 float()은 통과하므로 따로 막는다
                raise ValueError
            values.append(value)
        except ValueError:
            raise ValueError(FORMAT_ERROR.format(n=n) + " ('{}'은(는) 숫자가 아님)".format(token))
    return values


def read_matrix_rows(title, n=3, reader=None):
    """n줄을 입력받아 n×n 리스트로 돌려준다. 틀린 줄은 안내 후 그 줄만 다시 입력받는다."""
    reader = reader or ask
    print("{} ({}줄 입력, 공백 구분)".format(title, n))
    rows = []
    while len(rows) < n:
        line = reader("")
        try:
            rows.append(parse_row(line, n))
        except ValueError as error:
            print("  ⚠ {}".format(error))
            print("  → {}번째 줄을 다시 입력하세요.".format(len(rows) + 1))
    return rows
