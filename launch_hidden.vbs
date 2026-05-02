Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta"
WshShell.Environment("PROCESS")("PIP_CACHE_DIR") = "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"
WshShell.Environment("PROCESS")("HF_HOME") = "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface"
WshShell.Environment("PROCESS")("TORCH_HOME") = "K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch"
WshShell.Environment("PROCESS")("XDG_CACHE_HOME") = "K:\AI_VIDEO_COMERCIAL_STUDIO\cache"
WshShell.Environment("PROCESS")("TEMP") = "K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
WshShell.Environment("PROCESS")("TMP") = "K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
WshShell.Run "cmd /c ""K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe"" ""K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\run_galFlowAI.py"" > logs\vbs_launch.log 2>&1", 0, False
