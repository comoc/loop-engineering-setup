"""温度ログ行のパーサ。

ログ行形式: "YYYY-MM-DD HH:MM, sensor<ID>, <temperature>"
"""

from dataclasses import dataclass


class InvalidSensorId(ValueError):
    pass


@dataclass
class Record:
    timestamp: str
    sensor_id: str
    temperature: float


def validate_sensor_id(raw: str) -> str:
    """センサーIDを検証する。

    仕様: "sensor" + 半角数字2桁 (docs/spec.md 参照)。
    """
    if not raw.startswith("sensor"):
        raise InvalidSensorId(f"bad prefix: {raw!r}")
    digits = raw[len("sensor"):]
    # 仕様 (docs/spec.md): 半角数字(ASCII digits)ちょうど2桁のみ。
    # str.isdigit() は全角数字にも True を返すため、isascii() を併用する。
    if len(digits) != 2 or not (digits.isascii() and digits.isdigit()):
        raise InvalidSensorId(f"bad id digits: {raw!r}")
    return raw


def parse_line(line: str) -> Record:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"expected 3 fields: {line!r}")
    timestamp, sensor_id, temp = parts
    return Record(timestamp, validate_sensor_id(sensor_id), float(temp))
