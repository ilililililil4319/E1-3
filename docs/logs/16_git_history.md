# 16. Git 이력 (커밋 단위, 브랜치 병합)

> 이 파일은 `scripts/16_git_history.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:36 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

```console
$ git log --oneline --graph --all | head -n 40
* fd48095 Docs: README 22장과 결과 리포트 (실패 원인, 시간 복잡도)
* 04e9e3f Docs: 환경 세팅 문서 (Windows WSL2 기준)
* d85d815 Fix: 07 스크립트 비교 열 이름을 단순비교로 (> 비교임을 명확히)
* 5f268dd Test: 보너스·대량 데이터·단위 테스트·Git 이력 스크립트 12~16
* 5964999 Test: 기능 요구사항별 실습 스크립트 01~11
* e4bf2fb Chore: 실습 스크립트 공통 함수와 전체 실행 (lib.sh, run_all.sh, 00_env.sh)
*   303a400 Merge: feature/performance (성능 분석과 보너스)
|\  
| * edfb695 Test: 단위 테스트 (Matrix, 입력, MAC, 라벨, epsilon, 스키마)
| * efc5767 Feat: 성능 분석 출력과 보너스 메뉴 3, 4 연결
| * 1778e07 Feat: 성능 측정 (10회 평균 ms, N² 표, 2차원/1차원 비교)
| * d5940e8 Feat: 1차원 배열 변환과 1차원 MAC (보너스 1)
| * b8570eb Feat: 패턴 생성기 N×N Cross/X (보너스 2)
|/  
*   b0d3eeb Merge: feature/json-analysis (모드 2 data.json 분석)
|\  
| * 32c0d93 Feat: 모드 2 data.json 분석 흐름 (케이스 단위 PASS/FAIL)
| * f343db4 Feat: 결과 요약 (전체/통과/실패, 실패 사유 목록)
| * fbb21d7 Feat: data.json 로드와 스키마 검증 (키에서 N 추출, 크기 확인)
|/  
* 4dbc2ee Feat: 모드 1 사용자 입력 흐름과 메인 메뉴 (main.py)
* 7139112 Feat: 3×3 줄 단위 입력과 형식 검증 (재입력 유도)
* 5ed9299 Feat: epsilon 기반 점수 비교와 판정 (1e-9)
* e8adf4c Feat: 라벨 정규화 (+, cross → Cross / x → X)
* c3e1ecb Feat: MAC 연산 (이중 반복문, 외부 라이브러리 없음)
* 01e846f Feat: Matrix 데이터 구조 (n×n 저장, get/set, 입력 검증)
* d110b58 Chore: 프로젝트 시작 (.gitignore, 미션 data.json)
```

```console
$ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature/json-analysis
  remotes/origin/feature/performance
  remotes/origin/main
```

```console
$ git log --merges --oneline
303a400 Merge: feature/performance (성능 분석과 보너스)
b0d3eeb Merge: feature/json-analysis (모드 2 data.json 분석)
```

```console
$ git log --format='%h %an %s' | head -n 30
fd48095 ilililililil4319 Docs: README 22장과 결과 리포트 (실패 원인, 시간 복잡도)
04e9e3f ilililililil4319 Docs: 환경 세팅 문서 (Windows WSL2 기준)
d85d815 ilililililil4319 Fix: 07 스크립트 비교 열 이름을 단순비교로 (> 비교임을 명확히)
5f268dd ilililililil4319 Test: 보너스·대량 데이터·단위 테스트·Git 이력 스크립트 12~16
5964999 ilililililil4319 Test: 기능 요구사항별 실습 스크립트 01~11
e4bf2fb ilililililil4319 Chore: 실습 스크립트 공통 함수와 전체 실행 (lib.sh, run_all.sh, 00_env.sh)
303a400 ilililililil4319 Merge: feature/performance (성능 분석과 보너스)
edfb695 ilililililil4319 Test: 단위 테스트 (Matrix, 입력, MAC, 라벨, epsilon, 스키마)
b0d3eeb ilililililil4319 Merge: feature/json-analysis (모드 2 data.json 분석)
efc5767 ilililililil4319 Feat: 성능 분석 출력과 보너스 메뉴 3, 4 연결
32c0d93 ilililililil4319 Feat: 모드 2 data.json 분석 흐름 (케이스 단위 PASS/FAIL)
1778e07 ilililililil4319 Feat: 성능 측정 (10회 평균 ms, N² 표, 2차원/1차원 비교)
f343db4 ilililililil4319 Feat: 결과 요약 (전체/통과/실패, 실패 사유 목록)
d5940e8 ilililililil4319 Feat: 1차원 배열 변환과 1차원 MAC (보너스 1)
b8570eb ilililililil4319 Feat: 패턴 생성기 N×N Cross/X (보너스 2)
fbb21d7 ilililililil4319 Feat: data.json 로드와 스키마 검증 (키에서 N 추출, 크기 확인)
4dbc2ee ilililililil4319 Feat: 모드 1 사용자 입력 흐름과 메인 메뉴 (main.py)
7139112 ilililililil4319 Feat: 3×3 줄 단위 입력과 형식 검증 (재입력 유도)
5ed9299 ilililililil4319 Feat: epsilon 기반 점수 비교와 판정 (1e-9)
e8adf4c ilililililil4319 Feat: 라벨 정규화 (+, cross → Cross / x → X)
c3e1ecb ilililililil4319 Feat: MAC 연산 (이중 반복문, 외부 라이브러리 없음)
01e846f ilililililil4319 Feat: Matrix 데이터 구조 (n×n 저장, get/set, 입력 검증)
d110b58 ilililililil4319 Chore: 프로젝트 시작 (.gitignore, 미션 data.json)
```
- ✅ 병합 커밋이 2개 이상

---

**결과: 모든 단계 통과 ✅**
