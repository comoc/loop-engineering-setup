# templog — Claude Code プロジェクトメモ

温度センサーログ行のパーサ。仕様の正は `docs/spec.md`(実装より仕様を優先し、乖離はバグとして扱う)。

## 検証コマンド(ループの検証ゲート)

- テスト: `python3 -m unittest discover -s tests`(終了コード0で合格)
- lint: `ruff check src tests`(終了コード0で合格)

## ループ運用ルール

- ループを回すときは `/loop` を実行する(1回で1イテレーション)。
- Maker(実装)と Checker(判定)は別サブエージェント(`.claude/agents/`)。
  **Checker に Write/Edit を与えない。Maker の自己申告で完了扱いにしない。**
- 完了・High・エラー性質判定・人間確認の基準は `docs/loop/criteria.md` が正。
- エラー=バグではない。`InvalidSensorId` / `ValueError` は仕様が定める想定内の異常系
  (docs/spec.md)。仕様との乖離だけが修正対象。
- 題材と無関係な問題を見つけたら直さず `docs/loop/STATE.md` の backlog に記録する。
- 停止条件: 反復5回上限 / 2回連続改善なし / ツール連続失敗 → status を
  `requires human review` にして人間へ。
- git commit / push はユーザーの明示指示があるまで行わない。

## 状態ファイル

- `docs/loop/STATE.md` — status・試行履歴・ゲート結果・未解決・backlog・次の一手。
  ループの記憶はコンテキストではなくこのファイルに置く(エージェントは忘れる、リポジトリは忘れない)。
- `docs/loop/criteria.md` — 判定基準。

## Automations

- 未有効化。雛形は `docs/loop/automations.sample.md`(試運転が安定してからユーザー自身が有効化する)。
