#!/usr/bin/env bash
# 14. 대량 데이터 성능: 케이스 1천/1만/10만 개, 크기 N 25→200 (O(N²) 확인)
source "$(dirname "$0")/lib.sh"
start_log "14. 대량 데이터 성능 측정"
reset_demo

note "scripts/bench_scale.py 가 .demo/ 에 큰 data.json 을 만들어 재고 지운다. 10만 개는 몇 초 걸린다."
run "$PY scripts/bench_scale.py .demo"
check "측정 파일 정리됨" "[ -z \"\$(ls .demo)\" ]"
finish
