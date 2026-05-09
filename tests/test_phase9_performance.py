import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_metrics_service_import():
    from app.services.metrics_service import MetricsService
    assert MetricsService is not None
    print('[OK] MetricsService imported')

def test_timeout_retry_import():
    from app.utils.timeout_retry import TimeoutRetry
    assert TimeoutRetry is not None
    print('[OK] TimeoutRetry imported')

def test_metrics_basic():
    from app.services.metrics_service import MetricsService
    m = MetricsService()
    data = m._load_data()
    data['pipeline_runs'] = 1
    m._save_data(data)
    loaded = m._load_data()
    assert loaded['pipeline_runs'] == 1
    print('[OK] Metrics basic')

def test_vram():
    from app.hardware import get_recommended_preset
    preset = get_recommended_preset(6, "Test GPU")
    assert preset is not None
    print('[OK] VRAM estimate')

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
