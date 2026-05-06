#!/usr/bin/env python3
import subprocess
import time
import sys
import os

# Path to the Python executable
python_exe = r"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe"
app_path = r"app\main.py"

# Start the application
print("Starting application...")
proc = subprocess.Popen([python_exe, app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Wait for the application to start
time.sleep(10)

# Check if the process is still running
if proc.poll() is None:
    print("Application is running (PID: {})".format(proc.pid))
    # Try to check if port 7860 is listening
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 7860))
    if result == 0:
        print("SUCCESS: Port 7860 is open - application is accessible")
    else:
        print("WARNING: Port 7860 is not open - application may not be listening on the expected port")
    # Terminate the process
    proc.terminate()
    proc.wait(timeout=5)
    if proc.poll() is None:
        proc.kill()
        proc.wait()
else:
    # Process has ended, capture output
    stdout, stderr = proc.communicate()
    print("Application exited with code: {}".format(proc.returncode))
    if stdout:
        print("STDOUT:")
        print(stdout[:500])  # First 500 chars
    if stderr:
        print("STDERR:")
        print(stderr[:500])  # First 500 chars

print("Verification complete.")