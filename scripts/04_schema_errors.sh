#!/usr/bin/env bash
# 04. 스키마·크기 불일치: 일부러 망가뜨린 data.json → 그 케이스만 FAIL, 프로그램은 계속
source "$(dirname "$0")/lib.sh"
start_log "04. 모드 2: 스키마 오류와 크기 불일치"
reset_demo

section "실습용 망가진 파일 만들기 (.demo/, 진짜 data.json은 그대로)"
run "$PY scripts/make_broken.py .demo"

section "케이스 단위 오류 5종: 크기 불일치, 필터 없음, 키 형식, 라벨, 숫자 아님"
note "NPU_DATA_PATH 환경 변수로 읽을 파일을 바꾼다. 정상 6개는 그대로 판정되고 망가진 5개만 FAIL 이 된다."
run "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json $PY main.py | sed -n '/\[2\]/,/\[3\]/p'"
run "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json $PY main.py | sed -n '/\[4\] 결과 요약/,\$p'"
check "크기 불일치 → FAIL" "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json $PY main.py | grep -q 'size_5_3: 크기 불일치: 패턴 3×3, 필터 5×5'"
check "총 11개 중 실패 8개(동점 3 + 오류 5)" "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json $PY main.py | grep -q '실패: 8개'"
check "오류가 있어도 끝까지 실행 (종료 메시지)" "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json $PY main.py | grep -q '프로그램을 종료합니다'"

section "필터가 망가진 경우: size_13 x 필터가 12×12 → 필터 로드 실패 → size_13 패턴 FAIL"
run "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_filter.json $PY main.py | sed -n '/\[1\]/,/\[2\]/p'"
run "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_filter.json $PY main.py | grep -A1 -- '--- size_13'"

section "파일 단위 오류: JSON 문법 오류, 파일 없음 → 안내 후 메뉴로 돌아옴"
run "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_syntax.json $PY main.py | tail -n 12"
run "printf '2\n0\n' | NPU_DATA_PATH=.demo/없는파일.json $PY main.py | grep -A1 '✗'"
check "JSON 문법 오류 안내" "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_syntax.json $PY main.py | grep -q 'JSON 형식 오류'"
check "문법 오류 뒤에도 종료 코드 0" "printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_syntax.json $PY main.py > /dev/null"
finish
