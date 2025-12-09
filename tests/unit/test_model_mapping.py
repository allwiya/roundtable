"""Unit tests for model mapping."""
import pytest
from claudable_helper.cli.base import MODEL_MAPPING, CLIType


@pytest.mark.unit
class TestModelMapping:
    """Test model mapping configuration."""
    
    def test_claude_model_mapping(self):
        """Test Claude model mappings."""
        assert "claude" in MODEL_MAPPING
        
        claude_models = MODEL_MAPPING["claude"]
        assert "opus-4.1" in claude_models
        assert "sonnet-4" in claude_models
        assert claude_models["opus-4.1"] == "claude-opus-4-1-20250805"
    
    def test_cursor_model_mapping(self):
        """Test Cursor model mappings."""
        assert "cursor" in MODEL_MAPPING
        
        cursor_models = MODEL_MAPPING["cursor"]
        assert "gpt-5" in cursor_models
        assert "sonnet-4" in cursor_models
    
    def test_codex_model_mapping(self):
        """Test Codex model mappings."""
        assert "codex" in MODEL_MAPPING
        
        codex_models = MODEL_MAPPING["codex"]
        assert "gpt-5" in codex_models
        assert "gpt-4o" in codex_models
    
    def test_gemini_model_mapping(self):
        """Test Gemini model mappings."""
        assert "gemini" in MODEL_MAPPING
        
        gemini_models = MODEL_MAPPING["gemini"]
        assert "gemini-2.5-pro" in gemini_models
        assert "gemini-2.5-flash" in gemini_models
    
    def test_qwen_model_mapping(self):
        """Test Qwen model mappings."""
        assert "qwen" in MODEL_MAPPING
        
        qwen_models = MODEL_MAPPING["qwen"]
        assert "qwen-coder" in qwen_models
        assert qwen_models["qwen-coder"] == "qwen-coder"
    
    def test_cli_types(self):
        """Test CLIType enum."""
        assert CLIType.CLAUDE == "claude"
        assert CLIType.CURSOR == "cursor"
        assert CLIType.CODEX == "codex"
        assert CLIType.GEMINI == "gemini"
        assert CLIType.QWEN == "qwen"
