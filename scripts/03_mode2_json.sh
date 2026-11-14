#!/usr/bin/env bash
# 03. 모드 2: data.json 로드 → 키에서 N 추출 → size_N 필터 선택 → 크기 검증 → 판정
source "$(dirname "$0")/lib.sh"
start_log "03. 모드 2: data.json 분석"

section "data.json 구조 살펴보기 (키 목록과 크기)"
run "$PY -c 'import json
d = json.load(open(\"data.json\", encoding=\"utf-8\"))
print(\"최상위 키:\", list(d))
for k, v in d[\"filters\"].items():
    print(\"filters.{}: {} → 각 {}×{}\".format(k, list(v), len(v[\"cross\"]), len(v[\"cross\"][0])))
for k, v in d[\"patterns\"].items():
    print(\"patterns.{}: input {}×{}, expected {!r}\".format(k, len(v[\"input\"]), len(v[\"input\"][0]), v[\"expected\"]))'"

section "키에서 N 추출: size_13_2 → 13 → size_13 필터"
run "$PY -c 'import re
for key in (\"size_5_1\", \"size_13_2\", \"size_25_1\"):
    n = int(re.match(r\"^size_(\\d+)_(\\d+)\$\", key).group(1))
    print(key, \"→ N =\", n, \"→ filters[size_{}]\".format(n))'"

section "모드 2 실행"
play '2\n0\n'
check "필터 3종 로드 완료" "[ \$(printf '2\n0\n' | $PY main.py | grep -c '필터 로드 완료') -eq 3 ]"
check "패턴 6개 모두 점수 계산" "[ \$(printf '2\n0\n' | $PY main.py | grep -c '^Cross 점수') -eq 6 ]"
finish
