#!/usr/bin/env python3
import subprocess
import sys

pip_exe = r"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\pip.exe"
cache_dir = r"K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"

print("Installing gpt4all...")
result = subprocess.run(
    [pip_exe, "install", "gpt4all", "--cache-dir", cache_dir],
    capture_output=True,
    text=True,
    timeout=300
)

print("STDOUT:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    print("SUCCESS: gpt4all installed")
else:
    print("FAILED: Could not install gpt4all")
    sys.exit(1)
