#!/usr/bin/env bash
# 16. Git 이력: 기능 단위 커밋, 브랜치와 병합
source "$(dirname "$0")/lib.sh"
start_log "16. Git 이력 (커밋 단위, 브랜치 병합)"
run "git log --oneline --graph --all | head -n 40"
run "git branch -a"
run "git log --merges --oneline"
run "git log --format='%h %an %s' | head -n 30"
check "병합 커밋이 2개 이상" "[ \$(git log --merges --oneline | wc -l) -ge 2 ]"
finish
