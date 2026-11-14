"""핵심 기능 단위 테스트 (표준 라이브러리 unittest). 실행: python3 -m unittest -v"""

import unittest

from app.generator import make_cross, make_x
from app.judge import EPSILON, is_tie, judge
from app.labels import normalize_label
from app.mac import mac, mac_flat
from app.console import parse_row
from app.matrix import Matrix

CROSS3 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
X3 = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]


class MatrixTest(unittest.TestCase):
    def test_sizes_3_5_13_25(self):
        for n in (3, 5, 13, 25):
            m = Matrix(n)
            m.set(n - 1, n - 1, 7)
            self.assertEqual(m.get(n - 1, n - 1), 7.0)
            self.assertEqual(len(m.to_flat()), n * n)

    def test_not_square(self):
        with self.assertRaises(ValueError):
            Matrix.from_rows([[1, 2, 3], [1, 2]])

    def test_not_number(self):
        with self.assertRaises(ValueError):
            Matrix.from_rows([[1, "a"], [1, 2]])
        with self.assertRaises(ValueError):
            Matrix.from_rows([[True, 0], [0, 1]])
        with self.assertRaises(ValueError):
            Matrix.from_rows([[float("nan"), 0], [0, 1]])

    def test_out_of_range(self):
        with self.assertRaises(IndexError):
            Matrix(3).set(3, 0, 1)


class InputTest(unittest.TestCase):
    def test_parse_row(self):
        self.assertEqual(parse_row("0 1 0", 3), [0.0, 1.0, 0.0])
        self.assertEqual(parse_row("  1   0.5  0 ", 3), [1.0, 0.5, 0.0])
        self.assertEqual(parse_row("010", 3), [0.0, 1.0, 0.0])
        for bad in ("0 1", "0 1 0 1", "0 a 0", "", "nan 0 0", "0,1,0"):
            with self.assertRaises(ValueError):
                parse_row(bad, 3)


class MacTest(unittest.TestCase):
    def test_mission_examples(self):
        self.assertEqual(mac(Matrix.from_rows(CROSS3), Matrix.from_rows(CROSS3)), 5.0)
        self.assertEqual(mac(Matrix.from_rows(CROSS3), Matrix.from_rows(X3)), 1.0)

    def test_flat_equals_2d(self):
        for n in (3, 5, 13, 25):
            p, f = make_cross(n), make_x(n)
            self.assertEqual(mac(p, f), mac_flat(p.to_flat(), f.to_flat()))

    def test_size_mismatch(self):
        with self.assertRaises(ValueError):
            mac(Matrix(3), Matrix(5))


class LabelTest(unittest.TestCase):
    def test_normalize(self):
        for raw, std in (("+", "Cross"), ("cross", "Cross"), (" CROSS ", "Cross"), ("x", "X"), ("X", "X")):
            self.assertEqual(normalize_label(raw), std)

    def test_unknown(self):
        for raw in ("o", "", None, 1):
            with self.assertRaises(ValueError):
                normalize_label(raw)


class JudgeTest(unittest.TestCase):
    def test_float_error_is_tie(self):
        self.assertNotEqual(0.1 + 0.2, 0.3)          # == 비교는 실패한다
        self.assertTrue(is_tie(0.1 + 0.2, 0.3))     # epsilon 비교는 같다고 본다

    def test_judge(self):
        self.assertEqual(judge(5.0, 1.0, "A", "B", "U"), "A")
        self.assertEqual(judge(1.0, 5.0, "A", "B", "U"), "B")
        self.assertEqual(judge(0.9, 0.8999999999999999, "A", "B", "U"), "U")
        self.assertEqual(judge(1.0, 1.0 + EPSILON * 2, "A", "B", "U"), "B")


if __name__ == "__main__":
    unittest.main()
