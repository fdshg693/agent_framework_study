# Agent Examples

エージェントの作成と活用を学ぶサンプルです。

## ファイル一覧

### chat_agent_instance.py
- `ChatAgent` - ChatClientを使用したエージェントの作成
- `BaseAgent` - カスタムエージェントの実装（SimpleAgent）
- `run()` / `run_stream()` メソッドの使用

### agent_chat.py
- `AgentMiddleware` - ミドルウェアによるエージェント処理のカスタマイズ
- ツール（関数）をエージェントに追加する方法
- `@handler`デコレータの使用

### agent_as_tool.py
- `agent.as_tool()` - エージェントをツールとして変換
- 他のエージェントから呼び出し可能なツール化
