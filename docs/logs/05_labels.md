# 05. 라벨 정규화 (표준화)

> 이 파일은 `scripts/05_labels.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:24 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## data.json 원본에 들어 있는 라벨 모양

filter 키는 소문자 cross/x, expected는 기호 '+'와 소문자 'x' 다. 같은 뜻인데 모양이 다르다.

```console
$ grep -oE '"(cross|x)": \[' data.json | sort | uniq -c
      3 "cross": [
      3 "x": [
```

```console
$ grep -oE '"expected": "[^"]*"' data.json | sort | uniq -c
      3 "expected": "+"
      3 "expected": "x"
```

## normalize_label: 여러 모양 → Cross / X

```console
$ python3 -c 'from app.labels import normalize_label
for raw in ("+", "cross", " CROSS ", "x", "X"):
    print(repr(raw).ljust(10), "→", normalize_label(raw))'
'+'        → Cross
'cross'    → Cross
' CROSS '  → Cross
'x'        → X
'X'        → X
```

```console
$ python3 -c 'from app.labels import normalize_label; normalize_label("o")' 2>&1 | tail -1
ValueError: 알 수 없는 라벨: 'o' (허용: '+', 'cross', 'x')
[종료 코드: 1]
```

## 모드 2 출력: expected가 표준 라벨(Cross/X)로 표시된다

```console
$ printf '2\n0\n' | python3 main.py | grep 'expected:'
판정: UNDECIDED | expected: X | FAIL (동점 규칙: |차이| 1.1e-16 < 1e-09)
판정: Cross | expected: Cross | PASS
판정: X | expected: X | PASS
판정: UNDECIDED | expected: Cross | FAIL (동점 규칙: |차이| 2.7e-15 < 1e-09)
판정: UNDECIDED | expected: X | FAIL (동점 규칙: |차이| 1.8e-15 < 1e-09)
판정: Cross | expected: Cross | PASS
```
- ✅ 출력에 '+' 나 소문자 x 라벨이 남지 않음
- ✅ 라벨 단위 테스트 통과

---

**결과: 모든 단계 통과 ✅**
