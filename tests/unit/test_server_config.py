"""Unit tests for server configuration."""
import os
import pytest
from roundtable_mcp_server.server import ServerConfig, parse_config_from_env


@pytest.mark.unit
class TestServerConfig:
    """Test ServerConfig model."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ServerConfig()
        
        assert config.subagents == ["codex", "claude", "cursor", "gemini", "qwen", "kiro", "copilot", "grok", "kilocode", "crush", "opencode", "antigravity"]
        assert config.working_dir is None
        assert config.debug is True
        assert config.verbose is False
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = ServerConfig(
            subagents=["codex", "qwen"],
            working_dir="/tmp/test",
            debug=False,
            verbose=True
        )
        
        assert config.subagents == ["codex", "qwen"]
        assert config.working_dir == "/tmp/test"
        assert config.debug is False
        assert config.verbose is True


@pytest.mark.unit
class TestParseConfigFromEnv:
    """Test environment variable parsing."""
    
    def test_parse_with_env_subagents(self):
        """Test parsing with CLI_MCP_SUBAGENTS set."""
        os.environ["CLI_MCP_SUBAGENTS"] = "codex,gemini"
        
        config = parse_config_from_env()
        
        assert "codex" in config.subagents
        assert "gemini" in config.subagents
        assert len(config.subagents) == 2
    
    def test_parse_with_invalid_subagents(self):
        """Test parsing with invalid subagent names."""
        os.environ["CLI_MCP_SUBAGENTS"] = "codex,invalid,gemini"
        
        config = parse_config_from_env()
        
        assert "codex" in config.subagents
        assert "gemini" in config.subagents
        assert "invalid" not in config.subagents
    
    def test_parse_with_working_dir(self):
        """Test parsing with working directory."""
        os.environ["CLI_MCP_WORKING_DIR"] = "/tmp/test"
        
        config = parse_config_from_env()
        
        assert config.working_dir == "/tmp/test"
    
    def test_parse_with_debug_flag(self):
        """Test parsing debug flag."""
        os.environ["CLI_MCP_DEBUG"] = "false"
        
        config = parse_config_from_env()
        
        assert config.debug is False
    
    def test_parse_with_verbose_flag(self):
        """Test parsing verbose flag."""
        os.environ["CLI_MCP_SUBAGENTS"] = "codex"
        os.environ["CLI_MCP_VERBOSE"] = "true"
        
        config = parse_config_from_env()
        
        assert config.verbose is True
    
    def test_parse_ignore_availability(self):
        """Test ignore availability flag."""
        os.environ["CLI_MCP_IGNORE_AVAILABILITY"] = "true"
        
        config = parse_config_from_env()
        
        # Should enable all subagents
        assert len(config.subagents) == 5
        assert "qwen" in config.subagents
