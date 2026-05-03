import subprocess
import sys
import os

os.chdir(r"K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta")
python = r"K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\python.exe"

proc = subprocess.Popen(
    [python, "app/main.py"],
    stdout=open("server.log", "w"),
    stderr=subprocess.STDOUT
)
print("Server started with PID:", proc.pid)