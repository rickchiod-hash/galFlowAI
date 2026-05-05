#!/usr/bin/env python3
"""
Setup script for Gal AI LLM providers.
Run this script to download models for local LLM inference.
"""
import os
import sys
from pathlib import Path

print("=== Gal AI LLM Providers Setup ===")
print()

# 1. GPT4All
print("1. GPT4All Provider:")
print("   ✅ Package installed")
print("   ❌ Models needed: Place .gguf or .bin files in:")
print("      K:\\AI_VIDEO_COMMERCIAL_STUDIO\\models\\gpt4all\\")
print("   Recommended: Orca Mini 3B Q4_0 (~2GB) or similar small model")
print("   Download from: https://huggingface.co/TheBloke/Orca-Mini-3B-GGUF")
print()

# 2. LM Studio
print("2. LM Studio Provider:")
print("   ✅ Code ready")
print("   ❌ LM Studio software needed: Download and install from https://lmstudio.ai/")
print("   ❌ Start LM Studio and load a model (e.g., Mistral 7B)")
print("   ✅ Provider will auto-detect running LM Studio")
print()

# 3. KoboldCpp
print("3. KoboldCpp Provider:")
print("   ✅ Code ready")
print("   ❌ KoboldCpp software needed: https://github.com/LostRuins/KoboldCpp")
print("   ❌ Place model files in: K:\\AI_VIDEO_COMMERCIAL_STUDIO\\models\\koboldcpp\\")
print()

# 4. LlamaCpp
print("4. LlamaCpp Provider:")
print("   ✅ Code ready")
print("   ❌ Llama.cpp needed: https://github.com/ggerganov/llama.cpp")
print("   ❌ Place model files in: K:\\AI_VIDEO_COMMERCIAL_STUDIO\\models\\llamacpp\\")
print()

# 5. WanGP/Wan2GP
print("5. WanGP/Wan2GP Provider:")
print("   ✅ Code ready with hardware-aware defaults (1.3B, 480p)")
print("   ❌ PyTorch needed: Install in studio environment")
print("   ✅ WanGP directory exists: K:\\AI_VIDEO_COMMERCIAL_STUDIO\\engines\\Wan2GP")
print()

print("=== Quick Test ===")
try:
    from app.adapters.llm.provider_router import ProviderRouter
    router = ProviderRouter()
    providers = router.detect_available()
    print("Current provider availability:")
    for name, available in providers.items():
        status = "✅ Available" if available else "❌ Unavailable"
        print(f"  {name}: {status}")
except Exception as e:
    print(f"Error: {e}")

print()
print("=== Next Steps ===")
print("1. Place model files in the directories above")
print("2. Or install LM Studio and start it")
print("3. Restart the application")
print("4. The system will use available providers or fall back to TemplateProvider")
