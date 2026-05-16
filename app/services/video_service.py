"""Video Service - Geração de vídeos usando WanGP ou FFmpeg fallback"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable

from app.adapters.wangp_adapter import WanGPAdapter
from app.adapters.ffmpeg_adapter import FFmpegAdapter
from app.config import PROJECTS_DIR

logger = logging.getLogger(__name__)


class VideoService:
    """Serviço para geração de vídeos comerciais"""
    
    def __init__(self, llm_provider=None):
        """
        Inicializa o serviço de vídeo.
        
        Args:
            llm_provider: Provider LLM para geração de roteiro (opcional)
        """
        self.llm_provider = llm_provider
        self.wangp_adapter = WanGPAdapter()
        self.ffmpeg_adapter = FFmpegAdapter()
        self.wangp_available = self.wangp_adapter.is_available()
        self.ffmpeg_available = self.ffmpeg_adapter.is_available()
        
        if self.wangp_available:
            logger.info("WanGP disponível - usando geração real de vídeo")
        elif self.ffmpeg_available:
            logger.info("WanGP indisponível - usando FFmpeg fallback")
        else:
            logger.warning("Nenhum motor de vídeo disponível")
    
    def is_available(self) -> bool:
        """Retorna se pelo menos um motor de vídeo está disponível"""
        return self.wangp_available or self.ffmpeg_available
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status dos motores de vídeo"""
        return {
            "available": self.is_available(),
            "wangp_available": self.wangp_available,
            "ffmpeg_available": self.ffmpeg_available,
            "preferred_provider": "WanGP" if self.wangp_available else "FFmpeg" if self.ffmpeg_available else "None"
        }
    
    def generate_scene_video(
        self,
        scene_id: str,
        prompt: str,
        output_path: str,
        negative_prompt: str = "",
        duration_seconds: int = 5,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Gera vídeo para uma única cena.
        
        Args:
            scene_id: ID da cena
            prompt: Prompt positivo para geração
            output_path: Caminho para salvar o vídeo
            negative_prompt: Prompt negativo (opcional)
            duration_seconds: Duração em segundos
            progress_callback: Função de callback para progresso
            
        Returns:
            Dict com status e metadados
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "Nenhum motor de vídeo disponível",
                "scene_id": scene_id
            }
        
        if progress_callback:
            progress_callback(0, f"Iniciando geração da cena {scene_id}...")
        
        # Tenta WanGP primeiro
        if self.wangp_available:
            if progress_callback:
                progress_callback(10, f"Gerando vídeo com WanGP (cena {scene_id})...")
            
            result = self.wangp_adapter.generate_video(
                prompt=prompt,
                output_path=output_path,
                negative_prompt=negative_prompt,
                duration_seconds=duration_seconds
            )
            
            if result.get("success"):
                if progress_callback:
                    progress_callback(100, f"Cena {scene_id} gerada com sucesso (WanGP)")
                return {
                    "success": True,
                    "scene_id": scene_id,
                    "video_path": output_path,
                    "provider": "WanGP",
                    "duration": duration_seconds
                }
            else:
                logger.warning(f"WanGP falhou para cena {scene_id}: {result.get('error')}")
        
        # Fallback: FFmpeg
        if self.ffmpeg_available:
            if progress_callback:
                progress_callback(20, f"Usando FFmpeg fallback para cena {scene_id}...")
            
            result = self.ffmpeg_adapter.create_static_video(
                text=prompt[:200],  # Limita texto para vídeo
                output_path=output_path,
                duration=duration_seconds
            )
            
            if result.get("success"):
                if progress_callback:
                    progress_callback(100, f"Cena {scene_id} gerada com sucesso (FFmpeg)")
                return {
                    "success": True,
                    "scene_id": scene_id,
                    "video_path": output_path,
                    "provider": "FFmpeg",
                    "duration": duration_seconds
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Erro FFmpeg"),
                    "scene_id": scene_id
                }
        
        return {
            "success": False,
            "error": "Todos os motores de vídeo falharam",
            "scene_id": scene_id
        }
    
    def generate_commercial(
        self,
        project_id: str,
        product: str,
        target_audience: str,
        duration_seconds: int = 30,
        style: str = "viral",
        keywords: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Gera um comercial completo: roteiro -> cenas -> vídeos -> montagem.
        
        Args:
            project_id: ID do projeto
            product: Nome do produto
            target_audience: Público-alvo
            duration_seconds: Duração total em segundos
            style: Estilo (viral, premium, direct)
            keywords: Palavras-chave
            progress_callback: Função de callback para progresso
            
        Returns:
            Dict com status e caminhos dos arquivos gerados
        """
        try:
            from app.services.script_service import generate_script
            from app.domain.scene_parser import split_script_into_scenes
            from app.domain.prompt_builder_service import build_prompts_for_scenes
            import json
            
            project_dir = Path(PROJECTS_DIR) / project_id
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. Gerar roteiro
            if progress_callback:
                progress_callback(10, "Gerando roteiro...")
            
            script_result = generate_script(
                briefing=f"{product}. Público: {target_audience}",
                mode="safe"
            )
            
            if not script_result or "script" not in script_result:
                return {"success": False, "error": "Falha ao gerar roteiro"}
            
            script_text = script_result["script"]
            
            # Salva roteiro
            script_path = project_dir / "script" / "script_approved.md"
            script_path.parent.mkdir(exist_ok=True)
            script_path.write_text(script_text, encoding="utf-8")
            
            # 2. Dividir em cenas
            if progress_callback:
                progress_callback(20, "Dividindo em cenas...")
            
            scenes = split_script_into_scenes(script_text, project_id=project_id)
            
            if not scenes:
                return {"success": False, "error": "Falha ao dividir em cenas"}
            
            # Salva cenas
            scenes_path = project_dir / "storyboard" / "scenes.json"
            scenes_path.parent.mkdir(exist_ok=True)
            import json
            scenes_path.write_text(
                json.dumps(scenes, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            
            # 3. Gerar prompts para cada cena
            if progress_callback:
                progress_callback(30, "Gerando prompts de vídeo...")
            
            scene_prompts = build_prompts_for_scenes(
                scenes=scenes,
                project_id=project_id
            )
            
            # 4. Gerar vídeos das cenas
            if progress_callback:
                progress_callback(40, "Gerando vídeos das cenas...")
            
            rendered_scenes = []
            
            for i, scene_prompt in enumerate(scene_prompts):
                progress = 40 + (i / len(scene_prompts)) * 40
                if progress_callback:
                    progress_callback(int(progress), f"Gerando cena {i+1}/{len(scene_prompts)}...")
                
                scene_output = project_dir / "renders" / f"scene_{i:03d}.mp4"
                scene_output.parent.mkdir(exist_ok=True)
                
                result = self.generate_scene_video(
                    scene_id=f"scene_{i:03d}",
                    prompt=scene_prompt.get("prompt", ""),
                    output_path=str(scene_output),
                    negative_prompt=scene_prompt.get("negative_prompt", ""),
                    duration_seconds=scene_prompt.get("duration", 5)
                )
                
                if result.get("success"):
                    scene_prompt["status"] = "completed"
                    scene_prompt["video_path"] = str(scene_output)
                    rendered_scenes.append(scene_prompt)
                else:
                    scene_prompt["status"] = "failed"
                    scene_prompt["error"] = result.get("error", "Erro desconhecido")
            
            # 5. Montar vídeo final
            if progress_callback:
                progress_callback(85, "Montando vídeo final...")
            
            final_video_path = project_dir / "final" / "commercial.mp4"
            final_video_path.parent.mkdir(exist_ok=True)
            
            video_files = [s["video_path"] for s in rendered_scenes if s.get("video_path")]
            
            if not video_files:
                return {"success": False, "error": "Nenhum vídeo de cena foi gerado"}
            
            concat_result = self.ffmpeg_adapter.concat_videos(
                video_paths=video_files,
                output_path=str(final_video_path)
            )
            
            if not concat_result.get("success"):
                return {
                    "success": False,
                    "error": f"Falha ao montar vídeo final: {concat_result.get('error')}"
                }
            
            if progress_callback:
                progress_callback(100, "Comercial gerado com sucesso!")
            
            return {
                "success": True,
                "project_id": project_id,
                "final_video": str(final_video_path),
                "script_path": str(script_path),
                "scenes_count": len(rendered_scenes),
                "scenes_succeeded": len([s for s in rendered_scenes if s.get("status") == "completed"]),
                "provider_used": "WanGP" if self.wangp_available else "FFmpeg Fallback"
            }
        except Exception as e:
            logger.error(f"Erro no serviço de vídeo: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def export_final_video(
        self,
        video_path: str,
        audio_path: Optional[str] = None,
        srt_path: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Exporta video final com audio e legenda opcionais.

        Args:
            video_path: Caminho do video de entrada
            audio_path: Caminho do audio (opcional)
            srt_path: Caminho do SRT (opcional)
            output_path: Caminho de saida (auto se None)

        Returns:
            Dict com success, video_path, manifest
        """
        try:
            if not Path(video_path).exists():
                return {"success": False, "error": "Video de origem nao encontrado"}

            out = Path(output_path) if output_path else Path(video_path).parent / "final" / "commercial.mp4"
            out.parent.mkdir(parents=True, exist_ok=True)

            manifest = {"audio": bool(audio_path), "srt": bool(srt_path)}

            if audio_path and Path(audio_path).exists():
                result = self.ffmpeg_adapter.add_audio_to_video(video_path, audio_path, str(out))
                if not result.get("success"):
                    result = self.ffmpeg_adapter.concat_videos([video_path], str(out), audio_path=audio_path)
            else:
                result = self.ffmpeg_adapter.concat_videos([video_path], str(out))

            if result.get("success"):
                manifest_path = out.parent / "export_manifest.json"
                manifest_path.write_text(
                    json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
                )
                return {"success": True, "video_path": str(out), "manifest": manifest}
            return {"success": False, "error": result.get("error", "Falha no FFmpeg")}
        except Exception as e:
            logger.error("Export falhou: %s", e, exc_info=True)
            return {"success": False, "error": str(e)}
