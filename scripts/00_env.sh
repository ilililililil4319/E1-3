#!/usr/bin/env bash
# 00. 실행 환경 기록: 어떤 OS·Python·Git에서 실행했는지 남긴다.
source "$(dirname "$0")/lib.sh"
start_log "00. 실행 환경"

section "운영체제"
run "uname -srm"
try "grep PRETTY_NAME /etc/os-release"

section "Python (요구: 3.8 이상, 외부 라이브러리 없음)"
run "$PY --version"
run "which $PY"
check "Python 3.8 이상" "$PY -c 'import sys; assert sys.version_info >= (3, 8)'"

section "외부 라이브러리를 쓰지 않는지 (import 목록)"
note "코드에 있는 import 줄을 모두 모았다. json, os, sys, time, math, re, unicodedata 는 모두 Python에 기본으로 들어 있는 표준 라이브러리다."
run "grep -rhoE '^(import|from) [a-z_.]+' main.py app/ | sort | uniq -c"
check "numpy, pandas 를 import 하지 않는다" "! grep -rqE '^(import|from) (numpy|pandas)' main.py app/"

section "Git"
run "git --version"
run "git config user.name"
run "git config user.email"

section "작업 위치와 원격 저장소"
run "pwd"
run "git remote -v"
run "git status -sb | head -1"
finish
