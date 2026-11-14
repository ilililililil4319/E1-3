#!/usr/bin/env bash
# 07. 점수 비교 정책: |A-B| < 1e-9 이면 동점. 부동소수점 오차 확인
source "$(dirname "$0")/lib.sh"
start_log "07. 부동소수점 오차와 epsilon 비교"

section "부동소수점 오차: 0.1 + 0.2 는 0.3 이 아니다"
run "$PY -c 'print(0.1 + 0.2); print(0.1 + 0.2 == 0.3); print(abs((0.1 + 0.2) - 0.3) < 1e-9)'"
run "$PY -c 'print(sum([0.1] * 9)); print(sum([0.1] * 9) == 0.9)'"

section "data.json 점수를 == 비교 vs epsilon 비교"
note "== 와 > 로 비교하면 1e-16 수준의 오차가 승패를 정한다. epsilon 비교는 '사실상 같다'고 보고 UNDECIDED 로 둔다."
run "$PY -c 'import json
from app.mac import mac
from app.judge import judge
d = json.load(open(\"data.json\", encoding=\"utf-8\"))
print(\"케이스      Cross점수            X점수                ==비교   epsilon비교\")
for k, v in d[\"patterns\"].items():
    n = int(k.split(\"_\")[1]); f = d[\"filters\"][\"size_%d\" % n]
    a, b = mac(v[\"input\"], f[\"cross\"]), mac(v[\"input\"], f[\"x\"])
    naive = \"Cross\" if a > b else (\"X\" if b > a else \"UNDECIDED\")
    print(\"{:<11} {:<20} {:<20} {:<8} {}\".format(k, repr(a), repr(b), naive, judge(a, b, \"Cross\", \"X\", \"UNDECIDED\")))'"

section "모드 1에서 판정 불가: A=0.1 아홉 칸, B=가운데 0.9, 패턴=모두 1"
play '1\n0.1 0.1 0.1\n0.1 0.1 0.1\n0.1 0.1 0.1\n0 0 0\n0 0.9 0\n0 0 0\n1 1 1\n1 1 1\n1 1 1\n0\n'
check "판정 불가 출력" "printf '1\n0.1 0.1 0.1\n0.1 0.1 0.1\n0.1 0.1 0.1\n0 0 0\n0 0.9 0\n0 0 0\n1 1 1\n1 1 1\n1 1 1\n0\n' | $PY main.py | grep -q '판정: 판정 불가 (|A-B| < 1e-09)'"
check "비교 단위 테스트 통과" "$PY -m unittest tests.test_core.JudgeTest"
finish
