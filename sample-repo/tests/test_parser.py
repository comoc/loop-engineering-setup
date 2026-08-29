import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from templog.parser import InvalidSensorId, parse_line, validate_sensor_id


class TestParser(unittest.TestCase):
    def test_parse_valid_line(self):
        r = parse_line("2026-08-29 12:00, sensor01, 23.5")
        self.assertEqual(r.sensor_id, "sensor01")
        self.assertAlmostEqual(r.temperature, 23.5)

    def test_bad_prefix(self):
        with self.assertRaises(InvalidSensorId):
            validate_sensor_id("probe01")

    def test_bad_length(self):
        with self.assertRaises(InvalidSensorId):
            validate_sensor_id("sensor1")

    def test_non_digit(self):
        with self.assertRaises(InvalidSensorId):
            validate_sensor_id("sensorAB")

    def test_fullwidth_digits_rejected(self):
        # 仕様 (docs/spec.md): ASCII数字ちょうど2桁のみ。全角数字は弾く。
        with self.assertRaises(InvalidSensorId):
            validate_sensor_id("sensor０１")  # U+FF10 U+FF11


if __name__ == "__main__":
    unittest.main()
