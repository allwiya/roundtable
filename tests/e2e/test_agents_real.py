"""Real end-to-end tests that validate roundtable opinion functionality."""
import pytest
import asyncio


@pytest.mark.e2e
@pytest.mark.asyncio
class TestAgentsReal:
    """Real e2e tests that verify agents give opinions on proposals."""

    @pytest.fixture
    def test_project_path(self, tmp_path):
        """Create a temporary project directory."""
        project = tmp_path / "test_project"
        project.mkdir()
        return str(project)

    async def test_claude_gives_opinion(self, test_project_path):
        """Test Claude gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import claude_subagent, check_claude_availability
        
        availability = await check_claude_availability()
        if "Unavailable" in availability:
            pytest.skip("Claude not available")
        
        result = await claude_subagent(
            instruction="Review this proposal: Implement user authentication with OAuth2. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Claude should return a response"
        assert len(result) > 10, f"Claude response too short: {result}"

    async def test_gemini_gives_opinion(self, test_project_path):
        """Test Gemini gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import gemini_subagent, check_gemini_availability
        
        availability = await check_gemini_availability()
        if "Unavailable" in availability:
            pytest.skip("Gemini not available")
        
        result = await gemini_subagent(
            instruction="Review this proposal: Use MongoDB for data storage. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Gemini should return a response"
        assert len(result) > 10, f"Gemini response too short: {result}"

    async def test_codex_gives_opinion(self, test_project_path):
        """Test Codex gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import codex_subagent, check_codex_availability
        
        availability = await check_codex_availability()
        if "Unavailable" in availability:
            pytest.skip("Codex not available")
        
        result = await codex_subagent(
            instruction="Review this proposal: Implement caching with Redis. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Codex should return a response"
        assert len(result) > 10, f"Codex response too short: {result}"

    async def test_qwen_gives_opinion(self, test_project_path):
        """Test Qwen gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import qwen_subagent, check_qwen_availability
        
        availability = await check_qwen_availability()
        if "Unavailable" in availability:
            pytest.skip("Qwen not available")
        
        result = await qwen_subagent(
            instruction="Review this proposal: Use TypeScript instead of JavaScript. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Qwen should return a response"
        assert len(result) > 10, f"Qwen response too short: {result}"

    async def test_kiro_gives_opinion(self, test_project_path):
        """Test Kiro gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import kiro_subagent, check_kiro_availability
        
        availability = await check_kiro_availability()
        if "Unavailable" in availability:
            pytest.skip("Kiro not available")
        
        result = await kiro_subagent(
            instruction="Review this proposal: Deploy on AWS Lambda. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Kiro should return a response"
        assert len(result) > 10, f"Kiro response too short: {result}"

    async def test_cursor_gives_opinion(self, test_project_path):
        """Test Cursor gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import cursor_subagent, check_cursor_availability
        
        availability = await check_cursor_availability()
        if "Unavailable" in availability:
            pytest.skip("Cursor not available")
        
        result = await cursor_subagent(
            instruction="Review this proposal: Implement JWT authentication with refresh tokens. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Cursor should return a response"
        assert len(result) > 10, f"Cursor response too short: {result}"

    async def test_copilot_gives_opinion(self, test_project_path):
        """Test Copilot gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import copilot_subagent, check_copilot_availability
        
        availability = await check_copilot_availability()
        if "Unavailable" in availability:
            pytest.skip("Copilot not available")
        
        result = await copilot_subagent(
            instruction="Review this proposal: Use Redis for session storage. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Copilot should return a response"
        assert len(result) > 10, f"Copilot response too short: {result}"

    async def test_grok_gives_opinion(self, test_project_path):
        """Test Grok gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import grok_subagent, check_grok_availability
        
        availability = await check_grok_availability()
        if "Unavailable" in availability:
            pytest.skip("Grok not available")
        
        result = await grok_subagent(
            instruction="Review this proposal: Implement rate limiting with 100 requests per minute. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Grok should return a response"
        assert len(result) > 10, f"Grok response too short: {result}"

    async def test_kilocode_gives_opinion(self, test_project_path):
        """Test Kilocode gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import kilocode_subagent, check_kilocode_availability
        
        availability = await check_kilocode_availability()
        if "Unavailable" in availability:
            pytest.skip("Kilocode not available")
        
        result = await kilocode_subagent(
            instruction="Review this proposal: Use PostgreSQL with connection pooling. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Kilocode should return a response"
        assert len(result) > 10, f"Kilocode response too short: {result}"

    async def test_crush_gives_opinion(self, test_project_path):
        """Test Crush gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import crush_subagent, check_crush_availability
        
        availability = await check_crush_availability()
        if "Unavailable" in availability:
            pytest.skip("Crush not available")
        
        result = await crush_subagent(
            instruction="Review this proposal: Implement microservices architecture. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Crush should return a response"
        assert len(result) > 10, f"Crush response too short: {result}"

    async def test_opencode_gives_opinion(self, test_project_path):
        """Test OpenCode gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import opencode_subagent, check_opencode_availability
        
        availability = await check_opencode_availability()
        if "Unavailable" in availability:
            pytest.skip("OpenCode not available")
        
        result = await opencode_subagent(
            instruction="Review this proposal: Use Docker containers for deployment. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "OpenCode should return a response"
        assert len(result) > 10, f"OpenCode response too short: {result}"

    async def test_factory_gives_opinion(self, test_project_path):
        """Test Factory gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import factory_subagent, check_factory_availability
        
        availability = await check_factory_availability()
        if "Unavailable" in availability or "not enabled" in availability:
            pytest.skip("Factory not available")
        
        result = await factory_subagent(
            instruction="Review this proposal: Implement GraphQL API instead of REST. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Factory should return a response"
        assert len(result) > 10, f"Factory response too short: {result}"

    async def test_rovo_gives_opinion(self, test_project_path):
        """Test Rovo gives opinion on a proposal."""
        from roundtable_mcp_server.cli_subagent import rovo_subagent, check_rovo_availability
        
        availability = await check_rovo_availability()
        if "Unavailable" in availability:
            pytest.skip("Rovo not available")
        
        result = await rovo_subagent(
            instruction="Review this proposal: Use WebSockets for real-time updates. What's your opinion?",
            project_path=test_project_path
        )
        
        assert result, "Rovo should return a response"
        assert len(result) > 10, f"Rovo response too short: {result}"
