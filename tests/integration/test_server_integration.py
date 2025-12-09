"""Integration tests for MCP server."""
import pytest
from unittest.mock import patch, MagicMock
from roundtable_mcp_server import server


@pytest.mark.integration
class TestServerIntegration:
    """Test server integration."""
    
    def test_server_initialization(self):
        """Test server can be initialized."""
        assert server.server is not None
        assert server.server.name == "roundtable-ai"
    
    def test_config_initialization(self):
        """Test configuration initialization."""
        with patch.dict('os.environ', {'CLI_MCP_SUBAGENTS': 'codex,qwen'}):
            server.initialize_config()
            
            assert server.config is not None
            assert "codex" in server.enabled_subagents
            assert "qwen" in server.enabled_subagents
    
    @pytest.mark.asyncio
    async def test_all_tools_registered(self):
        """Test all expected tools are registered."""
        # Get registered tools from server - FastMCP uses async list_tools()
        tools_list = await server.server.list_tools()
        tool_names = [tool.name for tool in tools_list]
        
        # Check availability tools
        assert "check_codex_availability" in tool_names
        assert "check_claude_availability" in tool_names
        assert "check_cursor_availability" in tool_names
        assert "check_gemini_availability" in tool_names
        assert "check_qwen_availability" in tool_names
        
        # Check subagent tools
        assert "codex_subagent" in tool_names
        assert "claude_subagent" in tool_names
        assert "cursor_subagent" in tool_names
        assert "gemini_subagent" in tool_names
        assert "qwen_subagent" in tool_names
    
    @pytest.mark.asyncio
    async def test_tool_count(self):
        """Test correct number of tools registered."""
        tools_list = await server.server.list_tools()
        
        # Should have 10 main tools + test_tool
        assert len(tools_list) >= 10


@pytest.mark.integration
@pytest.mark.slow
class TestEndToEndFlow:
    """Test end-to-end execution flow."""
    
    @pytest.mark.asyncio
    async def test_availability_check_flow(self):
        """Test availability check flow."""
        server.enabled_subagents = {"codex"}
        
        with patch('roundtable_mcp_server.server._import_module_item') as mock_import:
            mock_check = MagicMock()
            mock_check.return_value = "✅ Available"
            mock_import.return_value = mock_check
            
            # This would be called by MCP client
            result = await server.check_codex_availability()
            
            assert result is not None
