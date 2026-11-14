# 01. 데이터 구조 (Matrix)

> 이 파일은 `scripts/01_data_structure.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:23 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## Matrix 만들기: 2차원 리스트 → Matrix

from_rows 는 [[0,1,0],[1,1,1],[0,1,0]] 같은 '리스트 안의 리스트'를 받아 정사각형인지, 모두 숫자인지 검사하고 저장한다.

```console
$ python3 -c 'from app.matrix import Matrix
m = Matrix.from_rows([[0,1,0],[1,1,1],[0,1,0]])
print(m, "크기:", m.size)
print(m.pretty())'
Matrix(3×3) 크기: 3
  0 1 0
  1 1 1
  0 1 0
```

## 특정 위치의 값 저장(set)과 읽기(get) - 위치는 0부터 센다

```console
$ python3 -c 'from app.matrix import Matrix
m = Matrix(3)
m.set(1, 2, 7)
print("(1,2)에 7 저장 → get(1,2) =", m.get(1, 2))
print(m.pretty())'
(1,2)에 7 저장 → get(1,2) = 7.0
  0 0 0
  0 0 7
  0 0 0
```

## 3×3, 5×5, 13×13, 25×25 모두 처리

```console
$ python3 -c 'from app.matrix import Matrix
for n in (3, 5, 13, 25):
    m = Matrix(n)
    m.set(n-1, n-1, 1)
    print("{0}×{0}: 칸 수 {1}, 마지막 칸 get({2},{2}) = {3}".format(n, len(m.to_flat()), n-1, m.get(n-1, n-1)))'
3×3: 칸 수 9, 마지막 칸 get(2,2) = 1.0
5×5: 칸 수 25, 마지막 칸 get(4,4) = 1.0
13×13: 칸 수 169, 마지막 칸 get(12,12) = 1.0
25×25: 칸 수 625, 마지막 칸 get(24,24) = 1.0
```

## 잘못된 데이터는 거절 (정사각형 아님, 숫자 아님, 범위 밖)

```console
$ python3 -c 'from app.matrix import Matrix; Matrix.from_rows([[1,2,3],[1,2]])' 2>&1 | tail -1
ValueError: 정사각형이 아닙니다: 2행인데 1번째 행의 열 수가 3
[종료 코드: 1]
```

```console
$ python3 -c 'from app.matrix import Matrix; Matrix.from_rows([[1,"a"],[1,2]])' 2>&1 | tail -1
ValueError: 1행 2열 값이 숫자가 아닙니다: 'a'
[종료 코드: 1]
```

```console
$ python3 -c 'from app.matrix import Matrix; Matrix(3).set(3, 0, 1)' 2>&1 | tail -1
IndexError: 위치 (3, 0)가 3×3 범위를 벗어났습니다
[종료 코드: 1]
```
- ✅ Matrix 단위 테스트 통과

---

**결과: 모든 단계 통과 ✅**
