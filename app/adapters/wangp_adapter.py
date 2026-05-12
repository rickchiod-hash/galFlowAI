"""Adapter para WanGP (Wan2GP) - Motor de vídeo principal"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
import shutil

import app.config as config

logger = logging.getLogger(__name__)

_WANGP_DEFAULT = str(config.ENGINES_DIR / "Wan2GP")


class WanGPAdapter:
    """Adapter para integrar WanGP/Wan2GP para geração de vídeo"""
    
    @staticmethod
    def disponivel() -> bool:
        """Verifica se WanGP está disponível (método estático para testes)"""
        import os
        wangp_path = _WANGP_DEFAULT
        if not os.path.exists(wangp_path):
            return False
        possible_main_files = ["main.py", "gradio.py", "wan_interface.py", "inference.py"]
        for file in possible_main_files:
            if os.path.exists(os.path.join(wangp_path, file)):
                return True
        return False
    
    def __init__(self, wangp_path: Optional[str] = None):
        """
        Inicializa o adapter WanGP.
        
        Args:
            wangp_path: Caminho para a instalação do WanGP. Se None, usa padrão.
        """
        self.wangp_path = wangp_path or _WANGP_DEFAULT
        self.available = self._check_availability()
        self.model_preset = "1.3B"  # Padrão para GTX 1660 Super (6GB VRAM)
        self.resolution = "480p"     # Seguro para 6GB VRAM
        
    def _check_availability(self) -> bool:
        """Verifica se WanGP está disponível"""
        if not os.path.exists(self.wangp_path):
            logger.info(f"WanGP não encontrado em: {self.wangp_path}")
            return False
        
        # Verifica arquivos essenciais (main.py ou gradio.py ou wan_interface.py)
        possible_main_files = ["main.py", "gradio.py", "wan_interface.py", "inference.py"]
        main_found = False
        for file in possible_main_files:
            if os.path.exists(os.path.join(self.wangp_path, file)):
                self.main_file = file
                main_found = True
                break
        
        if not main_found:
            logger.info(f"Arquivo principal do WanGP não encontrado em {self.wangp_path}")
            return False
        
        # Verifica se PyTorch está instalado (simplificado)
        try:
            import torch
            self.available = True
            return True
        except ImportError:
            logger.warning("CAUSA: PyTorch não encontrado no ambiente | CORREÇÃO: Instale PyTorch no ambiente studio")
            self.available = False
            return False
    
    def is_available(self) -> bool:
        """Retorna se WanGP está disponível"""
        return self.available

    def render_scene(self, project_id: str, scene: dict, preset: dict = None) -> dict:
        """Render a single scene using generate_video().
        
        Called by RenderVideoUseCase with the scene dict format.
        Maps scene fields to generate_video parameters.
        """
        prompt = scene.get("prompt", scene.get("description", "Cena sem descricao"))
        scene_id = scene.get("id", scene.get("scene_number", "000"))
        output_path = scene.get("output_path", "")
        if not output_path:
            from app.config import PROJECTS_DIR
            output_dir = Path(PROJECTS_DIR) / project_id / "renders"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / "scene_%s.mp4" % str(scene_id).zfill(3))
        duration = scene.get("duration", scene.get("duration_estimate", 5))
        neg_prompt = scene.get("prompt_negative", scene.get("negative_prompt", ""))
        res = None
        if preset:
            res = preset.get("resolution")
        return self.generate_video(
            prompt=prompt,
            output_path=output_path,
            negative_prompt=neg_prompt,
            duration_seconds=int(duration),
            resolution=res,
        )

    def generate_video(
        self,
        prompt: str,
        output_path: str,
        negative_prompt: str = "",
        duration_seconds: int = 5,
        num_frames: int = 16,
        resolution: Optional[str] = None,
        model_preset: Optional[str] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Gera vídeo usando WanGP.
        
        Args:
            prompt: Prompt positivo para geração
            output_path: Caminho para salvar o vídeo
            negative_prompt: Prompt negativo
            duration_seconds: Duração desejada em segundos
            num_frames: Número de frames
            resolution: Resolução (ex: 480p, 512p)
            model_preset: Modelo (ex: 1.3B) - padrão seguro para 6GB VRAM
            progress_callback: Função de callback para progresso
            
        Returns:
            Dict com status, caminho do vídeo, e metadados
        """
        if not self.available:
            return {
                "success": False,
                "error": "WanGP não está disponível",
                "fallback_suggested": True
            }
        
        # Usa valores seguros para 6GB VRAM
        resolution = resolution or self.resolution
        model_preset = model_preset or self.model_preset
        
        # Validação para hardware limitation
        if self._get_vram_gb() <= 6:
            if model_preset not in ["1.3B"]:
                logger.warning("CAUSA: Modelo %s muito grande para 6GB VRAM | CORREÇÃO: Usando 1.3B (padrão seguro)", model_preset)
                model_preset = "1.3B"
            if resolution not in ["480p", "512p"]:
                logger.warning("CAUSA: Resolução %s muito alta para 6GB VRAM | CORREÇÃO: Usando 480p (padrão seguro)", resolution)
                resolution = "480p"
        
        try:
            # Prepara comando WanGP
            cmd = self._build_command(
                prompt=prompt,
                negative_prompt=negative_prompt,
                output_path=output_path,
                duration_seconds=duration_seconds,
                num_frames=num_frames,
                resolution=resolution,
                model_preset=model_preset
            )
            
            logger.info(f"Executando WanGP: {' '.join(cmd)}")
            
            # Executa WanGP
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.wangp_path
            )
            
            # Monitora progresso
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "video_path": output_path,
                    "prompt": prompt,
                    "model": model_preset,
                    "resolution": resolution,
                    "duration": duration_seconds,
                    "provider": "WanGP"
                }
            else:
                logger.error("CAUSA: Erro WanGP: %s | CORREÇÃO: Verifique se WanGP está instalado e configurado", stderr)
                return {
                    "success": False,
                    "error": stderr,
                    "fallback_suggested": True
                }
                
        except Exception as e:
            logger.error("CAUSA: Exceção ao executar WanGP: %s | CORREÇÃO: Verifique ambiente e dependências", e)
            return {
                "success": False,
                "error": str(e),
                "fallback_suggested": True
            }
    
    def _build_command(self, **kwargs) -> List[str]:
        """Constrói comando para execução do WanGP"""
        python_exe = self._get_python_executable()
        
        cmd = [
            python_exe,
            "main.py",
            "--prompt", kwargs["prompt"],
            "--output", kwargs["output_path"],
            "--model", kwargs.get("model_preset", "1.3B"),
            "--resolution", kwargs.get("resolution", "480p"),
            "--frames", str(kwargs.get("num_frames", 16)),
            "--duration", str(kwargs.get("duration_seconds", 5))
        ]
        
        if kwargs.get("negative_prompt"):
            cmd.extend(["--negative_prompt", kwargs["negative_prompt"]])
        
        return cmd
    
    def _get_python_executable(self) -> str:
        """Retorna caminho do Python para executar WanGP"""
        # Tenta usar o Python do ambiente studio
        studio_python = str(config.BASE_DIR / "envs" / "studio" / "Scripts" / "python.exe")
        if os.path.exists(studio_python):
            return studio_python
        
        # Fallback para python do sistema
        return "python"
    
    def _get_vram_gb(self) -> int:
        """Retorna VRAM em GB, detectada via hardware.py ou fallback para 6GB"""
        try:
            from app.hardware import get_gpu_info
            info = get_gpu_info()
            vram = int(info.get("vram_gb", 6))
            logger.debug(f"VRAM detectada: {vram}GB")
            return max(vram, 1)
        except Exception as e:
            logger.warning(f"CAUSA: Falha ao detectar VRAM via hardware.py: {e} | CORREÇÃO: Usando fallback 6GB")
            return 6
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do adapter"""
        return {
            "available": self.available,
            "path": self.wangp_path,
            "model_preset": self.model_preset,
            "resolution": self.resolution,
            "vram_gb": self._get_vram_gb()
        }
