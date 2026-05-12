import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.wangp_adapter import WanGPAdapter


def test_vram_hardware_integration():
    adapter = WanGPAdapter(wangp_path="/fake/path")
    with patch("app.hardware.get_gpu_info", return_value={"vram_gb": 8.0}):
        vram = adapter._get_vram_gb()
        assert vram == 8


def test_vram_hardware_rounds_down():
    adapter = WanGPAdapter(wangp_path="/fake/path")
    with patch("app.hardware.get_gpu_info", return_value={"vram_gb": 6.44}):
        vram = adapter._get_vram_gb()
        assert vram == 6


def test_vram_fallback_on_error():
    adapter = WanGPAdapter(wangp_path="/fake/path")
    with patch("app.hardware.get_gpu_info", side_effect=Exception("no GPU")):
        vram = adapter._get_vram_gb()
        assert vram == 6


def test_vram_minimum_one():
    adapter = WanGPAdapter(wangp_path="/fake/path")
    with patch("app.hardware.get_gpu_info", return_value={"vram_gb": 0.5}):
        vram = adapter._get_vram_gb()
        assert vram == 1


def test_vram_missing_key():
    adapter = WanGPAdapter(wangp_path="/fake/path")
    with patch("app.hardware.get_gpu_info", return_value={"name": "unknown"}):
        vram = adapter._get_vram_gb()
        assert vram == 6
