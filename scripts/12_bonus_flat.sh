#!/usr/bin/env bash
# 12. 보너스 1: 2차원 → 1차원(길이 N²) 변환 후 성능 비교 (같은 입력, 같은 반복 횟수)
source "$(dirname "$0")/lib.sh"
start_log "12. 보너스 1: 1차원 배열 최적화 비교"

section "2차원 → 1차원 변환: 위치 (r, c) → 인덱스 r×N + c"
run "$PY -c 'from app.generator import make_cross
m = make_cross(3)
print(m.pretty()); print(\"1차원:\", m.to_flat())
print(\"(1,2) → 인덱스\", 1*3+2, \"→ 값\", m.to_flat()[1*3+2], \"= get(1,2) =\", m.get(1,2))'"

section "1차원 MAC 코드 (for문 1개)"
run "sed -n '/^def mac_flat/,/return total/p' app/mac.py"

section "성능 비교 (메뉴 3), 2번 실행"
play '3\n0\n'
run "printf '3\n0\n' | $PY main.py | sed -n '/크기/,/※/p'"
check "두 방식의 점수가 같다" "$PY -m unittest tests.test_core.MacTest.test_flat_equals_2d"
finish
