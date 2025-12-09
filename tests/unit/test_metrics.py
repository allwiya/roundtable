"""Unit tests for metrics collection."""
import pytest
import json
from pathlib import Path
from roundtable_mcp_server.metrics import (
    ExecutionMetric,
    MetricsCollector,
    get_metrics_collector
)


@pytest.mark.unit
class TestExecutionMetric:
    """Test ExecutionMetric dataclass."""
    
    def test_create_metric(self):
        """Test creating a metric."""
        metric = ExecutionMetric(
            agent="codex",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.5,
            success=True,
            message_count=10,
            tool_uses=3
        )
        
        assert metric.agent == "codex"
        assert metric.duration_seconds == 1.5
        assert metric.success is True
        assert metric.message_count == 10
        assert metric.tool_uses == 3


@pytest.mark.unit
class TestMetricsCollector:
    """Test MetricsCollector class."""
    
    def test_collector_disabled_by_default(self):
        """Test collector is disabled by default."""
        collector = MetricsCollector()
        
        assert collector.enabled is False
    
    def test_collector_enabled(self, tmp_path):
        """Test collector when enabled."""
        storage = tmp_path / "metrics.jsonl"
        collector = MetricsCollector(enabled=True, storage_path=storage)
        
        assert collector.enabled is True
        assert collector.storage_path == storage
    
    def test_record_metric_disabled(self):
        """Test recording when disabled does nothing."""
        collector = MetricsCollector(enabled=False)
        
        metric = ExecutionMetric(
            agent="test",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.0,
            success=True
        )
        
        collector.record(metric)
        
        assert len(collector.metrics) == 0
    
    def test_record_metric_enabled(self, tmp_path):
        """Test recording when enabled."""
        storage = tmp_path / "metrics.jsonl"
        collector = MetricsCollector(enabled=True, storage_path=storage)
        
        metric = ExecutionMetric(
            agent="codex",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.5,
            success=True
        )
        
        collector.record(metric)
        
        assert len(collector.metrics) == 1
        assert storage.exists()
        
        # Check file content
        with open(storage) as f:
            line = f.readline()
            data = json.loads(line)
            assert data["agent"] == "codex"
            assert data["duration_seconds"] == 1.5
    
    def test_track_execution_success(self, tmp_path):
        """Test tracking successful execution."""
        storage = tmp_path / "metrics.jsonl"
        collector = MetricsCollector(enabled=True, storage_path=storage)
        
        with collector.track_execution("gemini") as metric:
            # Simulate work
            import time
            time.sleep(0.1)
            metric.message_count = 5
        
        assert len(collector.metrics) == 1
        assert collector.metrics[0].agent == "gemini"
        assert collector.metrics[0].success is True
        assert collector.metrics[0].duration_seconds >= 0.1
        assert collector.metrics[0].message_count == 5
    
    def test_track_execution_failure(self, tmp_path):
        """Test tracking failed execution."""
        storage = tmp_path / "metrics.jsonl"
        collector = MetricsCollector(enabled=True, storage_path=storage)
        
        with pytest.raises(ValueError):
            with collector.track_execution("claude"):
                raise ValueError("Test error")
        
        assert len(collector.metrics) == 1
        assert collector.metrics[0].success is False
        assert "Test error" in collector.metrics[0].error
    
    def test_get_stats_empty(self):
        """Test getting stats with no metrics."""
        collector = MetricsCollector(enabled=True)
        
        stats = collector.get_stats()
        
        assert stats == {}
    
    def test_get_stats_with_metrics(self, tmp_path):
        """Test getting aggregated stats."""
        storage = tmp_path / "metrics.jsonl"
        collector = MetricsCollector(enabled=True, storage_path=storage)
        
        # Add some metrics
        collector.record(ExecutionMetric(
            agent="codex",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.0,
            success=True
        ))
        collector.record(ExecutionMetric(
            agent="codex",
            timestamp="2024-01-01T00:01:00",
            duration_seconds=2.0,
            success=False,
            error="Failed"
        ))
        collector.record(ExecutionMetric(
            agent="gemini",
            timestamp="2024-01-01T00:02:00",
            duration_seconds=1.5,
            success=True
        ))
        
        stats = collector.get_stats()
        
        assert stats["total_executions"] == 3
        assert stats["successful"] == 2
        assert stats["failed"] == 1
        assert "codex" in stats["by_agent"]
        assert "gemini" in stats["by_agent"]
        assert stats["by_agent"]["codex"]["count"] == 2
        assert stats["by_agent"]["codex"]["success"] == 1
        assert stats["by_agent"]["codex"]["failed"] == 1
        assert stats["by_agent"]["gemini"]["count"] == 1
    
    def test_export_json(self, tmp_path):
        """Test exporting metrics to JSON."""
        storage = tmp_path / "metrics.jsonl"
        export_path = tmp_path / "export.json"
        collector = MetricsCollector(enabled=True, storage_path=storage)
        
        collector.record(ExecutionMetric(
            agent="qwen",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.0,
            success=True
        ))
        
        collector.export_json(export_path)
        
        assert export_path.exists()
        
        with open(export_path) as f:
            data = json.load(f)
            assert "metrics" in data
            assert "stats" in data
            assert len(data["metrics"]) == 1
            assert data["metrics"][0]["agent"] == "qwen"


@pytest.mark.unit
class TestGetMetricsCollector:
    """Test global metrics collector."""
    
    def test_get_collector_singleton(self):
        """Test collector is singleton."""
        collector1 = get_metrics_collector()
        collector2 = get_metrics_collector()
        
        assert collector1 is collector2
