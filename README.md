# cc_token_saver_mcp
Allow Claude code to use local llm for smaller tasks to save token or for specialized task.

Reduce your Claude Code tokens with ‘CC token saver’ MCP server that intelligently delegates simple tasks to your local LLM while keeping Claude Code for complex coordination and architecture decisions.

The MCP server exposes your local LLM as tools that Claude Code can use for:
- Code snippet generation
- Simple refactoring tasks
- Documentation writing
- Code reviews
- Basic Q&A
Claude Code automatically tries the local LLM first for simple tasks, only using premium tokens when necessary for complex reasoning and multi-step workflows.

## MCP server config
Create a `.env` file with the LLM config

Example:
```json
# Local LLM Configuration
OPENAI_API_KEY=none
OPENAI_BASE_URL=http://localhost:1234/v1
LOCAL_MODEL_NAME=qwen2.5-7b-instruct
LOCAL_LLM_TEMPERATURE=0.7
LOCAL_LLM_MAX_TOKENS=-1
```

## Claude Code MCP config
edit the `~/.claude.json` file

```json
"mcpServers": {
        "cc-token-saver": {
          "type": "stdio",
          "command": "python",
          "args": [
            "<path>/cc_token_saver_mcp/server.py"
          ]
        }
      },
```
