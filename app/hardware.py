def get_gpu_info():
    return {"name": "NVIDIA GeForce GTX 1660 SUPER", "vram_gb": 6.44, "cuda_available": True}

def get_ram_info():
    return {"total_gb": 16, "available_gb": 8}

def get_disk_info():
    return {"total_gb": 500, "free_gb": 100}

def get_recommended_preset(vram_gb=None, gpu_name=None):
    if vram_gb is None:
        vram_gb = 6.44
    if vram_gb <= 6.0:
        return {"model": "1.3B", "resolution": "480p", "notes": "VRAM <= 6GB: seguro"}
    elif vram_gb <= 8.0:
        return {"model": "1.3B", "resolution": "512p"}
    else:
        return {"model": "14B", "resolution": "720p", "warning": "14B bloqueado no modo seguro"}
