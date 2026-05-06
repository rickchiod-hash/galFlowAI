#!/usr/bin/env python3
"""Download GPT4All model using huggingface_hub (public access)."""
import sys
import os
from pathlib import Path

# Ensure huggingface_hub is available
try:
    from huggingface_hub import hf_hub_download, whoami
except ImportError:
    print("Installing huggingface_hub...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub", "--quiet"], 
                   check=True)
    from huggingface_hub import hf_hub_download, whoami

# Model config
repo_id = "TheBloke/Orca-Mini-3B-GGUF"
filename = "orca-mini-3b.q4_0.gguf"
model_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/models/gpt4all")
model_dir.mkdir(parents=True, exist_ok=True)
model_path = model_dir / filename

if model_path.exists():
    print(f"✅ Model already exists: {model_path}")
    print(f"   Size: {model_path.stat().st_size / (1024*1024):.1f} MB")
    sys.exit(0)

print(f"Downloading {filename} (~2GB)...")
print(f"From: {repo_id}")
print(f"To: {model_path}")
print()

try:
    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=str(model_dir),
        token=False,  # Public model, no auth needed
        force_download=True
    )
    
    if os.path.exists(downloaded_path):
        size_mb = os.path.getsize(downloaded_path) / (1024 * 1024)
        print(f"\n✅ SUCCESS: Model downloaded!")
        print(f"   Path: {downloaded_path}")
        print(f"   Size: {size_mb:.1f} MB")
        sys.exit(0)
    else:
        print("❌ Download reported success but file not found")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nAlternative: Manual download")
    print(f"1. Go to: https://huggingface.co/TheBloke/Orca-Mini-3B-GGUF")
    print(f"2. Download: {filename}")
    print(f"3. Save to: {model_dir}")
    sys.exit(1)
