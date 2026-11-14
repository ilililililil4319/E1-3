#!/usr/bin/env bash
# 11. 실행 흐름: 모드 선택 → 모드 1 → 모드 2 → 종료. 잘못된 번호, Ctrl+C, 입력 끊김 처리
source "$(dirname "$0")/lib.sh"
start_log "11. 전체 실행 흐름"

section "메뉴에 없는 번호(9), 글자(a) → 안내 후 다시 묻기"
play '9\na\n0\n'

section "단계 순서 확인: 모드 1 = 필터 입력 → 저장 확인 → 패턴 입력 → MAC 결과 → 성능 분석"
run "printf '1\n0 1 0\n1 1 1\n0 1 0\n1 0 1\n0 1 0\n1 0 1\n1 0 1\n0 1 0\n1 0 1\n0\n' | $PY main.py | grep -E '^# \[|저장 완료'"
section "단계 순서 확인: 모드 2 = 필터 로드 → 패턴 분석 → 성능 분석 → 결과 요약"
run "printf '2\n0\n' | $PY main.py | grep -E '^# \['"

section "입력이 중간에 끊김(EOF) → 오류 화면 없이 종료"
run "printf '1\n0 1 0\n' | $PY main.py | tail -n 2; echo \"종료 코드: \${PIPESTATUS[1]}\""
section "Ctrl+C (SIGINT) → 안전 종료"
run "sleep 3 | timeout --preserve-status -s INT 1 $PY main.py | tail -n 1; echo \"종료 코드: \${PIPESTATUS[1]}\""
check "Ctrl+C 후 종료 코드 0" "sleep 2 | timeout --preserve-status -s INT 1 $PY main.py"
finish
