#!/usr/bin/env bash
# 10. 결과 리포트(콘솔): 전체/통과/실패 수 + 실패 케이스와 이유
source "$(dirname "$0")/lib.sh"
start_log "10. 결과 리포트 (콘솔 요약)"

section "결과 요약"
run "printf '2\n0\n' | $PY main.py | sed -n '/\[4\] 결과 요약/,/README/p'"
check "총 6 / 통과 3 / 실패 3" "printf '2\n0\n' | $PY main.py | grep -A2 '총 테스트: 6개' | grep -q '실패: 3개'"
check "README에 결과 리포트 장이 있다" "grep -q '결과 리포트' README.md"
finish
