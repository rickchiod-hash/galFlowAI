#!/usr/bin/env python3
"""Download GPT4All model - Mistral 7B Instruct Q4_0 (compatible model)."""
import sys
from pathlib import Path

model_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/models/gpt4all")
model_dir.mkdir(parents=True, exist_ok=True)

print("Using GPT4All Python package...")
print(f"Model directory: {model_dir}")
print()

try:
    from gpt4all import GPT4All
    
    # Use a known working model
    model_name = "mistral-7b-openorca.Q4_0.gguf"
    print(f"Loading model: {model_name}")
    print("(This will auto-download ~4GB if not present)")
    print()
    
    # Let GPT4All handle the download with progress
    model = GPT4All(
        model_name=model_name,
        model_path=str(model_dir),
        allow_download=True
    )
    
    print(f"\nSUCCESS: Model loaded!")
    print(f"Model path: {model.model_path}")
    
    # Test generation
    print("\nTesting generation...")
    response = model.generate("Hello! Who are you?", max_tokens=50)
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
    print(f"Error type: {type(e).__name__}")
    
    # Try alternative model
    print("\nTrying alternative model...")
    try:
        from gpt4all import GPT4All
        # Try orca-mini-3b (smaller, better for 6GB VRAM)
        alt_model = "orca-mini-3b-gguf"
        print(f"Trying: {alt_model}")
        model = GPT4All(
            model_name=alt_model,
            model_path=str(model_dir),
            allow_download=True
        )
        print(f"\nSUCCESS with alternative model!")
        sys.exit(0)
    except Exception as e2:
        print(f"Alternative also failed: {e2}")
    
    print("\nManual download instructions:")
    print("1. Go to: https://gpt4all.com/")
    print("2. Download a small model (3B-7B, Q4 quantization)")
    print(f"3. Save to: {model_dir}")
    sys.exit(1)
