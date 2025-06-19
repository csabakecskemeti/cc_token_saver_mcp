# cc_token_saver_mcp
Allow Claude code to use local llm for smaller tasks to save token or for specialized task

## MCP config
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
