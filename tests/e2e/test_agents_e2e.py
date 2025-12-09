"""End-to-end tests for CLI agents via MCP server."""
import pytest
import asyncio
from pathlib import Path


@pytest.mark.e2e
@pytest.mark.asyncio
class TestAgentsE2E:
    """E2E tests for each CLI agent."""

    @pytest.fixture
    def test_project_path(self, tmp_path):
        """Create a temporary project directory."""
        project = tmp_path / "test_project"
        project.mkdir()
        return str(project)

    async def test_codex_simple_task(self, test_project_path):
        """Test Codex agent with simple task."""
        from roundtable_mcp_server.cli_subagent import codex_subagent, check_codex_availability
        
        # Check availability
        availability = await check_codex_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Codex CLI not available")
        
        # Execute simple task
        result = await codex_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None
        assert "error" not in result.lower() or "Error" not in result

    async def test_claude_simple_task(self, test_project_path):
        """Test Claude agent with simple task."""
        from roundtable_mcp_server.cli_subagent import claude_subagent, check_claude_availability
        
        availability = await check_claude_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Claude CLI not available")
        
        result = await claude_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None
        assert "error" not in result.lower() or "Error" not in result

    async def test_gemini_simple_task(self, test_project_path):
        """Test Gemini agent with simple task."""
        from roundtable_mcp_server.cli_subagent import gemini_subagent, check_gemini_availability
        
        availability = await check_gemini_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Gemini CLI not available")
        
        result = await gemini_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None
        assert "error" not in result.lower() or "Error" not in result

    async def test_kiro_simple_task(self, test_project_path):
        """Test Kiro agent with simple task."""
        from roundtable_mcp_server.cli_subagent import kiro_subagent, check_kiro_availability
        
        availability = await check_kiro_availability()
        if "Unavailable" in availability or "not available" in availability or "Error" in availability:
            pytest.skip("Kiro CLI not available")
        
        result = await kiro_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None
        assert "error" not in result.lower() or "Error" not in result

    async def test_qwen_simple_task(self, test_project_path):
        """Test Qwen agent with simple task."""
        from roundtable_mcp_server.cli_subagent import qwen_subagent, check_qwen_availability
        
        availability = await check_qwen_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Qwen CLI not available")
        
        result = await qwen_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None
        assert "error" not in result.lower() or "Error" not in result
