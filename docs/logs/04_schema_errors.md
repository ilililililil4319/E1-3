# 04. 모드 2: 스키마 오류와 크기 불일치

> 이 파일은 `scripts/04_schema_errors.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:24 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

```console
$ rm -rf .demo && mkdir -p .demo
```

## 실습용 망가진 파일 만들기 (.demo/, 진짜 data.json은 그대로)

```console
$ python3 scripts/make_broken.py .demo
만듦: .demo/broken_cases.json
만듦: .demo/broken_filter.json
만듦: .demo/broken_syntax.json
```

## 케이스 단위 오류 5종: 크기 불일치, 필터 없음, 키 형식, 라벨, 숫자 아님

NPU_DATA_PATH 환경 변수로 읽을 파일을 바꾼다. 정상 6개는 그대로 판정되고 망가진 5개만 FAIL 이 된다.

```console
$ printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json python3 main.py | sed -n '/\[2\]/,/\[3\]/p'
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

--- size_5_3 ---
FAIL (크기 불일치: 패턴 3×3, 필터 5×5)

--- size_5_4 ---
FAIL (라벨 오류: 알 수 없는 라벨: 'o' (허용: '+', 'cross', 'x'))

--- size_5_5 ---
FAIL (스키마 오류: input 1행 2열 값이 숫자가 아닙니다: '1')

--- size_7_1 ---
FAIL (필터 없음: size_7 필터가 로드되지 않음)

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

--- pattern_A ---
FAIL (키 형식 오류: size_{N}_{idx} 형태가 아님)

#----------------------------------------
# [3] 성능 분석 (평균/10회)
```

```console
$ printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_cases.json python3 main.py | sed -n '/\[4\] 결과 요약/,$p'
# [4] 결과 요약
#----------------------------------------
총 테스트: 11개
통과: 3개
실패: 8개
실패 케이스:
- size_5_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = 1.1e-16)
- size_5_3: 크기 불일치: 패턴 3×3, 필터 5×5
- size_5_4: 라벨 오류: 알 수 없는 라벨: 'o' (허용: '+', 'cross', 'x')
- size_5_5: 스키마 오류: input 1행 2열 값이 숫자가 아닙니다: '1'
- size_7_1: 필터 없음: size_7 필터가 로드되지 않음
- size_13_2: 동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = 2.7e-15)
- size_25_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL (|Cross-X| = 1.8e-15)
- pattern_A: 키 형식 오류: size_{N}_{idx} 형태가 아님
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
- ✅ 크기 불일치 → FAIL
- ✅ 총 11개 중 실패 8개(동점 3 + 오류 5)
- ✅ 오류가 있어도 끝까지 실행 (종료 메시지)

## 필터가 망가진 경우: size_13 x 필터가 12×12 → 필터 로드 실패 → size_13 패턴 FAIL

```console
$ printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_filter.json python3 main.py | sed -n '/\[1\]/,/\[2\]/p'
# [1] 필터 로드
#----------------------------------------
✓ size_5 필터 로드 완료 (Cross, X)
✗ size_13 필터 로드 실패: X 필터 크기 12×12 ≠ 키의 N=13
✓ size_25 필터 로드 완료 (Cross, X)

#----------------------------------------
# [2] 패턴 분석 (라벨 정규화 적용)
```

```console
$ printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_filter.json python3 main.py | grep -A1 -- '--- size_13'
--- size_13_1 ---
FAIL (필터 없음: size_13 필터가 로드되지 않음)
--
--- size_13_2 ---
FAIL (필터 없음: size_13 필터가 로드되지 않음)
```

## 파일 단위 오류: JSON 문법 오류, 파일 없음 → 안내 후 메뉴로 돌아옴

```console
$ printf '2\n0\n' | NPU_DATA_PATH=.demo/broken_syntax.json python3 main.py | tail -n 12
#----------------------------------------
✗ data.json을 읽을 수 없습니다: JSON 형식 오류: Expecting ',' delimiter (줄 3, 칸 3)
  → 파일 위치와 형식을 확인하세요. (메뉴로 돌아갑니다)

[모드 선택]
1. 사용자 입력 (3x3)
2. data.json 분석
3. [보너스] 2차원 vs 1차원 성능 비교
4. [보너스] 패턴 생성기
0. 종료
선택: 0
프로그램을 종료합니다.
```

```console
$ printf '2\n0\n' | NPU_DATA_PATH=.demo/없는파일.json python3 main.py | grep -A1 '✗'
✗ data.json을 읽을 수 없습니다: 파일이 없습니다: .demo/없는파일.json
  → 파일 위치와 형식을 확인하세요. (메뉴로 돌아갑니다)
```
- ✅ JSON 문법 오류 안내
- ✅ 문법 오류 뒤에도 종료 코드 0

---

**결과: 모든 단계 통과 ✅**
