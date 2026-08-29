# Automations 雛形(未有効化 — 提示のみ)

**これらは雛形であり、有効化されていない。** トリガー自動化は実コスト(API利用・CI時間)が
発生するため、/loop の手動運用が安定してから、ユーザー自身が内容を確認のうえ有効化すること。
自律度は L1(報告のみ)→ L2(承認付き修正)→ L3(無人実行)の順で上げる。

## 案1: GitHub Actions(夜間ループ・L1 報告のみから開始)

有効化する場合は `.github/workflows/nightly-loop.yml` として配置(このファイルのままでは動かない)。

```yaml
name: nightly-loop
on:
  schedule:
    - cron: "0 18 * * 1-5"   # 平日 18:00 UTC(JST 翌3:00)
  workflow_dispatch: {}
permissions:
  contents: read             # L1: 読み取りのみ。L2以降で書込権限を検討
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install ruff
      - run: python3 -m unittest discover -s tests
      - run: ruff check src tests
      # L1ではゲート結果の報告まで。エージェント起動(claude -p "/loop" 等)は
      # コスト上限とシークレット管理を決めてから L2/L3 で追加する。
```

## 案2: ローカル cron / スケジュールタスク(L2〜)

```
# crontab 例(有効化しないこと — 雛形)
# 平日 6:00 に1イテレーションだけ回し、ログを残す
0 6 * * 1-5  cd /path/to/repo && claude -p "/loop" --max-turns 30 >> docs/loop/cron.log 2>&1
```

前提条件(有効化前に満たすこと):
- /loop の手動試運転が複数回安定して完走している
- 停止条件(反復5回・無進展2回・連続失敗)が STATE.md 上で機能した実績がある
- 予算上限(1日あたりの起動回数・トークン量)を決めてある
- 週次で STATE.md / backlog / 生成コードを人間がレビューする習慣を決めてある
