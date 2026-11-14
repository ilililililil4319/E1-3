#!/usr/bin/env bash
# 08. 판정과 PASS/FAIL: Cross 점수, X 점수, 판정(Cross/X/UNDECIDED), expected 비교
source "$(dirname "$0")/lib.sh"
start_log "08. 판정과 PASS/FAIL 출력"

section "케이스별 점수와 판정"
run "printf '2\n0\n' | $PY main.py | sed -n '/\[2\] 패턴 분석/,/\[3\]/p'"

section "PASS / FAIL 개수"
run "printf '2\n0\n' | $PY main.py | grep -oE '\| (PASS|FAIL)' | sort | uniq -c"
check "PASS 3개" "[ \$(printf '2\n0\n' | $PY main.py | grep -c '| PASS') -eq 3 ]"
check "FAIL 3개 (모두 동점 규칙)" "[ \$(printf '2\n0\n' | $PY main.py | grep -c 'FAIL (동점 규칙') -eq 3 ]"
finish
