# loop-engineering-setup

ループエンジニアリング(Loop Engineering)の実戦の「お膳立て」を一気通貫で行う Claude スキル。

ループエンジニアリングは Addy Osmani が2026年6月に提唱した手法で、原文の定義は
"Loop engineering is replacing yourself as the person who prompts the agent."
— 自分がエージェントにプロンプトを打つのをやめ、プロンプトを打つシステム自体を設計する、という考え方。
プロンプト → コンテキスト → ハーネスに続く第4世代と位置づけられ、
**Automations / Worktrees / Skills / Connectors / Sub-agents / Memory** の6要素で構成される。

## このスキルがやること

対象リポジトリに対して次の5フェーズを実行する:

1. **診断** — 検証ゲート(テスト/lint/型)の実在を実際に走らせて確認し、6要素+ゲートを A〜F で採点
   (`docs/loop/REPORT.md` に保存)
2. **設計** — 題材選定(反復性/検証可能性/経済価値)とループ設計書の提示・承認
   (`docs/loop/DESIGN.md` に保存)
3. **生成** — 実行に必要な一式を生成:
   - `.claude/agents/loop-maker.md` … 実装担当。エラー性質判定(想定内 vs バグ)を最初に置く。テストファースト推奨
   - `.claude/agents/loop-checker.md` … 判定専用。Write/Edit なし+書込系 Bash 禁止。fresh context で独立検証
   - `.claude/commands/loop.md` … 1イテレーションを回すオーケストレータ(/loop)。STATE.md の更新責務を持つ
   - `docs/loop/STATE.md` … 状態(status / 試行履歴 / 未解決 / backlog)
   - `docs/loop/criteria.md` … 完了条件・High定義・エラー性質判定・人間確認マトリックス・停止条件
   - `CLAUDE.md` 追記(なければ新規作成)
   - `docs/loop/automations.sample.md` … Automations 雛形(不活性。有効化はユーザー自身が行う)
4. **試運転** — 最小題材で1イテレーション実行+停止条件のドライラン確認
5. **運用ガイド** — /loop の回し方、L1(報告)→L2(承認付き)→L3(無人)の段階的自律化、コストガード

設計の核: 書いた者に採点させない(Maker/Checker分離)・完了は機械検証ゲートで判定・
状態はディスクに置く・停止条件は多層(回数/無進展/連続失敗/予算)・人間確認は可逆性×影響範囲で濃淡。

## 使い方(インストール)

Claude Code の場合、このリポジトリの `SKILL.md` を次のいずれかに置く:

- 個人スキル: `~/.claude/skills/loop-engineering-setup/SKILL.md`(全プロジェクトで有効)
- プロジェクトスキル: 対象リポジトリの `.claude/skills/loop-engineering-setup/SKILL.md`

claude.ai / Cowork では、設定の機能(Capabilities)からスキルとして追加する。

発動はセッションで「ループエンジニアリングを実践したい」「このリポジトリでループを回したい」などと
言うだけでよい(スキル名の明示は不要)。生成後の日常運用は、対象リポジトリで `/loop` を都度実行する
(1回=1イテレーション)。

## リポジトリ構成

| パス | 内容 |
|---|---|
| `SKILL.md` | スキル本体 |
| `sample-repo/` | スモークテスト済みサンプル(templog: 温度ログパーサ)。スキルが生成する一式(`.claude/agents/`、`/loop` コマンド、`docs/loop/`)の実例 |
| `sample-repo/SMOKE_REPORT.md` | 試運転の顛末: 仕込まれた全角数字バグをループが検出 → テストファーストで RED を確認して修正 → Checker が独立検証して完了、までの記録とスキルへのフィードバック |

sample-repo の検証ゲートは `python3 -m unittest discover -s tests` と `ruff check src tests`。

## 経緯

2026-08-29 作成。Web上の主要記事の調査 → SKILL.md 起草 → サンプルリポジトリでのスモークテスト →
テストで見つかった曖昧点(無人実行時の承認代替、成果物の保存先、Checker の Bash 抜け穴、
停止条件のドライラン確認など)を反映、という手順で作られた。

## 参考文献

- Addy Osmani "Loop Engineering" — https://addyosmani.com/blog/loop-engineering/ (原典)
- Addy Osmani "Agent Harness Engineering" — https://addyosmani.com/blog/agent-harness-engineering/
- IBM "What Is Loop Engineering?" — https://www.ibm.com/think/topics/loop-engineering
- お前のループエンジニアリングは間違っている — https://zenn.dev/t_hayashi/articles/20ec8fbebbeabb
- Claude Code で「ループエンジニアリング」を実践してみた — https://zenn.dev/tetsu_don/articles/e40b95dfc726ac
- ループエンジニアリングとは？6つの構成要素 — https://www.ai-souken.com/article/what-is-loop-engineering
- ループエンジニアリングとは？導入ステップ — https://jp.findy-team.io/blogs/loop-engineering/
