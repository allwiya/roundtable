# Architecture

Technical architecture documentation for Roundtable AI.

## System Overview

Roundtable AI is a Model Context Protocol (MCP) server that orchestrates multiple AI coding assistants through a unified interface.

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Clients                          │
│  (Cursor, VS Code, Claude Desktop, JetBrains, etc.)    │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol (stdio/SSE)
┌────────────────────▼────────────────────────────────────┐
│              Roundtable MCP Server                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  FastMCP Server                                  │  │
│  │  - Tool Registration                             │  │
│  │  - Request Routing                               │  │
│  │  - Progress Reporting                            │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Configuration Manager                           │  │
│  │  - Environment Variables                         │  │
│  │  - Availability Cache                            │  │
│  │  - Agent Selection                               │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              CLI Adapter Framework                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  BaseCLI (Abstract)                              │  │
│  │  - check_availability()                          │  │
│  │  - execute_with_streaming()                      │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────┬──────────┬──────────┬──────────┬──────┐  │
│  │ CodexCLI │ClaudeCLI │CursorCLI │GeminiCLI │QwenCLI│ │
│  └──────────┴──────────┴──────────┴──────────┴──────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              External CLI Tools                         │
│  ┌──────────┬──────────┬──────────┬──────────┬──────┐  │
│  │  codex   │  claude  │  cursor  │  gemini  │ qwen │  │
│  └──────────┴──────────┴──────────┴──────────┴──────┘  │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. MCP Server Layer

**Location:** `roundtable_mcp_server/server.py`

**Responsibilities:**
- Expose MCP tools to clients
- Handle tool invocations
- Manage configuration
- Report progress to clients
- Aggregate responses

**Key Classes:**
- `ServerConfig` - Configuration model
- `FastMCP` - MCP server instance

**Tools Exposed:**
- `check_{agent}_availability` - 5 tools
- `{agent}_subagent` - 5 tools
- Total: 10 tools

### 2. CLI Adapter Layer

**Location:** `claudable_helper/cli/`

**Responsibilities:**
- Abstract CLI interactions
- Parse streaming output
- Handle errors
- Map models
- Manage sessions

**Key Classes:**
- `BaseCLI` - Abstract base class
- `{Agent}CLI` - Concrete implementations
- `CLIType` - Agent type enum
- `AdapterSession` - Session management

**Adapters:**
1. `CodexCLI` - OpenAI Codex
2. `ClaudeCodeCLI` - Anthropic Claude Code
3. `CursorAgentCLI` - Cursor
4. `GeminiCLI` - Google Gemini
5. `QwenCLI` - Alibaba Qwen

### 3. Message System

**Location:** `claudable_helper/models/messages.py`

**Message Types:**
- `ASSISTANT` - Agent responses
- `TOOL_USE` - Tool invocations
- `TOOL_RESULT` - Tool results
- `ERROR` - Error messages
- `RESULT` - Final results

**Message Flow:**
```
CLI Output → Parser → Message → Aggregator → Response
```

### 4. Model Mapping

**Location:** `claudable_helper/cli/base.py`

Maps unified model names to CLI-specific names:

```python
MODEL_MAPPING = {
    "claude": {
        "opus-4.1": "claude-opus-4-1-20250805",
        "sonnet-4": "claude-sonnet-4-20250514"
    },
    "cursor": {
        "gpt-5": "gpt-5",
        "sonnet-4": "sonnet-4"
    },
    # ... etc
}
```

## Data Flow

### Request Flow

```
1. User Request
   ↓
2. MCP Client → MCP Server
   ↓
3. Tool Invocation (e.g., codex_subagent)
   ↓
4. Configuration Check
   ↓
5. Path Validation
   ↓
6. CLI Adapter Initialization
   ↓
7. Availability Check
   ↓
8. Command Construction
   ↓
9. Process Execution
   ↓
10. Stream Parsing
    ↓
11. Message Processing
    ↓
12. Progress Reporting
    ↓
13. Response Aggregation
    ↓
14. Return to Client
```

### Streaming Flow

```
CLI Process
    ↓ stdout
LineBuffer (handles large lines)
    ↓
JSON Parser
    ↓
Message Constructor
    ↓
Message Type Detection
    ↓
Content Extraction
    ↓
Progress Reporter (MCP)
    ↓
Response Aggregator
    ↓
Final Response
```

## Configuration System

### Priority Order

1. **Command Line Args** (`--agents`)
2. **Environment Variables** (`CLI_MCP_SUBAGENTS`)
3. **Availability Cache** (`~/.roundtable/availability_check.json`)
4. **Default** (all agents)

### Environment Variables

```bash
CLI_MCP_SUBAGENTS="codex,gemini"    # Agent selection
CLI_MCP_WORKING_DIR="/path"         # Working directory
CLI_MCP_DEBUG=true                  # Debug logging
CLI_MCP_VERBOSE=true                # Verbose output
CLI_MCP_IGNORE_AVAILABILITY=true    # Ignore cache
```

## Availability System

### Detection Process

```
1. Check CLI exists (shutil.which)
   ↓
2. Verify executable
   ↓
3. Test execution
   ↓
4. Cache result
   ↓
5. Return availability status
```

### Cache Location

- `~/.roundtable/availability_check.json`

### Cache Format

```json
{
  "codex": true,
  "claude": false,
  "cursor": true,
  "gemini": true,
  "qwen": false
}
```

## Error Handling

### Error Types

1. **Configuration Errors** - Invalid config
2. **Availability Errors** - CLI not found
3. **Execution Errors** - CLI execution failed
4. **Parsing Errors** - Invalid output format
5. **Timeout Errors** - Execution timeout

### Error Flow

```
Error Occurs
    ↓
Log Error (with context)
    ↓
Create Error Message
    ↓
Report to Client (ctx.error)
    ↓
Return Error Response
```

## Performance Considerations

### Streaming

- Uses `LineBuffer` for large lines (>64KB)
- Async generators for memory efficiency
- Progress reporting for UX

### Caching

- Availability results cached
- Session IDs for continuity
- Model mappings preloaded

### Concurrency

- Async/await throughout
- Non-blocking I/O
- Parallel agent execution (client-side)

## Security

### Input Validation

- Path validation (absolute paths)
- Directory existence checks
- Command sanitization

### Isolation

- Each agent runs in separate process
- No shared state between agents
- Clean environment variables

### Logging

- Sensitive data filtered
- Debug logs separate from user output
- Structured logging format

## Extensibility

### Adding New Agents

1. Create adapter class extending `BaseCLI`
2. Implement required methods
3. Add model mapping
4. Register in server
5. Add tests

### Adding New Features

1. Add to appropriate layer
2. Update interfaces if needed
3. Add tests
4. Update documentation

## Testing Strategy

### Unit Tests

- Individual component testing
- Mock external dependencies
- Fast execution

### Integration Tests

- End-to-end flows
- Real CLI interactions (optional)
- Slower execution

### Coverage Target

- 80%+ overall coverage
- 100% for critical paths

## Deployment

### Package Distribution

- PyPI package
- GitHub releases
- Docker image (future)

### Installation Methods

1. `pip install roundtable-ai`
2. `uvx roundtable-ai@latest`
3. From source: `pip install -e .`

## Monitoring

### Logs

- Location: `.juno_task/logs/roundtable_mcp_server.log`
- Format: Structured with timestamps
- Levels: DEBUG, INFO, ERROR

### Metrics (Future)

- Execution time per agent
- Token usage
- Success/failure rates
- Agent selection frequency

## Future Enhancements

### Planned

- More agents (Windsurf, Aider, etc.)
- Metrics collection
- Health checks
- Performance monitoring
- Docker support

### Under Consideration

- Web UI
- Agent chaining
- Custom agent plugins
- Cloud deployment
