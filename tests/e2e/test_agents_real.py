"""Real end-to-end tests that validate actual agent functionality."""
import pytest
import asyncio
from pathlib import Path


@pytest.mark.e2e
@pytest.mark.asyncio
class TestAgentsReal:
    """Real e2e tests that verify agents complete tasks correctly."""

    @pytest.fixture
    def test_project_path(self, tmp_path):
        """Create a temporary project directory."""
        project = tmp_path / "test_project"
        project.mkdir()
        return str(project)

    async def test_codex_creates_file(self, test_project_path):
        """Test Codex actually creates a file."""
        from roundtable_mcp_server.cli_subagent import codex_subagent, check_codex_availability
        
        availability = await check_codex_availability()
        if "Unavailable" in availability:
            pytest.skip("Codex not available")
        
        result = await codex_subagent(
            instruction="Create a Python file called sum.py with a function that adds 5 + 3 and prints the result",
            project_path=test_project_path
        )
        
        # Verify file was created
        sum_file = Path(test_project_path) / "sum.py"
        assert sum_file.exists(), f"Codex failed to create sum.py. Result: {result}"
        
        # Verify file has content
        content = sum_file.read_text()
        assert len(content) > 0, "sum.py is empty"
        assert "5" in content or "3" in content or "8" in content, "sum.py doesn't contain expected numbers"

    async def test_claude_creates_file(self, test_project_path):
        """Test Claude actually creates a file."""
        from roundtable_mcp_server.cli_subagent import claude_subagent, check_claude_availability
        
        availability = await check_claude_availability()
        if "Unavailable" in availability:
            pytest.skip("Claude not available")
        
        result = await claude_subagent(
            instruction="Create a Python file called multiply.py with a function that multiplies 4 * 6 and prints the result",
            project_path=test_project_path
        )
        
        multiply_file = Path(test_project_path) / "multiply.py"
        assert multiply_file.exists(), f"Claude failed to create multiply.py. Result: {result}"
        
        content = multiply_file.read_text()
        assert len(content) > 0, "multiply.py is empty"
        assert "4" in content or "6" in content or "24" in content, "multiply.py doesn't contain expected numbers"

    async def test_gemini_creates_file(self, test_project_path):
        """Test Gemini actually creates a file."""
        from roundtable_mcp_server.cli_subagent import gemini_subagent, check_gemini_availability
        
        availability = await check_gemini_availability()
        if "Unavailable" in availability:
            pytest.skip("Gemini not available")
        
        result = await gemini_subagent(
            instruction="Create a Python file called subtract.py with a function that subtracts 10 - 3 and prints the result",
            project_path=test_project_path
        )
        
        subtract_file = Path(test_project_path) / "subtract.py"
        assert subtract_file.exists(), f"Gemini failed to create subtract.py. Result: {result}"
        
        content = subtract_file.read_text()
        assert len(content) > 0, "subtract.py is empty"

    async def test_kiro_creates_file(self, test_project_path):
        """Test Kiro actually creates a file."""
        from roundtable_mcp_server.cli_subagent import kiro_subagent, check_kiro_availability
        
        availability = await check_kiro_availability()
        if "Unavailable" in availability or "Error" in availability:
            pytest.skip("Kiro not available")
        
        result = await kiro_subagent(
            instruction="Create a Python file called divide.py with a function that divides 20 / 4 and prints the result",
            project_path=test_project_path
        )
        
        divide_file = Path(test_project_path) / "divide.py"
        assert divide_file.exists(), f"Kiro failed to create divide.py. Result: {result}"
        
        content = divide_file.read_text()
        assert len(content) > 0, "divide.py is empty"

    async def test_qwen_creates_file(self, test_project_path):
        """Test Qwen actually creates a file."""
        from roundtable_mcp_server.cli_subagent import qwen_subagent, check_qwen_availability
        
        availability = await check_qwen_availability()
        if "Unavailable" in availability:
            pytest.skip("Qwen not available")
        
        result = await qwen_subagent(
            instruction="Create a Python file called power.py with a function that calculates 2 ** 3 and prints the result",
            project_path=test_project_path
        )
        
        power_file = Path(test_project_path) / "power.py"
        assert power_file.exists(), f"Qwen failed to create power.py. Result: {result}"
        
        content = power_file.read_text()
        assert len(content) > 0, "power.py is empty"
