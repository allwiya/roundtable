"""Unit tests for MCP tools."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from roundtable_mcp_server import server


@pytest.mark.unit
@pytest.mark.asyncio
class TestAvailabilityTools:
    """Test availability check tools."""
    
    async def test_check_codex_availability_enabled(self, mock_context):
        """Test check_codex_availability when enabled."""
        server.enabled_subagents = {"codex"}
        
        with patch('roundtable_mcp_server.server._import_module_item') as mock_import:
            mock_check = AsyncMock(return_value="✅ Codex available")
            mock_import.return_value = mock_check
            
            result = await server.check_codex_availability(mock_context)
            
            assert "✅" in result
            mock_check.assert_called_once()
    
    async def test_check_codex_availability_disabled(self, mock_context):
        """Test check_codex_availability when disabled."""
        server.enabled_subagents = set()
        
        result = await server.check_codex_availability(mock_context)
        
        assert "❌" in result
        assert "not enabled" in result
    
    async def test_check_qwen_availability_enabled(self, mock_context):
        """Test check_qwen_availability when enabled."""
        server.enabled_subagents = {"qwen"}
        
        with patch('roundtable_mcp_server.server._import_module_item') as mock_import:
            mock_check = AsyncMock(return_value="✅ Qwen available")
            mock_import.return_value = mock_check
            
            result = await server.check_qwen_availability(mock_context)
            
            assert "✅" in result
            mock_check.assert_called_once()


@pytest.mark.unit
@pytest.mark.asyncio
class TestSubagentTools:
    """Test subagent execution tools."""
    
    async def test_codex_subagent_disabled(self, mock_context, sample_instruction):
        """Test codex_subagent when disabled."""
        server.enabled_subagents = set()
        
        result = await server.codex_subagent(
            instruction=sample_instruction,
            ctx=mock_context
        )
        
        assert "❌" in result
        assert "not enabled" in result
    
    async def test_codex_subagent_invalid_path(self, mock_context, sample_instruction):
        """Test codex_subagent with invalid project path."""
        server.enabled_subagents = {"codex"}
        server.CLI_ADAPTERS_AVAILABLE = True
        
        with patch('roundtable_mcp_server.server.CodexCLI') as mock_cli:
            result = await server.codex_subagent(
                instruction=sample_instruction,
                project_path="/nonexistent/path",
                ctx=mock_context
            )
            
            assert "❌" in result
            assert "does not exist" in result
    
    async def test_qwen_subagent_success(self, mock_context, sample_instruction, temp_project_dir):
        """Test qwen_subagent successful execution."""
        server.enabled_subagents = {"qwen"}
        server.CLI_ADAPTERS_AVAILABLE = True
        server.config = MagicMock(verbose=False)
        
        with patch('roundtable_mcp_server.server.QwenCLI') as mock_cli_class:
            mock_cli = MagicMock()
            mock_cli.check_availability = AsyncMock(return_value={"available": True})
            
            # Mock streaming messages
            async def mock_stream(*args, **kwargs):
                msg = MagicMock()
                msg.message_type = MagicMock(value="assistant")
                msg.role = "assistant"
                msg.content = "Task completed successfully"
                yield msg
            
            mock_cli.execute_with_streaming = mock_stream
            mock_cli_class.return_value = mock_cli
            
            result = await server.qwen_subagent(
                instruction=sample_instruction,
                project_path=str(temp_project_dir),
                ctx=mock_context
            )
            
            assert "completed" in result.lower()
            mock_context.report_progress.assert_called()
