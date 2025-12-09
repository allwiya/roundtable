"""Unit tests for error handler utilities."""
import pytest
from pathlib import Path
from roundtable_mcp_server.error_handler import (
    validate_project_path,
    format_error_response,
    log_error_with_context
)
from roundtable_mcp_server.exceptions import (
    PathValidationError,
    AgentExecutionError,
    RoundtableError
)


@pytest.mark.unit
class TestValidateProjectPath:
    """Test path validation."""
    
    def test_validate_with_valid_path(self, temp_project_dir):
        """Test validation with valid path."""
        result = validate_project_path(
            str(temp_project_dir),
            Path.cwd(),
            "test-agent"
        )
        
        assert result == str(temp_project_dir.absolute())
    
    def test_validate_with_none_path(self, temp_project_dir):
        """Test validation with None path uses fallback."""
        result = validate_project_path(
            None,
            temp_project_dir,
            "test-agent"
        )
        
        assert result == str(temp_project_dir.absolute())
    
    def test_validate_with_empty_path(self, temp_project_dir):
        """Test validation with empty path uses fallback."""
        result = validate_project_path(
            "",
            temp_project_dir,
            "test-agent"
        )
        
        assert result == str(temp_project_dir.absolute())
    
    def test_validate_with_nonexistent_path(self):
        """Test validation with nonexistent path raises error."""
        with pytest.raises(PathValidationError) as exc_info:
            validate_project_path(
                "/nonexistent/path",
                Path.cwd(),
                "test-agent"
            )
        
        assert "does not exist" in str(exc_info.value).lower()
        assert exc_info.value.context["agent"] == "test-agent"
    
    def test_validate_with_file_path(self, tmp_path):
        """Test validation with file path raises error."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test")
        
        with pytest.raises(PathValidationError) as exc_info:
            validate_project_path(
                str(file_path),
                Path.cwd(),
                "test-agent"
            )
        
        assert "not a directory" in str(exc_info.value).lower()


@pytest.mark.unit
class TestFormatErrorResponse:
    """Test error response formatting."""
    
    def test_format_custom_exception(self):
        """Test formatting custom exception."""
        error = AgentExecutionError("codex", "Process failed")
        
        result = format_error_response(error, include_context=True)
        
        assert "❌" in result
        assert "codex" in result
        assert "Process failed" in result
    
    def test_format_custom_exception_with_context(self):
        """Test formatting with context."""
        error = RoundtableError(
            "Test error",
            "TEST_CODE",
            {"key": "value", "number": 42}
        )
        
        result = format_error_response(error, include_context=True)
        
        assert "❌" in result
        assert "Test error" in result
        assert "key=value" in result or "number=42" in result
    
    def test_format_generic_exception(self):
        """Test formatting generic exception."""
        error = ValueError("Invalid value")
        
        result = format_error_response(error, agent_name="test-agent")
        
        assert "❌" in result
        assert "test-agent" in result
        assert "ValueError" in result
        assert "Invalid value" in result
    
    def test_format_without_context(self):
        """Test formatting without context."""
        error = RoundtableError("Test", "CODE", {"hidden": "data"})
        
        result = format_error_response(error, include_context=False)
        
        assert "❌" in result
        assert "Test" in result
        assert "hidden" not in result


@pytest.mark.unit
class TestLogErrorWithContext:
    """Test error logging with context."""
    
    def test_log_custom_error(self, caplog):
        """Test logging custom error."""
        error = AgentExecutionError("codex", "Failed")
        
        log_error_with_context(
            error,
            "execute_task",
            {"session": "123"}
        )
        
        assert "execute_task" in caplog.text
        assert "AGENT_EXECUTION_ERROR" in caplog.text
    
    def test_log_generic_error(self, caplog):
        """Test logging generic error."""
        error = RuntimeError("Something broke")
        
        log_error_with_context(
            error,
            "test_operation",
            {"detail": "info"}
        )
        
        assert "test_operation" in caplog.text
        assert "RuntimeError" in caplog.text
