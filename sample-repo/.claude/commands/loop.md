---
description: ループを1イテレーション回す(状態読込 → Maker → ゲート → Checker → 状態更新 → 判定)
---

ループを**1イテレーションだけ**回してください。手順:

1. **状態読込**: `docs/loop/STATE.md` と `docs/loop/criteria.md` を読む。
   - status が `done` または `requires human review` なら、その旨を報告して**何もせず終了**。
   - 停止条件チェック: 試行回数が上限(5回)に達している / 直近2回の試行で改善がない
     (ゲート不合格数も High 指摘数も減っていない) /
     直前の試行がツール連続失敗で終わっている — いずれかに該当したら status を
     `requires human review` に更新し、経緯の要約を STATE.md に書いて終了。
2. **Maker**: Task ツールで `loop-maker` サブエージェントを起動し、STATE.md の「次の一手」を
   実行させる。
3. **ゲート実行**(メインセッションで自分でも実行し、生の結果を記録する):
   - `python3 -m unittest discover -s tests`
   - `ruff check src tests`
4. **Checker**: Task ツールで `loop-checker` サブエージェントを起動し、独立検証させる。
   Maker の報告文をそのまま渡して「これを信じて」と言ってはならない。渡すのは題材と
   完了条件の所在(criteria.md)のみでよい。
5. **状態更新**: `docs/loop/STATE.md` に試行番号・日時・Maker 要約・ゲート結果(生の終了コード)・
   Checker 判定(High/Medium/Low件数)・次の一手を追記する。backlog 報告があれば backlog 節に足す。
6. **判定**:
   - Checker PASS(High 0件)かつ全ゲート合格 → status を `done` に更新し、完了サマリを報告。
     人間確認マトリックス(criteria.md)に従い、可逆で影響が狭い変更は自動採用として
     事後サマリで報告する(commit はユーザー指示があるまで行わない)。
   - Checker FAIL → status は `running` のまま、High 指摘を「次の一手」に反映して報告
     (次回 /loop で差し戻し分が実行される)。
   - 停止条件に該当 → status を `requires human review` にし、人間に要約を提示。

**やってはいけないこと**: 1回の実行で複数イテレーションを回す / Maker の自己申告だけで done に
する / Checker の High を無視して done にする / 題材と無関係な修正を混ぜる。
