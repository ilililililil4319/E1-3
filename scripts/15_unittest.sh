#!/usr/bin/env bash
# 15. 단위 테스트 전체 (표준 라이브러리 unittest)
source "$(dirname "$0")/lib.sh"
start_log "15. 단위 테스트"
run "$PY -m unittest -v 2>&1"
finish
