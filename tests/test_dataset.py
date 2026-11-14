"""data.json 검증 테스트: 정상 데이터, 크기 불일치, 키·라벨 오류, 파일 문제."""

import json
import os
import tempfile
import unittest

from app import dataset
from app.generator import make_cross

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RealDataTest(unittest.TestCase):
    def test_real_data_json_loads(self):
        data = dataset.load_json(os.path.join(ROOT, "data.json"))
        filters, messages = dataset.parse_filters(data["filters"])
        self.assertEqual(sorted(filters), [5, 13, 25])
        self.assertTrue(all(ok for ok, _ in messages))
        keys = [k for k, _ in dataset.iter_cases(data["patterns"])]
        self.assertEqual(keys[0], "size_5_1")      # 숫자 순서 정렬 (size_13보다 size_5가 먼저)
        for key, item in dataset.iter_cases(data["patterns"]):
            n, pattern, expected = dataset.prepare_case(key, item, filters)
            self.assertEqual(pattern.size, n)
            self.assertIn(expected, ("Cross", "X"))


class BrokenCaseTest(unittest.TestCase):
    def setUp(self):
        rows = make_cross(5).rows()
        self.filters, _ = dataset.parse_filters({"size_5": {"cross": rows, "x": rows}})

    def reason(self, key, item):
        with self.assertRaises(ValueError) as ctx:
            dataset.prepare_case(key, item, self.filters)
        return str(ctx.exception)

    def test_size_mismatch(self):
        item = {"input": make_cross(3).rows(), "expected": "+"}
        self.assertIn("크기 불일치", self.reason("size_5_9", item))

    def test_bad_key_and_missing_filter(self):
        item = {"input": make_cross(5).rows(), "expected": "+"}
        self.assertIn("키 형식 오류", self.reason("five_1", item))
        self.assertIn("필터 없음", self.reason("size_7_1", item))

    def test_bad_label_and_schema(self):
        self.assertIn("라벨 오류", self.reason("size_5_1", {"input": make_cross(5).rows(), "expected": "o"}))
        self.assertIn("스키마 오류", self.reason("size_5_1", {"expected": "+"}))
        self.assertIn("스키마 오류", self.reason("size_5_1", {"input": [[1, 2], [3]], "expected": "+"}))

    def test_bad_filter_is_skipped(self):
        filters, messages = dataset.parse_filters({"size_5": {"cross": make_cross(3).rows()}})
        self.assertEqual(filters, {})
        self.assertFalse(messages[0][0])


class FileProblemTest(unittest.TestCase):
    def test_missing_and_broken(self):
        with self.assertRaises(dataset.DataError):
            dataset.load_json("/없는/경로/data.json")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{ 깨진 json")
        try:
            with self.assertRaises(dataset.DataError):
                dataset.load_json(f.name)
        finally:
            os.unlink(f.name)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"filters": {}}, f)
        try:
            with self.assertRaises(dataset.DataError):
                dataset.load_json(f.name)
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
