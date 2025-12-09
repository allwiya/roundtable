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

    async def test_cursor_creates_file(self, test_project_path):
        """Test Cursor actually creates a file."""
        from roundtable_mcp_server.cli_subagent import cursor_subagent, check_cursor_availability
        
        availability = await check_cursor_availability()
        if "Unavailable" in availability:
            pytest.skip("Cursor not available")
        
        result = await cursor_subagent(
            instruction="Create a Python file called modulo.py with a function that calculates 10 % 3 and prints the result",
            project_path=test_project_path
        )
        
        modulo_file = Path(test_project_path) / "modulo.py"
        assert modulo_file.exists(), f"Cursor failed to create modulo.py. Result: {result}"

    async def test_copilot_creates_file(self, test_project_path):
        """Test Copilot actually creates a file."""
        from roundtable_mcp_server.cli_subagent import copilot_subagent, check_copilot_availability
        
        availability = await check_copilot_availability()
        if "Unavailable" in availability:
            pytest.skip("Copilot not available")
        
        result = await copilot_subagent(
            instruction="Create a Python file called floor.py with a function that calculates 7 // 2 and prints the result",
            project_path=test_project_path
        )
        
        floor_file = Path(test_project_path) / "floor.py"
        assert floor_file.exists(), f"Copilot failed to create floor.py. Result: {result}"

    async def test_grok_creates_file(self, test_project_path):
        """Test Grok actually creates a file."""
        from roundtable_mcp_server.cli_subagent import grok_subagent, check_grok_availability
        
        availability = await check_grok_availability()
        if "Unavailable" in availability:
            pytest.skip("Grok not available")
        
        result = await grok_subagent(
            instruction="Create a Python file called max_num.py with a function that finds max of 5 and 9 and prints the result",
            project_path=test_project_path
        )
        
        max_file = Path(test_project_path) / "max_num.py"
        assert max_file.exists(), f"Grok failed to create max_num.py. Result: {result}"

    async def test_kilocode_creates_file(self, test_project_path):
        """Test Kilocode actually creates a file."""
        from roundtable_mcp_server.cli_subagent import kilocode_subagent, check_kilocode_availability
        
        availability = await check_kilocode_availability()
        if "Unavailable" in availability:
            pytest.skip("Kilocode not available")
        
        result = await kilocode_subagent(
            instruction="Create a Python file called min_num.py with a function that finds min of 3 and 7 and prints the result",
            project_path=test_project_path
        )
        
        min_file = Path(test_project_path) / "min_num.py"
        assert min_file.exists(), f"Kilocode failed to create min_num.py. Result: {result}"

    async def test_crush_creates_file(self, test_project_path):
        """Test Crush actually creates a file."""
        from roundtable_mcp_server.cli_subagent import crush_subagent, check_crush_availability
        
        availability = await check_crush_availability()
        if "Unavailable" in availability:
            pytest.skip("Crush not available")
        
        result = await crush_subagent(
            instruction="Create a Python file called abs_val.py with a function that calculates abs(-5) and prints the result",
            project_path=test_project_path
        )
        
        abs_file = Path(test_project_path) / "abs_val.py"
        assert abs_file.exists(), f"Crush failed to create abs_val.py. Result: {result}"

    async def test_opencode_creates_file(self, test_project_path):
        """Test OpenCode actually creates a file."""
        from roundtable_mcp_server.cli_subagent import opencode_subagent, check_opencode_availability
        
        availability = await check_opencode_availability()
        if "Unavailable" in availability:
            pytest.skip("OpenCode not available")
        
        result = await opencode_subagent(
            instruction="Create a Python file called round_num.py with a function that rounds 3.7 and prints the result",
            project_path=test_project_path
        )
        
        round_file = Path(test_project_path) / "round_num.py"
        assert round_file.exists(), f"OpenCode failed to create round_num.py. Result: {result}"

    async def test_factory_creates_file(self, test_project_path):
        """Test Factory actually creates a file."""
        from roundtable_mcp_server.cli_subagent import factory_subagent, check_factory_availability
        
        availability = await check_factory_availability()
        if "Unavailable" in availability or "not enabled" in availability:
            pytest.skip("Factory not available")
        
        result = await factory_subagent(
            instruction="Create a Python file called len_str.py with a function that calculates len('hello') and prints the result",
            project_path=test_project_path
        )
        
        len_file = Path(test_project_path) / "len_str.py"
        assert len_file.exists(), f"Factory failed to create len_str.py. Result: {result}"

    async def test_rovo_creates_file(self, test_project_path):
        """Test Rovo actually creates a file."""
        from roundtable_mcp_server.cli_subagent import rovo_subagent, check_rovo_availability
        
        availability = await check_rovo_availability()
        if "Unavailable" in availability:
            pytest.skip("Rovo not available")
        
        result = await rovo_subagent(
            instruction="Create a Python file called upper_str.py with a function that converts 'hello' to uppercase and prints the result",
            project_path=test_project_path
        )
        
        upper_file = Path(test_project_path) / "upper_str.py"
        assert upper_file.exists(), f"Rovo failed to create upper_str.py. Result: {result}"
