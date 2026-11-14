#!/usr/bin/env bash
# =============================================================================
# 실습 스크립트 공통 함수 (각 NN_*.sh가 맨 위에서 source 한다)
#
#   section "제목"      로그에 소제목(##)을 쓴다
#   note    "설명"      로그에 설명 문단을 쓴다
#   run     "명령"      명령을 실행하고 명령+출력을 로그에 남긴다. 실패하면 [중단]
#   try     "명령"      실패가 "예상된" 명령(일부러 오류 내는 실습). 실패해도 계속
#   check   "설명" "명령"  조용히 확인만 하고 ✅/❌ 한 줄을 남긴다. 실패하면 [중단]
#   play    "입력"      시뮬레이터에 입력을 파이프로 넣어 실행한다 (예: '2\n0\n')
#   finish             로그 마무리
#
# 로그 위치: docs/logs/<스크립트이름>.md   (```console 코드블록에 "$ 명령" + 출력)
# 개인정보: 이메일·GitHub 토큰은 ****, 홈 경로(/home/아이디)는 ~ 로 가린다.
# =============================================================================

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/docs/logs"
PY="${PYTHON:-python3}"

# 일부러 망가뜨린 data.json 같은 실습용 파일은 .demo/ 에 따로 둔다. (진짜 data.json은 건드리지 않음)
DEMO_DIR="$ROOT/.demo"
# 진짜 data.json 을 쓰도록 고정 (내 셸에 NPU_DATA_PATH 가 남아 있어도 영향 없게)
unset NPU_DATA_PATH NPU_REPEAT

cd "$ROOT" || exit 1
mkdir -p "$LOG_DIR"

NAME="$(basename "$0" .sh)"
LOG="$LOG_DIR/$NAME.md"

# ----------------------------------------------------------------- 내부 함수
_mask() {
    sed -E \
        -e 's#git@github\.com#__GH_SSH__#g' \
        -e 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/****@****/g' \
        -e 's#__GH_SSH__#git@github.com#g' \
        -e 's/(ghp_|gho_|github_pat_)[A-Za-z0-9_]+/\1****/g' \
        -e "s#${HOME}#~#g"
}

_record() {  # $1=run|try  $2=명령
    local mode="$1" cmd="$2" out code shown
    out="$(bash -o pipefail -c "$cmd" 2>&1)"
    code=$?
    # 141 = head 등이 필요한 줄만 읽고 파이프를 먼저 닫은 경우(SIGPIPE). 오류가 아니다.
    [ "$code" -eq 141 ] && code=0
    out="$(printf '%s' "$out" | _mask)"
    shown="$(printf '%s' "$cmd" | _mask)"

    {
        echo
        echo '```console'
        printf '$ %s\n' "$shown"
        [ -n "$out" ] && printf '%s\n' "$out"
        [ "$code" -ne 0 ] && echo "[종료 코드: $code]"
        echo '```'
    } >> "$LOG"

    printf '\n\033[1m$ %s\033[0m\n' "$shown"
    [ -n "$out" ] && printf '%s\n' "$out"

    if [ "$code" -ne 0 ]; then
        if [ "$mode" = "run" ]; then
            printf '\n**[중단]** 위 명령이 실패했습니다. (종료 코드 %s)\n' "$code" >> "$LOG"
            printf '\n\033[31m[중단]\033[0m %s (종료 코드 %s)\n  → 로그: docs/logs/%s.md\n' "$shown" "$code" "$NAME" >&2
            exit 1
        fi
        printf '\033[33m(예상된 실패: 종료 코드 %s)\033[0m\n' "$code"
    fi
    return 0
}

# ----------------------------------------------------------------- 공개 함수
start_log() {  # $1=제목
    {
        echo "# $1"
        echo
        echo "> 이 파일은 \`scripts/$NAME.sh\`가 자동으로 만든 실행 기록입니다. \`\$\` 뒤가 입력한 명령, 그 아래가 실제 출력입니다."
        echo ">"
        echo "> - 실행 시각: $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "> - 데이터: 루트 \`data.json\` (실습용으로 망가뜨린 파일은 \`.demo/\`), 시간(ms)은 PC마다 다름"
        echo "> - 개인정보 마스킹: 이메일·토큰은 \`****\`, 홈 경로는 \`~\`"
    } > "$LOG"
    printf '\n\033[1;36m▶ %s\033[0m\n' "$1"
}

section() {
    printf '\n## %s\n' "$1" >> "$LOG"
    printf '\n\033[1;34m── %s\033[0m\n' "$1"
}

note() {
    printf '\n%s\n' "$1" >> "$LOG"
    printf '  %s\n' "$1"
}

run() { _record run "$1"; }
try() { _record try "$1"; }

check() {  # $1=설명 $2=명령
    # 확인은 파이프 마지막 명령(grep 등)의 결과로 판단한다. (pipefail 없음)
    if bash -c "$2" > /dev/null 2>&1; then
        printf -- '- ✅ %s\n' "$1" >> "$LOG"
        printf '  \033[32m✅ %s\033[0m\n' "$1"
    else
        printf -- '- ❌ %s\n\n**[중단]** 확인 실패: `%s`\n' "$1" "$2" >> "$LOG"
        printf '\n\033[31m[중단]\033[0m 확인 실패: %s\n  → 로그: docs/logs/%s.md\n' "$1" "$NAME" >&2
        exit 1
    fi
}

play() {  # $1=입력 (줄바꿈은 \n 으로 적는다)
    run "printf '$1' | $PY main.py"
}

reset_demo() {
    run "rm -rf .demo && mkdir -p .demo"
}

finish() {
    printf '\n---\n\n**결과: 모든 단계 통과 ✅**\n' >> "$LOG"
    printf '\n\033[1;32m✔ 완료\033[0m → docs/logs/%s.md\n' "$NAME"
}
