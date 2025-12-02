# Workflow Examples

ワークフローの構築を学ぶサンプルです。

## ファイル一覧

### workflow_agent.py
- `WorkflowBuilder` - シンプルなワークフローの構築
- `Executor` - ワークフロー内で実行されるタスク
- `.as_agent()` - ワークフローをエージェントとしてラップ

### review_workflow.py
- 複数Executor間の連携（Worker ↔ Reviewer）
- `ReviewRequest` / `ReviewResponse` - 構造化されたメッセージの受け渡し
- フィードバックループ（承認/却下による再生成）
- `WorkflowContext` - ワークフロー内でのコンテキスト管理
- `add_edge()` - Executor間のエッジ（接続）定義
