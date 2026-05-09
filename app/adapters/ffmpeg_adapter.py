"""Adapter para FFmpeg - Processamento de vídeo estático e montagem"""

import subprocess
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from app.logging_config import setup_logger
from app import config

logger = setup_logger()

# Caminhos conhecidos do FFmpeg — relativos ao BASE_DIR
_FFMPEG_PATHS = [
    config.BASE_DIR / "tools" / "ffmpeg" / "ffmpeg-8.1-essentials_build" / "bin" / "ffmpeg.exe",
    config.ENGINES_DIR / "Wan2GP" / "ffmpeg_bins" / "ffmpeg.exe",
    config.BASE_DIR / "envs" / "studio" / "Library" / "bin" / "ffmpeg.exe"
]

def _find_ffmpeg() -> Path:
    import shutil
    # Tenta PATH primeiro
    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        return Path(ffmpeg_in_path)
    
    # Tenta caminhos conhecidos
    for path in _FFMPEG_PATHS:
        if path.exists():
            return path
    
    # Se não encontrou, retorna o primeiro caminho conhecido (mesmo que não exist)
    if _FFMPEG_PATHS:
        return _FFMPEG_PATHS[0]
    return Path("ffmpeg")  # Fallback: espera que esteja no PATH

FFMPEG_PATH = _find_ffmpeg()


class FFmpegAdapter:
    """Adapter para operações com FFmpeg"""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Inicializa o adapter FFmpeg.
        
        Args:
            ffmpeg_path: Caminho para o executável FFmpeg. Se None, usa padrão.
        """
        if ffmpeg_path:
            self.ffmpeg_path = Path(ffmpeg_path)
        else:
            # Usa a função para encontrar FFmpeg
            self.ffmpeg_path = _find_ffmpeg()
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Verifica se FFmpeg está disponível"""
        # Tenta encontrar no PATH primeiro
        import shutil
        ffmpeg_in_path = shutil.which("ffmpeg")
        if ffmpeg_in_path:
            self.ffmpeg_path = Path(ffmpeg_in_path)
            logger.info("FFmpeg encontrado no PATH: %s", ffmpeg_in_path)
            return True
        # Tenta caminho padrão
        if self.ffmpeg_path.exists():
            logger.info("FFmpeg encontrado: %s", self.ffmpeg_path)
            return True
        logger.warning("CAUSA: FFmpeg não encontrado em %s ou no PATH | CORREÇÃO: Verifique se FFmpeg está instalado e no PATH", self.ffmpeg_path)
        return False
    
    def is_available(self) -> bool:
        """Retorna se FFmpeg está disponível"""
        return self.available
    
    def create_static_video(
        self,
        text: str,
        output_path: str,
        duration: int = 5,
        width: int = 854,
        height: int = 480,
        bg_color: str = "303030",
        text_color: str = "FFFFFF"
    ) -> Dict[str, Any]:
        """
        Cria vídeo estático com texto (fallback quando WanGP não disponível).
        
        Args:
            text: Texto para exibir no vídeo
            output_path: Caminho para salvar o vídeo
            duration: Duração em segundos
            width: Largura do vídeo
            height: Altura do vídeo
            bg_color: Cor de fundo (hex sem #)
            text_color: Cor do texto (hex sem #)
            
        Returns:
            Dict com status e metadados
        """
        if not self.available:
            return {
                "success": False,
                "error": "FFmpeg não disponível"
            }
        
        try:
            # Cria filtro de texto (escapa aspas)
            text_escaped = text.replace("'", "'\\''")
            drawtext_filter = (
                f"drawtext=text='{text_escaped}':"
                f"fontcolor={text_color}:"
                f"fontsize=24:"
                f"x=(w-text_w)/2:y=(h-text_h)/2:"
                f"box=1:boxcolor={bg_color}@0.5"
            )
            
            cmd = [
                str(self.ffmpeg_path), "-y",
                "-f", "lavfi",
                "-i", f"color=c={bg_color}:s={width}x{height}:d={duration}",
                "-vf", drawtext_filter,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-t", str(duration),
                output_path
            ]
            
            logger.info("Criando vídeo estático com FFmpeg...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and Path(output_path).exists():
                logger.info("Vídeo estático criado: %s", Path(output_path).name)
                return {
                    "success": True,
                    "video_path": output_path,
                    "duration": duration,
                    "method": "static_text"
                }
            else:
                logger.error("CAUSA: Erro FFmpeg: %s | CORREÇÃO: Verifique parâmetros de vídeo/áudio", result.stderr[-500:] if result.stderr else "Sem erro")
                return {
                    "success": False,
                    "error": result.stderr[-500:] if result.stderr else "Erro desconhecido"
                }
                
        except Exception as e:
            logger.error("CAUSA: Exceção ao criar vídeo estático: %s | CORREÇÃO: Verifique se imagem e áudio estão acessíveis", str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    def concat_videos(
        self,
        video_paths: List[str],
        output_path: str,
        audio_path: Optional[str] = None,
        transition: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Concatena múltiplos vídeos em um único arquivo.
        
        Args:
            video_paths: Lista de caminhos dos vídeos
            output_path: Caminho para salvar o vídeo final
            audio_path: Caminho opcional para áudio de fundo
            transition: Transição entre vídeos (None, 'fade', etc.)
            
        Returns:
            Dict com status e metadados
        """
        if not self.available:
            return {
                "success": False,
                "error": "FFmpeg não disponível"
            }
        
        if not video_paths:
            return {
                "success": False,
                "error": "Nenhum vídeo para concatenar"
            }
        
        try:
            # Filtra apenas vídeos que existem
            valid_videos = [vp for vp in video_paths if Path(vp).exists()]
            
            if not valid_videos:
                return {
                    "success": False,
                    "error": "Nenhum vídeo válido encontrado"
                }
            
            # Cria arquivo de lista para o FFmpeg
            list_file = Path(output_path).parent / "concat_list.txt"
            list_content = ""
            for vp in valid_videos:
                list_content += f"file '{Path(vp).resolve()}'\n"
            list_file.write_text(list_content, encoding="utf-8")
            
            # Comando base
            if audio_path and Path(audio_path).exists():
                # Com áudio: concat + audio em um passo
                cmd = [
                    str(self.ffmpeg_path), "-y",
                    "-f", "concat", "-safe", "0",
                    "-i", str(list_file),
                    "-i", str(audio_path),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-preset", "fast",
                    "-c:a", "aac",
                    "-shortest",
                    output_path
                ]
            else:
                # Sem áudio
                cmd = [
                    str(self.ffmpeg_path), "-y",
                    "-f", "concat", "-safe", "0",
                    "-i", str(list_file),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-preset", "fast",
                    output_path
                ]
            
            logger.info("Concatenando %d vídeos...", len(valid_videos))
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            # Limpa arquivo temporário
            if list_file.exists():
                list_file.unlink()
            
            if result.returncode == 0 and Path(output_path).exists():
                logger.info("Vídeos concatenados: %s", Path(output_path).name)
                return {
                    "success": True,
                    "video_path": output_path,
                    "videos_count": len(valid_videos),
                    "audio_added": audio_path is not None
                }
            else:
                logger.error("CAUSA: Erro ao concatenar: %s | CORREÇÃO: Verifique se vídeos de cena existem e são compatíveis", result.stderr[-500:] if result.stderr else "Sem erro")
                return {
                    "success": False,
                    "error": result.stderr[-500:] if result.stderr else "Erro desconhecido"
                }
                
        except Exception as e:
            logger.error("CAUSA: Exceção ao concatenar vídeos: %s | CORREÇÃO: Verifique integridade dos arquivos de vídeo", str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_audio_to_video(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> Dict[str, Any]:
        """
        Adiciona áudio a um vídeo existente.
        
        Args:
            video_path: Caminho do vídeo
            audio_path: Caminho do áudio
            output_path: Caminho para salvar
            
        Returns:
            Dict com status
        """
        if not self.available:
            return {"success": False, "error": "FFmpeg não disponível"}
        
        try:
            cmd = [
                str(self.ffmpeg_path), "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and Path(output_path).exists():
                return {"success": True, "video_path": output_path}
            else:
                return {"success": False, "error": result.stderr[-500:] if result.stderr else "Erro"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do adapter"""
        return {
            "available": self.available,
            "path": str(self.ffmpeg_path),
            "exists": self.ffmpeg_path.exists()
        }


# ========== Funções de compatibilidade (mantidas para código existente) ==========

def check_ffmpeg():
    """Verifica se FFmpeg está disponível."""
    return FFmpegAdapter().is_available()


def create_storyboard_video(project_id: str, scenes: list) -> Path or None:
    """
    Cria vídeo de storyboard usando FFmpeg.
    Fallback: imagens estáticas + áudio.
    """
    from app.config import PROJECTS_DIR
    
    adapter = FFmpegAdapter()
    if not adapter.is_available():
        logger.error("CAUSA: FFmpeg não disponível | CORREÇÃO: Instale FFmpeg e adicione ao PATH")
        return None
    
    proj_dir = PROJECTS_DIR / project_id
    output_dir = proj_dir / "final"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "comercial_storyboard.mp4"
    
    # Cria vídeos estáticos para cada cena
    scene_videos = []
    storyboard_dir = proj_dir / "storyboard"
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    
    for scene in scenes:
        scene_id = scene.get("id", "unknown")
        scene_text = scene.get("description", "Cena")
        scene_duration = scene.get("duration_estimate", 5)
        
        scene_video = storyboard_dir / f"{scene_id}.mp4"
        result = adapter.create_static_video(
            text=scene_text,
            output_path=str(scene_video),
            duration=scene_duration
        )
        
        if result.get("success"):
            scene_videos.append(str(scene_video))
    
    if not scene_videos:
        logger.error("CAUSA: Nenhum vídeo de cena criado | CORREÇÃO: Verifique se cenas foram geradas corretamente")
        return None
    
    # Concatena todos
    concat_result = adapter.concat_videos(
        video_paths=scene_videos,
        output_path=str(output_path)
    )
    
    if concat_result.get("success"):
        return output_path
    else:
        return None


def mixar_audio_video(video_path: Path, audio_path: Path, output_path: Path) -> Path or None:
    """Combina narração com vídeo, ajustando duração automaticamente"""
    adapter = FFmpegAdapter()
    result = adapter.add_audio_to_video(
        video_path=str(video_path),
        audio_path=str(audio_path),
        output_path=str(output_path)
    )
    return Path(output_path) if result.get("success") else None


def compile_final_video(project_id: str, video_paths: list, audio_path: Path = None) -> Path or None:
    """Compila vídeos renderizados em um único MP4 final."""
    from app.config import PROJECTS_DIR
    
    adapter = FFmpegAdapter()
    proj_dir = PROJECTS_DIR / project_id
    output_path = proj_dir / "final" / "comercial_final.mp4"
    
    result = adapter.concat_videos(
        video_paths=video_paths,
        output_path=str(output_path),
        audio_path=str(audio_path) if audio_path and audio_path.exists() else None
    )
    
    return Path(output_path) if result.get("success") else None


def create_placeholder_image(output_path: Path, text: str):
    """Cria imagem placeholder com texto (requer PIL/Pillow)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (854, 480), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        position = ((854 - w) / 2, (480 - h) / 2)
        draw.text(position, text, fill=(255, 255, 255), font=font)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))
        logger.info("Placeholder criado: %s", output_path.name)
    except ImportError:
        logger.warning("CAUSA: Pillow não instalado | CORREÇÃO: pip install Pillow")
    except Exception as e:
        logger.error("CAUSA: Erro ao criar placeholder: %s | CORREÇÃO: Verifique permissões e espaço em disco", str(e))
