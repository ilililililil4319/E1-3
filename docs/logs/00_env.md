# 00. 실행 환경

> 이 파일은 `scripts/00_env.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:23 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## 운영체제

```console
$ uname -srm
Linux 6.18.58.1-microsoft-standard-WSL2 x86_64
```

```console
$ grep PRETTY_NAME /etc/os-release
PRETTY_NAME="Ubuntu 26.04.1 LTS"
```

## Python (요구: 3.8 이상, 외부 라이브러리 없음)

```console
$ python3 --version
Python 3.14.4
```

```console
$ which python3
/usr/bin/python3
```
- ✅ Python 3.8 이상

## 외부 라이브러리를 쓰지 않는지 (import 목록)

코드에 있는 import 줄을 모두 모았다. json, os, sys, time, math, re, unicodedata 는 모두 Python에 기본으로 들어 있는 표준 라이브러리다.

```console
$ grep -rhoE '^(import|from) [a-z_.]+' main.py app/ | sort | uniq -c
      1 from .
      1 from .console
      1 from .judge
      2 from .labels
      2 from .mac
      4 from .matrix
      1 from .report
      1 from app
      1 from app.console
      1 import json
      2 import math
      2 import os
      1 import re
      2 import sys
      1 import time
      1 import unicodedata
```
- ✅ numpy, pandas 를 import 하지 않는다

## Git

```console
$ git --version
git version 2.53.0
```

```console
$ git config user.name
ilililililil4319
```

```console
$ git config user.email
****@****
```

## 작업 위치와 원격 저장소

```console
$ pwd
~/codyssey/E1-3
```

```console
$ git remote -v
origin	git@github.com:ilililililil4319/E1-3.git (fetch)
origin	git@github.com:ilililililil4319/E1-3.git (push)
```

```console
$ git status -sb | head -1
## main...origin/main
```

---

**결과: 모든 단계 통과 ✅**
