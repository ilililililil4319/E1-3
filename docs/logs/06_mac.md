# 06. MAC 연산 (반복문 직접 구현)

> 이 파일은 `scripts/06_mac.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:24 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## 구현 코드 (app/mac.py 의 mac 함수)

```console
$ sed -n '/^def mac(/,/return total/p' app/mac.py
def mac(pattern, filt):
    """2차원 MAC: 이중 for문으로 N×N번 곱하고 더한다. 결과는 float 점수.

    pattern, filt: Matrix 또는 2차원 리스트
    """
    p = pattern.rows() if isinstance(pattern, Matrix) else pattern
    f = filt.rows() if isinstance(filt, Matrix) else filt
    n = len(p)
    if n != len(f):
        raise ValueError("크기 불일치: 패턴 {0}×{0}, 필터 {1}×{1}".format(n, len(f)))

    total = 0.0
    for r in range(n):          # 행(가로줄)을 하나씩
        p_row = p[r]
        f_row = f[r]
        for c in range(n):      # 그 행의 칸을 하나씩
            total += p_row[c] * f_row[c]   # 곱해서(M) 누적(A)
    return total
```

## 미션 Case 1, 2: 십자가 입력 × 십자가 필터 = 5, × X 필터 = 1

```console
$ python3 -c 'from app.mac import mac
cross = [[0,1,0],[1,1,1],[0,1,0]]
x     = [[1,0,1],[0,1,0],[1,0,1]]
print("십자가 × 십자가 =", mac(cross, cross))
print("십자가 × X      =", mac(cross, x))'
십자가 × 십자가 = 5.0
십자가 × X      = 1.0
```

## 곱셈 과정을 한 칸씩 보기 (십자가 × X)

```console
$ python3 -c 'p = [[0,1,0],[1,1,1],[0,1,0]]; f = [[1,0,1],[0,1,0],[1,0,1]]
total = 0.0
for r in range(3):
    print("  ".join("{}×{}".format(p[r][c], f[r][c]) for c in range(3)))
    for c in range(3):
        total += p[r][c] * f[r][c]
print("합계 =", total)'
0×1  1×0  0×1
1×0  1×1  1×0
0×1  1×0  0×1
합계 = 1.0
```

## 결과는 float (소수 필터도 계산)

```console
$ python3 -c 'from app.mac import mac; print(mac([[1,1],[1,1]], [[0.5,0.25],[0.1,0.2]]))'
1.05
```
- ✅ numpy 없이 구현 (import 없음)
- ✅ MAC 단위 테스트 통과

---

**결과: 모든 단계 통과 ✅**
