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

    async def test_cursor_simple_task(self, test_project_path):
        """Test Cursor agent with simple task."""
        from roundtable_mcp_server.cli_subagent import cursor_subagent, check_cursor_availability
        
        availability = await check_cursor_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Cursor CLI not available")
        
        result = await cursor_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_copilot_simple_task(self, test_project_path):
        """Test Copilot agent with simple task."""
        from roundtable_mcp_server.cli_subagent import copilot_subagent, check_copilot_availability
        
        availability = await check_copilot_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Copilot CLI not available")
        
        result = await copilot_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_grok_simple_task(self, test_project_path):
        """Test Grok agent with simple task."""
        from roundtable_mcp_server.cli_subagent import grok_subagent, check_grok_availability
        
        availability = await check_grok_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Grok CLI not available")
        
        result = await grok_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_kilocode_simple_task(self, test_project_path):
        """Test Kilocode agent with simple task."""
        from roundtable_mcp_server.cli_subagent import kilocode_subagent, check_kilocode_availability
        
        availability = await check_kilocode_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Kilocode CLI not available")
        
        result = await kilocode_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_crush_simple_task(self, test_project_path):
        """Test Crush agent with simple task."""
        from roundtable_mcp_server.cli_subagent import crush_subagent, check_crush_availability
        
        availability = await check_crush_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Crush CLI not available")
        
        result = await crush_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_opencode_simple_task(self, test_project_path):
        """Test OpenCode agent with simple task."""
        from roundtable_mcp_server.cli_subagent import opencode_subagent, check_opencode_availability
        
        availability = await check_opencode_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("OpenCode CLI not available")
        
        result = await opencode_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_factory_simple_task(self, test_project_path):
        """Test Factory agent with simple task."""
        from roundtable_mcp_server.cli_subagent import factory_subagent, check_factory_availability
        
        availability = await check_factory_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Factory CLI not available")
        
        result = await factory_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None

    async def test_rovo_simple_task(self, test_project_path):
        """Test Rovo agent with simple task."""
        from roundtable_mcp_server.cli_subagent import rovo_subagent, check_rovo_availability
        
        availability = await check_rovo_availability()
        if "Unavailable" in availability or "not available" in availability:
            pytest.skip("Rovo CLI not available")
        
        result = await rovo_subagent(
            instruction="Create a file called test.txt with content 'Hello World'",
            project_path=test_project_path
        )
        
        assert result is not None
