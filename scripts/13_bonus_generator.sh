#!/usr/bin/env bash
# 13. 보너스 2: 패턴 생성기 (N 입력 → N×N Cross, X 자동 생성 → 판정·성능 분석에 재활용)
source "$(dirname "$0")/lib.sh"
start_log "13. 보너스 2: 패턴 생성기"

section "N=5: 그림, 판정, 성능"
play '4\n5\n0\n'
section "N=2(너무 작음), abc → 안내 후 다시 입력 → N=7"
play '4\n2\nabc\n7\n0\n'
section "N=51: 큰 패턴도 생성 (그림 생략)"
run "printf '4\n51\n0\n' | $PY main.py | sed -n '/생성 패턴을/,/^51×51/p'"
section "재활용: 모드 2 성능 표의 3×3은 생성기가 만든 패턴"
run "grep -n 'generator.make' app/modes.py"
check "N=25 Cross 패턴 → Cross PASS" "printf '4\n25\n0\n' | $PY main.py | grep -q 'Cross 패턴 → .* Cross | PASS'"
check "N=25 X 패턴 → X PASS" "printf '4\n25\n0\n' | $PY main.py | grep -q 'X 패턴 → .* X | PASS'"
finish
