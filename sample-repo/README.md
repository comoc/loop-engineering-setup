# templog

温度センサーのログ行をパースする小さなCLIライブラリ。

- 入力例: `2026-08-29 12:00, sensor01, 23.5`
- 実行: `python3 -m templog.parser <logfile>`
- テスト: `python3 -m unittest discover -s tests`
