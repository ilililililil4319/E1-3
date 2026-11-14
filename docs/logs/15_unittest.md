# 15. 단위 테스트

> 이 파일은 `scripts/15_unittest.sh`가 자동으로 만든 실행 기록입니다. `$` 뒤가 입력한 명령, 그 아래가 실제 출력입니다.
>
> - 실행 시각: 2026-11-14 22:51:36 KST
> - 데이터: 루트 `data.json` (실습용으로 망가뜨린 파일은 `.demo/`), 시간(ms)은 PC마다 다름
> - 개인정보 마스킹: 이메일·토큰은 `****`, 홈 경로는 `~`

```console
$ python3 -m unittest -v 2>&1
test_parse_row (tests.test_core.InputTest.test_parse_row) ... ok
test_float_error_is_tie (tests.test_core.JudgeTest.test_float_error_is_tie) ... ok
test_judge (tests.test_core.JudgeTest.test_judge) ... ok
test_normalize (tests.test_core.LabelTest.test_normalize) ... ok
test_unknown (tests.test_core.LabelTest.test_unknown) ... ok
test_flat_equals_2d (tests.test_core.MacTest.test_flat_equals_2d) ... ok
test_mission_examples (tests.test_core.MacTest.test_mission_examples) ... ok
test_size_mismatch (tests.test_core.MacTest.test_size_mismatch) ... ok
test_not_number (tests.test_core.MatrixTest.test_not_number) ... ok
test_not_square (tests.test_core.MatrixTest.test_not_square) ... ok
test_out_of_range (tests.test_core.MatrixTest.test_out_of_range) ... ok
test_sizes_3_5_13_25 (tests.test_core.MatrixTest.test_sizes_3_5_13_25) ... ok
test_bad_filter_is_skipped (tests.test_dataset.BrokenCaseTest.test_bad_filter_is_skipped) ... ok
test_bad_key_and_missing_filter (tests.test_dataset.BrokenCaseTest.test_bad_key_and_missing_filter) ... ok
test_bad_label_and_schema (tests.test_dataset.BrokenCaseTest.test_bad_label_and_schema) ... ok
test_size_mismatch (tests.test_dataset.BrokenCaseTest.test_size_mismatch) ... ok
test_missing_and_broken (tests.test_dataset.FileProblemTest.test_missing_and_broken) ... ok
test_real_data_json_loads (tests.test_dataset.RealDataTest.test_real_data_json_loads) ... ok

----------------------------------------------------------------------
Ran 18 tests in 0.004s

OK
```

---

**결과: 모든 단계 통과 ✅**
