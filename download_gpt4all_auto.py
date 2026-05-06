#!/usr/bin/env python3
"""Download GPT4All model using the official Python package (handles download internally)."""
import sys
import time
from pathlib import Path

model_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/models/gpt4all")
model_dir.mkdir(parents=True, exist_ok=True)

print("Using GPT4All Python package to download model...")
print(f"Model directory: {model_dir}")
print()

try:
    from gpt4all import GPT4All
    
    # This will automatically download the model if not present
    print("Initializing GPT4All with model: orca-mini-3b-gguf...")
    print("(This will download ~2GB if not already present)")
    print()
    
    # Create with download=True (default)
    model = GPT4All(
        model_name="orca-mini-3b-gguf",
        model_path=str(model_dir),
        allow_download=True
    )
    
    print(f"\nSUCCESS: Model loaded!")
    print(f"Model path: {model.model_path}")
    
    # Test generation
    print("\nTesting generation...")
    response = model.generate("Hello, who are you?", max_tokens=50)
    print(f"Response: {response[:100]}...")
    
    sys.exit(0)
    
except ImportError:
    print("ERROR: gpt4all package not installed")
    print("Installing gpt4all...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "gpt4all", "--quiet"])
    print("Please run this script again.")
    sys.exit(1)
    
except Exception as e:
    print(f"\nFAILED: {e}")
    print("\nAlternative: Manual download")
    print("1. Go to: https://gpt4all.com/")
    print("2. Download: orca-mini-3b.gguf")
    print(f"3. Save to: {model_dir}")
    sys.exit(1)
