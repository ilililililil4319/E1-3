# 09. 성능 분석 (크기별 평균 시간)

> 이 파일은 `scripts/09_performance.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:25 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

## 측정 코드: 연산 함수 호출 구간만 잰다 (app/perf.py)

```console
$ sed -n '/^def measure_ms/,/return total/p' app/perf.py
def measure_ms(func, args, repeat=None):
    """func(*args)를 repeat번 호출해 1회 평균 시간(ms)을 돌려준다.

    time.perf_counter(): 짧은 구간을 재는 데 쓰는 가장 정밀한 표준 시계.
    준비 작업(패턴 만들기, 출력)은 시계 바깥에 둔다.
    """
    repeat = repeat or repeat_count()
    func(*args)  # 워밍업 1회 (첫 호출의 준비 비용이 평균에 섞이지 않게) - 측정 제외
    total = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        func(*args)
        total += time.perf_counter() - start
    return total / repeat * 1000.0
```

## 모드 2 성능 표 (3×3은 생성기, 5/13/25는 data.json 필터)

```console
$ printf '2\n0\n' | python3 main.py | sed -n '/\[3\] 성능 분석/,/\[4\]/p' | head -n -1
# [3] 성능 분석 (평균/10회)
#----------------------------------------
크기         평균 시간(ms)   연산 횟수(N²)
------------------------------------------
3×3                 0.0010               9
5×5                 0.0015              25
13×13               0.0055             169
25×25               0.0256             625

#----------------------------------------
```

## 같은 측정을 3번 반복 (PC 상태에 따라 값이 조금씩 흔들림)

```console
$ printf '2\n0\n' | python3 main.py | grep -E '^(3×3|25×25) '
3×3                 0.0008               9
25×25               0.0182             625
```

```console
$ printf '2\n0\n' | python3 main.py | grep -E '^(3×3|25×25) '
3×3                 0.0009               9
25×25               0.0182             625
```

```console
$ printf '2\n0\n' | python3 main.py | grep -E '^(3×3|25×25) '
3×3                 0.0008               9
25×25               0.0182             625
```
- ✅ 표에 크기 4줄 (3, 5, 13, 25)
- ✅ 연산 횟수 N² = 9, 25, 169, 625

---

**결과: 모든 단계 통과 ✅**
