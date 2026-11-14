"""data.json 불러오기와 스키마(구조) 검증.

요구사항 3
- filters : size_5, size_13, size_25 (각각 cross, x 필터 2개)
- patterns: size_{N}_{idx} 키, 각 항목에 input(2차원 배열)과 expected
- 패턴 키에서 N을 뽑아 size_N 필터를 고른다
- 필터와 패턴 크기가 다르면 그 케이스만 FAIL + 이유 메시지 (프로그램은 멈추지 않음)
"""

import json
import re

from .labels import normalize_label
from .matrix import Matrix

FILTER_KEY = re.compile(r"^size_(\d+)$")
PATTERN_KEY = re.compile(r"^size_(\d+)_(\d+)$")


class DataError(Exception):
    """파일 전체 문제 (파일 없음, JSON 깨짐, 최상위에 filters/patterns 없음)."""


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise DataError("파일이 없습니다: {}".format(path))
    except json.JSONDecodeError as error:
        raise DataError("JSON 형식 오류: {} (줄 {}, 칸 {})".format(error.msg, error.lineno, error.colno))
    if not isinstance(data, dict):
        raise DataError("최상위가 객체({...})가 아닙니다")
    for key in ("filters", "patterns"):
        if not isinstance(data.get(key), dict):
            raise DataError("'{}' 항목이 없거나 객체가 아닙니다".format(key))
    return data


def parse_filters(raw_filters):
    """{'size_5': {'cross': [[...]], 'x': [[...]]}} → ({5: {'Cross': Matrix, 'X': Matrix}}, messages)

    messages: [(성공 여부, 문장), ...] 콘솔에 출력할 줄
    문제가 있는 필터는 등록하지 않는다 → 그 크기의 패턴은 "필터 없음"으로 FAIL.
    """
    filters, messages = {}, []
    for key in sorted(raw_filters, key=_size_order):
        match = FILTER_KEY.match(key)
        if not match:
            messages.append((False, "{}: 키 형식 오류 (size_N 형태가 아님) → 건너뜀".format(key)))
            continue
        n = int(match.group(1))
        group = raw_filters[key]
        try:
            if not isinstance(group, dict):
                raise ValueError("cross/x 묶음(객체)이 아님")
            pair = {}
            for label_key, rows in group.items():
                label = normalize_label(label_key)        # 'cross' → Cross, 'x' → X
                matrix = Matrix.from_rows(rows)
                if matrix.size != n:
                    raise ValueError("{} 필터 크기 {}×{} ≠ 키의 N={}".format(label, matrix.size, matrix.size, n))
                pair[label] = matrix
            missing = [label for label in ("Cross", "X") if label not in pair]
            if missing:
                raise ValueError("{} 필터가 없음".format(", ".join(missing)))
        except ValueError as error:
            messages.append((False, "{} 필터 로드 실패: {}".format(key, error)))
            continue
        filters[n] = pair
        messages.append((True, "{} 필터 로드 완료 (Cross, X)".format(key)))
    return filters, messages


def iter_cases(raw_patterns):
    """패턴을 키 순서(size_5_1, size_5_2, size_13_1 ...)로 하나씩 꺼낸다."""
    for key in sorted(raw_patterns, key=_size_order):
        yield key, raw_patterns[key]


def prepare_case(key, item, filters):
    """케이스 1개 검증. (N, 패턴 Matrix, 표준 expected 라벨)을 돌려주고, 문제가 있으면 ValueError(이유)."""
    match = PATTERN_KEY.match(key)
    if not match:
        raise ValueError("키 형식 오류: size_{N}_{idx} 형태가 아님")
    n = int(match.group(1))
    if n not in filters:
        raise ValueError("필터 없음: size_{} 필터가 로드되지 않음".format(n))
    if not isinstance(item, dict) or "input" not in item or "expected" not in item:
        raise ValueError("스키마 오류: input 또는 expected 항목이 없음")
    try:
        expected = normalize_label(item["expected"])   # '+' → Cross, 'x' → X
    except ValueError as error:
        raise ValueError("라벨 오류: {}".format(error))
    try:
        pattern = Matrix.from_rows(item["input"])
    except ValueError as error:
        raise ValueError("스키마 오류: input {}".format(error))
    if pattern.size != n:
        raise ValueError(
            "크기 불일치: 패턴 {0}×{0}, 필터 {1}×{1}".format(pattern.size, n)
        )
    return n, pattern, expected


def _size_order(key):
    # 'size_13_2' → (13, 2). 글자 순서면 size_13이 size_5보다 앞에 오므로 숫자로 정렬. 이상한 키는 맨 뒤.
    numbers = re.findall(r"\d+", key)
    return (0, [int(x) for x in numbers]) if numbers else (1, [key])
