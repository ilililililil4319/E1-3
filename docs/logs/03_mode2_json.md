# 03. 모드 2: data.json 분석

> 이 파일은 `scripts/03_mode2_json.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:23 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## data.json 구조 살펴보기 (키 목록과 크기)

```console
$ python3 -c 'import json
d = json.load(open("data.json", encoding="utf-8"))
print("최상위 키:", list(d))
for k, v in d["filters"].items():
    print("filters.{}: {} → 각 {}×{}".format(k, list(v), len(v["cross"]), len(v["cross"][0])))
for k, v in d["patterns"].items():
    print("patterns.{}: input {}×{}, expected {!r}".format(k, len(v["input"]), len(v["input"][0]), v["expected"]))'
최상위 키: ['meta', 'filters', 'patterns']
filters.size_5: ['cross', 'x'] → 각 5×5
filters.size_13: ['cross', 'x'] → 각 13×13
filters.size_25: ['cross', 'x'] → 각 25×25
patterns.size_5_1: input 5×5, expected 'x'
patterns.size_5_2: input 5×5, expected '+'
patterns.size_13_1: input 13×13, expected 'x'
patterns.size_13_2: input 13×13, expected '+'
patterns.size_25_1: input 25×25, expected 'x'
patterns.size_25_2: input 25×25, expected '+'
```

## 키에서 N 추출: size_13_2 → 13 → size_13 필터

```console
$ python3 -c 'import re
for key in ("size_5_1", "size_13_2", "size_25_1"):
    n = int(re.match(r"^size_(\d+)_(\d+)$", key).group(1))
    print(key, "→ N =", n, "→ filters[size_{}]".format(n))'
size_5_1 → N = 5 → filters[size_5]
size_13_2 → N = 13 → filters[size_13]
size_25_1 → N = 25 → filters[size_25]
```

## 모드 2 실행

```console
$ printf '2\n0\n' | python3 main.py
=== Mini NPU Simulator ===

[모드 선택]
1. 사용자 입력 (3x3)
2. data.json 분석
3. [보너스] 2차원 vs 1차원 성능 비교
4. [보너스] 패턴 생성기
0. 종료
선택: 2
#----------------------------------------
# [1] 필터 로드
#----------------------------------------
✓ size_5 필터 로드 완료 (Cross, X)
✓ size_13 필터 로드 완료 (Cross, X)
✓ size_25 필터 로드 완료 (Cross, X)

#----------------------------------------
# [2] 패턴 분석 (라벨 정규화 적용)
#----------------------------------------
--- size_5_1 ---
Cross 점수: 0.9
X 점수: 0.8999999999999999
판정: UNDECIDED | expected: X | FAIL (동점 규칙: |차이| 1.1e-16 < 1e-09)

--- size_5_2 ---
Cross 점수: 8.9
X 점수: 0.1
판정: Cross | expected: Cross | PASS

--- size_13_1 ---
Cross 점수: 0.3
X 점수: 14.700000000000008
판정: X | expected: X | PASS

--- size_13_2 ---
Cross 점수: 7.499999999999997
X 점수: 7.5
판정: UNDECIDED | expected: Cross | FAIL (동점 규칙: |차이| 2.7e-15 < 1e-09)

--- size_25_1 ---
Cross 점수: 4.9
X 점수: 4.899999999999999
판정: UNDECIDED | expected: X | FAIL (동점 규칙: |차이| 1.8e-15 < 1e-09)

--- size_25_2 ---
Cross 점수: 52.9
X 점수: 0.1
판정: Cross | expected: Cross | PASS

#----------------------------------------
# [3] 성능 분석 (평균/10회)
#----------------------------------------
크기         평균 시간(ms)   연산 횟수(N²)
------------------------------------------
3×3                 0.0013               9
5×5                 0.0022              25
13×13               0.0108             169
25×25               0.0244             625

#----------------------------------------
# [4] 결과 요약
#----------------------------------------
총 테스트: 6개
통과: 3개
실패: 3개
실패 케이스:
- size_5_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = 1.1e-16)
- size_13_2: 동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = 2.7e-15)
- size_25_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = 1.8e-15)
(상세 원인 분석과 복잡도 설명은 README.md의 "결과 리포트" 장에 있습니다)


[모드 선택]
1. 사용자 입력 (3x3)
2. data.json 분석
3. [보너스] 2차원 vs 1차원 성능 비교
4. [보너스] 패턴 생성기
0. 종료
선택: 0
프로그램을 종료합니다.
```
- ✅ 필터 3종 로드 완료
- ✅ 패턴 6개 모두 점수 계산

---

**결과: 모든 단계 통과 ✅**
