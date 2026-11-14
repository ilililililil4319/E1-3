#!/usr/bin/env bash
# 09. 성능 분석: 크기별 MAC 시간(ms)을 10회 반복 측정한 평균, 연산 횟수 N²
source "$(dirname "$0")/lib.sh"
start_log "09. 성능 분석 (크기별 평균 시간)"

section "측정 코드: 연산 함수 호출 구간만 잰다 (app/perf.py)"
run "sed -n '/^def measure_ms/,/return total/p' app/perf.py"

section "모드 2 성능 표 (3×3은 생성기, 5/13/25는 data.json 필터)"
run "printf '2\n0\n' | $PY main.py | sed -n '/\[3\] 성능 분석/,/\[4\]/p' | head -n -1"

section "같은 측정을 3번 반복 (PC 상태에 따라 값이 조금씩 흔들림)"
for i in 1 2 3; do
    run "printf '2\n0\n' | $PY main.py | grep -E '^(3×3|25×25) '"
done
check "표에 크기 4줄 (3, 5, 13, 25)" "[ \$(printf '2\n0\n' | $PY main.py | grep -cE '^(3×3|5×5|13×13|25×25) ') -eq 4 ]"
check "연산 횟수 N² = 9, 25, 169, 625" "printf '2\n0\n' | $PY main.py | grep -E '^25×25 ' | grep -q ' 625\$'"
finish
