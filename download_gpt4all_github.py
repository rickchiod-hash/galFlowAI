#!/usr/bin/env python3
"""Download GPT4All model from GitHub Releases (public access)."""
import sys
import os
from pathlib import Path

# Config
filename = "orca-mini-3b.q4_0.gguf"
# Using Nomic AI's official releases
url = "https://github.com/nomic-ai/gpt4all/releases/download/v1.3/orca-mini-3b.q4_0.gguf"
model_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/models/gpt4all")
dest = model_dir / filename
model_dir.mkdir(parents=True, exist_ok=True)

# Check if already exists
if dest.exists():
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(f"Model already exists: {dest}")
    print(f"   Size: {size_mb:.1f} MB")
    sys.exit(0)

print(f"Downloading: {filename} (~2GB)")
print(f"From: {url}")
print(f"To: {dest}")
print()
print("Progress:")
print("-" * 60)

try:
    import urllib.request
    
    # Progress hook
    downloaded = [0]
    total_size = None
    
    def report_hook(block_num, block_size, total):
        if total_size is None:
            total_size = total
        downloaded[0] = block_num * block_size
        percent = min(100, (downloaded[0] / total) * 100) if total > 0 else 0
        mb_down = downloaded[0] / (1024 * 1024)
        mb_total = total / (1024 * 1024) if total > 0 else 0
        
        # Visual bar
        bar_width = 50
        filled = int(bar_width * (percent / 100))
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
        
        print(f"\r{bar} {percent:.1f}% ({mb_down:.1f}MB / {mb_total:.1f}MB)", end="", flush=True)
    
    urllib.request.urlretrieve(url, str(dest), reporthook=report_hook)
    
    print(f"\n\nSUCCESS: Model downloaded!")
    final_mb = dest.stat().st_size / (1024 * 1024)
    print(f"   Path: {dest}")
    print(f"   Size: {final_mb:.1f} MB")
    sys.exit(0)
    
except Exception as e:
    print(f"\n\nFAILED: {e}")
    print("\nAlternative: Manual download")
    print(f"1. Go to: https://github.com/nomic-ai/gpt4all/releases")
    print(f"2. Download: {filename}")
    print(f"3. Save to: {model_dir}")
    sys.exit(1)
