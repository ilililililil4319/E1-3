#!/usr/bin/env bash
# 06. MAC 연산: 같은 위치끼리 곱하고 모두 더하기. 외부 라이브러리 없이 이중 for문.
source "$(dirname "$0")/lib.sh"
start_log "06. MAC 연산 (반복문 직접 구현)"

section "구현 코드 (app/mac.py 의 mac 함수)"
run "sed -n '/^def mac(/,/return total/p' app/mac.py"

section "미션 Case 1, 2: 십자가 입력 × 십자가 필터 = 5, × X 필터 = 1"
run "$PY -c 'from app.mac import mac
cross = [[0,1,0],[1,1,1],[0,1,0]]
x     = [[1,0,1],[0,1,0],[1,0,1]]
print(\"십자가 × 십자가 =\", mac(cross, cross))
print(\"십자가 × X      =\", mac(cross, x))'"

section "곱셈 과정을 한 칸씩 보기 (십자가 × X)"
run "$PY -c 'p = [[0,1,0],[1,1,1],[0,1,0]]; f = [[1,0,1],[0,1,0],[1,0,1]]
total = 0.0
for r in range(3):
    print(\"  \".join(\"{}×{}\".format(p[r][c], f[r][c]) for c in range(3)))
    for c in range(3):
        total += p[r][c] * f[r][c]
print(\"합계 =\", total)'"

section "결과는 float (소수 필터도 계산)"
run "$PY -c 'from app.mac import mac; print(mac([[1,1],[1,1]], [[0.5,0.25],[0.1,0.2]]))'"
check "numpy 없이 구현 (import 없음)" "! grep -qE 'import (numpy|pandas)' app/mac.py"
check "MAC 단위 테스트 통과" "$PY -m unittest tests.test_core.MacTest"
finish
