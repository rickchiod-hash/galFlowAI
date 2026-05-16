"""Adapter para FramePack - Motor experimental de vídeo"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import logging
from app.config import ENGINES_DIR

logger = logging.getLogger(__name__)


class FramePackAdapter:
    """Adapter para integrar FramePack como motor experimental"""
    
    @staticmethod
    def disponivel() -> bool:
        """Verifica se FramePack está disponível"""
        framepack_path = str(ENGINES_DIR / "FramePack")
        if not os.path.exists(framepack_path):
            return False
        possible_files = ["main.py", "run.py", "inference.py", "generate.py"]
        for file in possible_files:
            if os.path.exists(os.path.join(framepack_path, file)):
                return True
        return False
    
    def __init__(self, framepack_path: Optional[str] = None):
        self.framepack_path = framepack_path or str(ENGINES_DIR / "FramePack")
        self.available = self.disponivel()
        self.model_preset = "1.3B"
        
    def is_available(self) -> bool:
        return self.available
    
    def generate_video(self, prompt: str, output_path: str, negative_prompt: str = "",
                       duration_seconds: int = 5, num_frames: int = 16,
                       resolution: str = "480p") -> Dict[str, Any]:
        if not self.available:
            return {"success": False, "error": "FramePack não disponível", "fallback_suggested": True}
        
        try:
            cmd = [
                self._get_python_executable(),
                "generate.py",
                "--prompt", prompt,
                "--output", output_path,
                "--resolution", resolution,
                "--frames", str(num_frames),
                "--duration", str(duration_seconds)
            ]
            if negative_prompt:
                cmd.extend(["--negative_prompt", negative_prompt])
            
            logger.info("Executando FramePack: %s", " ".join(cmd))
            
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, cwd=self.framepack_path
            )
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                return {"success": True, "video_path": output_path, "prompt": prompt,
                        "provider": "FramePack", "resolution": resolution}
            else:
                logger.error("CAUSA: Erro FramePack: %s | CORREÇÃO: Verifique se FramePack está instalado e configurado", stderr)
                return {"success": False, "error": stderr, "fallback_suggested": True}
                
        except Exception as e:
            logger.error("CAUSA: Exceção FramePack: %s | CORREÇÃO: Verifique se FramePack e dependências estão instalados", str(e))
            return {"success": False, "error": str(e), "fallback_suggested": True}
    
    def _get_python_executable(self) -> str:
        studio_python = str(ENGINES_DIR.parent / "envs" / "studio" / "Scripts" / "python.exe")
        if os.path.exists(studio_python):
            return studio_python
        return "python"
    
    def get_status(self) -> Dict[str, Any]:
        return {"available": self.available, "path": self.framepack_path,
                "model_preset": self.model_preset, "experimental": True}
