# 08. 판정과 PASS/FAIL 출력

> 이 파일은 `scripts/08_judge_passfail.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:25 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## 케이스별 점수와 판정

```console
$ printf '2\n0\n' | python3 main.py | sed -n '/\[2\] 패턴 분석/,/\[3\]/p'
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
```

## PASS / FAIL 개수

```console
$ printf '2\n0\n' | python3 main.py | grep -oE '\| (PASS|FAIL)' | sort | uniq -c
      3 | FAIL
      3 | PASS
```
- ✅ PASS 3개
- ✅ FAIL 3개 (모두 동점 규칙)

---

**결과: 모든 단계 통과 ✅**
