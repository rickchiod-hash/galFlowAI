#!/usr/bin/env python3
"""Install CPU-only PyTorch for WanGP adapter."""
import subprocess
import sys

pip_exe = r"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\pip.exe"
cache_dir = r"K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"

print("Installing CPU-only PyTorch...")
result = subprocess.run(
    [pip_exe, "install", "torch", "--index-url", "https://download.pytorch.org/whl/cpu", "--cache-dir", cache_dir],
    capture_output=True,
    text=True,
    timeout=180
)

print("STDOUT:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    print("SUCCESS: PyTorch installed")
else:
    print("FAILED: Could not install PyTorch")
    sys.exit(1)
