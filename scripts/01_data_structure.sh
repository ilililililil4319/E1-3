#!/usr/bin/env bash
# 01. 데이터 구조: n×n 2차원 배열(Matrix)에 값을 저장(set)하고 읽기(get). 3×3 ~ 25×25
source "$(dirname "$0")/lib.sh"
start_log "01. 데이터 구조 (Matrix)"

section "Matrix 만들기: 2차원 리스트 → Matrix"
note "from_rows 는 [[0,1,0],[1,1,1],[0,1,0]] 같은 '리스트 안의 리스트'를 받아 정사각형인지, 모두 숫자인지 검사하고 저장한다."
run "$PY -c 'from app.matrix import Matrix
m = Matrix.from_rows([[0,1,0],[1,1,1],[0,1,0]])
print(m, \"크기:\", m.size)
print(m.pretty())'"

section "특정 위치의 값 저장(set)과 읽기(get) - 위치는 0부터 센다"
run "$PY -c 'from app.matrix import Matrix
m = Matrix(3)
m.set(1, 2, 7)
print(\"(1,2)에 7 저장 → get(1,2) =\", m.get(1, 2))
print(m.pretty())'"

section "3×3, 5×5, 13×13, 25×25 모두 처리"
run "$PY -c 'from app.matrix import Matrix
for n in (3, 5, 13, 25):
    m = Matrix(n)
    m.set(n-1, n-1, 1)
    print(\"{0}×{0}: 칸 수 {1}, 마지막 칸 get({2},{2}) = {3}\".format(n, len(m.to_flat()), n-1, m.get(n-1, n-1)))'"

section "잘못된 데이터는 거절 (정사각형 아님, 숫자 아님, 범위 밖)"
try "$PY -c 'from app.matrix import Matrix; Matrix.from_rows([[1,2,3],[1,2]])' 2>&1 | tail -1"
try "$PY -c 'from app.matrix import Matrix; Matrix.from_rows([[1,\"a\"],[1,2]])' 2>&1 | tail -1"
try "$PY -c 'from app.matrix import Matrix; Matrix(3).set(3, 0, 1)' 2>&1 | tail -1"
check "Matrix 단위 테스트 통과" "$PY -m unittest tests.test_core.MatrixTest"
finish
