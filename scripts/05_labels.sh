#!/usr/bin/env bash
# 05. 라벨 정규화: '+'/'cross' → Cross, 'x' → X. 출력과 비교는 표준 라벨로.
source "$(dirname "$0")/lib.sh"
start_log "05. 라벨 정규화 (표준화)"

section "data.json 원본에 들어 있는 라벨 모양"
note "filter 키는 소문자 cross/x, expected는 기호 '+'와 소문자 'x' 다. 같은 뜻인데 모양이 다르다."
run "grep -oE '\"(cross|x)\": \\[' data.json | sort | uniq -c"
run "grep -oE '\"expected\": \"[^\"]*\"' data.json | sort | uniq -c"

section "normalize_label: 여러 모양 → Cross / X"
run "$PY -c 'from app.labels import normalize_label
for raw in (\"+\", \"cross\", \" CROSS \", \"x\", \"X\"):
    print(repr(raw).ljust(10), \"→\", normalize_label(raw))'"
try "$PY -c 'from app.labels import normalize_label; normalize_label(\"o\")' 2>&1 | tail -1"

section "모드 2 출력: expected가 표준 라벨(Cross/X)로 표시된다"
run "printf '2\n0\n' | $PY main.py | grep 'expected:'"
check "출력에 '+' 나 소문자 x 라벨이 남지 않음" "! printf '2\n0\n' | $PY main.py | grep -E 'expected: (\+|x) '"
check "라벨 단위 테스트 통과" "$PY -m unittest tests.test_core.LabelTest"
finish
