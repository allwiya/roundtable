"""Pytest configuration and shared fixtures."""
import asyncio
import os
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Dict, Any
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config():
    """Mock ServerConfig."""
    from roundtable_mcp_server.server import ServerConfig
    
    config = ServerConfig()
    config.subagents = ["codex", "claude", "cursor", "gemini", "qwen"]
    config.debug = True
    config.verbose = False
    return config


@pytest.fixture
def mock_context():
    """Mock MCP Context."""
    context = MagicMock()
    context.report_progress = AsyncMock()
    context.error = AsyncMock()
    context.debug = AsyncMock()
    return context


@pytest.fixture
def mock_availability_success():
    """Mock successful availability check."""
    return {
        "available": True,
        "version": "1.0.0",
        "path": "/usr/bin/mock-cli"
    }


@pytest.fixture
def mock_availability_failure():
    """Mock failed availability check."""
    return {
        "available": False,
        "error": "CLI not found"
    }


@pytest.fixture
def sample_instruction():
    """Sample instruction for testing."""
    return "Create a simple hello world function in Python"


@pytest.fixture
def mock_message():
    """Mock Message object."""
    from claudable_helper.models.messages import Message, MessageType
    
    message = MagicMock()
    message.message_type = MessageType.ASSISTANT
    message.role = "assistant"
    message.content = "Test response"
    return message


@pytest.fixture
async def mock_streaming_messages():
    """Mock streaming messages generator."""
    from claudable_helper.models.messages import Message, MessageType
    
    messages = [
        MagicMock(message_type=MessageType.ASSISTANT, role="assistant", content="Starting task"),
        MagicMock(message_type=MessageType.TOOL_USE, content="read_file: test.py"),
        MagicMock(message_type=MessageType.TOOL_RESULT, content="File content"),
        MagicMock(message_type=MessageType.ASSISTANT, role="assistant", content="Task completed"),
    ]
    
    async def generator():
        for msg in messages:
            yield msg
    
    return generator()


@pytest.fixture(autouse=True)
def reset_env_vars():
    """Reset environment variables before each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_cli_adapter():
    """Mock CLI adapter base class."""
    adapter = MagicMock()
    adapter.check_availability = AsyncMock(return_value={"available": True})
    adapter.execute_with_streaming = AsyncMock()
    return adapter
