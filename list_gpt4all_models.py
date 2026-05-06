#!/usr/bin/env python3
"""List available GPT4All models."""
try:
    from gpt4all import GPT4All
    print("Available models:")
    models = GPT4All.list_models()
    for m in models[:20]:  # First 20
        print(f"  - {m}")
    print(f"\nTotal: {len(models)} models")
except Exception as e:
    print(f"Error: {e}")
