"""Unit tests for error handling."""
import pytest
import asyncio
from roundtable_mcp_server.exceptions import (
    RoundtableError,
    ConfigurationError,
    AgentNotAvailableError,
    AgentExecutionError,
    StreamingError,
    PathValidationError,
    TimeoutError,
    RetryableError
)
from roundtable_mcp_server.retry import retry_async, retry_sync


@pytest.mark.unit
class TestExceptions:
    """Test custom exceptions."""
    
    def test_base_exception(self):
        """Test base RoundtableError."""
        error = RoundtableError("Test error", "TEST_CODE", {"key": "value"})
        
        assert str(error) == "[TEST_CODE] Test error"
        assert error.error_code == "TEST_CODE"
        assert error.context == {"key": "value"}
    
    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Invalid config")
        
        assert error.error_code == "CONFIG_ERROR"
        assert "Invalid config" in str(error)
    
    def test_agent_not_available_error(self):
        """Test AgentNotAvailableError."""
        error = AgentNotAvailableError("codex", "CLI not found")
        
        assert error.error_code == "AGENT_NOT_AVAILABLE"
        assert "codex" in str(error)
        assert "CLI not found" in str(error)
        assert error.context["agent"] == "codex"
    
    def test_agent_execution_error(self):
        """Test AgentExecutionError."""
        error = AgentExecutionError("gemini", "Process crashed")
        
        assert error.error_code == "AGENT_EXECUTION_ERROR"
        assert "gemini" in str(error)
        assert "Process crashed" in str(error)
    
    def test_streaming_error(self):
        """Test StreamingError."""
        error = StreamingError("Stream interrupted")
        
        assert error.error_code == "STREAMING_ERROR"
        assert "Stream interrupted" in str(error)
    
    def test_path_validation_error(self):
        """Test PathValidationError."""
        error = PathValidationError("/invalid/path", "Does not exist")
        
        assert error.error_code == "PATH_ERROR"
        assert "/invalid/path" in str(error)
        assert error.context["path"] == "/invalid/path"
    
    def test_timeout_error(self):
        """Test TimeoutError."""
        error = TimeoutError("execute", 30)
        
        assert error.error_code == "TIMEOUT_ERROR"
        assert "execute" in str(error)
        assert "30" in str(error)
    
    def test_retryable_error(self):
        """Test RetryableError."""
        error = RetryableError("Temporary failure")
        
        assert error.error_code == "RETRYABLE"
        assert "Temporary failure" in str(error)


@pytest.mark.unit
@pytest.mark.asyncio
class TestRetryAsync:
    """Test async retry decorator."""
    
    async def test_retry_success_first_attempt(self):
        """Test successful execution on first attempt."""
        call_count = 0
        
        @retry_async(max_attempts=3)
        async def success_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = await success_func()
        
        assert result == "success"
        assert call_count == 1
    
    async def test_retry_success_after_failures(self):
        """Test successful execution after retries."""
        call_count = 0
        
        @retry_async(max_attempts=3, delay=0.1)
        async def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RetryableError("Temporary failure")
            return "success"
        
        result = await flaky_func()
        
        assert result == "success"
        assert call_count == 3
    
    async def test_retry_all_attempts_fail(self):
        """Test all retry attempts fail."""
        call_count = 0
        
        @retry_async(max_attempts=3, delay=0.1)
        async def always_fail():
            nonlocal call_count
            call_count += 1
            raise RetryableError("Always fails")
        
        with pytest.raises(RetryableError):
            await always_fail()
        
        assert call_count == 3
    
    async def test_retry_non_retryable_error(self):
        """Test non-retryable error fails immediately."""
        call_count = 0
        
        @retry_async(max_attempts=3, exceptions=(RetryableError,))
        async def non_retryable():
            nonlocal call_count
            call_count += 1
            raise ValueError("Not retryable")
        
        with pytest.raises(ValueError):
            await non_retryable()
        
        assert call_count == 1


@pytest.mark.unit
class TestRetrySync:
    """Test sync retry decorator."""
    
    def test_retry_sync_success(self):
        """Test sync retry success."""
        call_count = 0
        
        @retry_sync(max_attempts=3, delay=0.1)
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RetryableError("Temporary")
            return "success"
        
        result = flaky_func()
        
        assert result == "success"
        assert call_count == 2
    
    def test_retry_sync_all_fail(self):
        """Test sync retry all attempts fail."""
        call_count = 0
        
        @retry_sync(max_attempts=2, delay=0.1)
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise RetryableError("Always fails")
        
        with pytest.raises(RetryableError):
            always_fail()
        
        assert call_count == 2
