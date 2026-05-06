#!/usr/bin/env python3
"""Download a small GPT4All model for testing on 6GB VRAM."""
import os
import sys
from pathlib import Path

model_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/models/gpt4all")
model_dir.mkdir(parents=True, exist_ok=True)

# Small model that can run on 6GB VRAM: Orca Mini 3B quantized
# This is ~2GB download
model_url = "https://huggingface.co/TheBloke/Orca-Mini-3B-GGUF/resolve/main/orca-mini-3b.q4_0.gguf"
model_name = "orca-mini-3b.q4_0.gguf"
model_path = model_dir / model_name

if model_path.exists():
    print(f"Model already exists: {model_path}")
    sys.exit(0)

print(f"Downloading {model_name} (~2GB)...")
print(f"URL: {model_url}")
print(f"Destination: {model_path}")

try:
    import urllib.request
    import time
    
    def report_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, downloaded * 100 / total_size) if total_size > 0 else 0
        if block_num % 10 == 0:
            print(f"  Downloaded: {downloaded//1024//1024:.1f}MB / {total_size//1024//1024:.1f}MB ({percent:.1f}%)")
    
    urllib.request.urlretrieve(model_url, str(model_path), reporthook=report_hook)
    print(f"SUCCESS: Model downloaded to {model_path}")
    print(f"Size: {model_path.stat().st_size // 1024 // 1024}MB")
    
except Exception as e:
    print(f"FAILED: {e}")
    print("Alternative: User can manually download model to:", model_dir)
    print("Recommended: Orca Mini 3B Q4_0 or similar small model")
    sys.exit(1)
