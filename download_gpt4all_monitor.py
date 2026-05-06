#!/usr/bin/env python3
"""Download GPT4All model with real-time visual progress bar."""
import sys
import requests
from pathlib import Path

# Configuration
url = "https://huggingface.co/TheBloke/Orca-Mini-3B-GGUF/resolve/main/orca-mini-3b.q4_0.gguf"
filename = "orca-mini-3b.q4_0.gguf"
model_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/models/gpt4all")
dest = model_dir / filename
model_dir.mkdir(parents=True, exist_ok=True)

# Check if already exists
if dest.exists():
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(f"✅ Model already exists: {dest}")
    print(f"   Size: {size_mb:.1f} MB")
    sys.exit(0)

    print(f"Downloading: {filename} (~2GB)")
print(f"   From: {url}")
print(f"   To: {dest}")
print()

try:
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    total_mb = total_size / (1024 * 1024)
    block_size = 1024 * 1024  # 1MB chunks
    downloaded = 0
    bar_width = 50
    
    print(f"Total size: {total_mb:.1f} MB")
    print("Progress:")
    
    with open(dest, 'wb') as f:
        for data in response.iter_content(block_size):
            if data:
                f.write(data)
                downloaded += len(data)
                percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                mb_down = downloaded / (1024 * 1024)
                
                # Create visual bar
                filled = int(bar_width * (percent / 100))
                bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
                
                # Print progress (no newline, overwrite line)
                print(f"\r{bar} {percent:.1f}% ({mb_down:.1f}MB / {total_mb:.1f}MB)", end="", flush=True)
    
    print(f"\n\n✅ SUCCESS: Model downloaded!")
    final_mb = dest.stat().st_size / (1024 * 1024)
    print(f"   Path: {dest}")
    print(f"   Size: {final_mb:.1f} MB")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")
    print("\nAlternative: Manual download")
    print(f"1. Go to: https://huggingface.co/TheBloke/Orca-Mini-3B-GGUF")
    print(f"2. Download: {filename}")
    print(f"3. Save to: {model_dir}")
    sys.exit(1)
