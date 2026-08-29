# templog 機能仕様

## ログ行形式

`<timestamp>, <sensor_id>, <temperature>`

## センサーIDの検証仕様

- 形式は `sensor` + **半角数字(ASCII digits)ちょうど2桁**。
- 全角数字・アルファベット・記号を含むIDは `InvalidSensorId` として弾くこと。
- 弾かれたIDは「想定内の異常系」であり、バグではない。

## 温度

- float にパースできない値は `ValueError`(想定内の異常系)。
