"""Video generation stage"""

from app.pipeline.stages.base_stage import BaseStage
import logging

logger = logging.getLogger(__name__)


class VideoGenerationStage(BaseStage):
    """Stage for generating videos for scenes"""
    
    def __init__(self, wangp_adapter, ffmpeg_adapter, framepack_adapter=None):
        super().__init__()
        self.wangp_adapter = wangp_adapter
        self.ffmpeg_adapter = ffmpeg_adapter
        self.framepack_adapter = framepack_adapter
        self.try_framepack_first = False  # Set to True to try FramePack first (experimental)
    
    def execute(self, scene_prompts: list, project_id: str, **kwargs) -> dict:
        """
        Generate videos for each scene (WanGP, FramePack experimental, or FFmpeg fallback)
        
        Args:
            scene_prompts: List of scene prompt dictionaries
            project_id: Project identifier (for file paths)
            **kwargs: Additional parameters (try_framepack_first: bool)
            
        Returns:
            Dict with video generation results
        """
        try:
            logger.info(f"Generating videos for {len(scene_prompts)} scenes")
            
            # Create renders directory
            from pathlib import Path
            renders_dir = Path(kwargs.get('projects_dir', '')) / project_id / "renders"
            renders_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if we should try FramePack first
            try_framepack_first = kwargs.get('try_framepack_first', self.try_framepack_first)
            
            # Process each scene
            rendered_scenes = []
            for i, scene_prompt in enumerate(scene_prompts):
                scene_output = renders_dir / f"scene_{i:03d}.mp4"
                
                # Create a copy of the scene to avoid modifying original
                updated_scene = scene_prompt.copy()
                
                video_generated = False
                
                # Try FramePack first if requested and available (experimental)
                if try_framepack_first and self.framepack_adapter and self.framepack_adapter.is_available():
                    logger.info(f"Trying FramePack for scene {i} (experimental)")
                    framepack_result = self.framepack_adapter.generate_video(
                        prompt=scene_prompt.get("prompt", ""),
                        output_path=str(scene_output),
                        negative_prompt=scene_prompt.get("negative_prompt", ""),
                        duration_seconds=scene_prompt.get("duration", 5)
                    )
                    
                    if framepack_result.get("success"):
                        updated_scene["status"] = "completed"
                        updated_scene["video_path"] = str(scene_output)
                        updated_scene["provider"] = "FramePack"
                        rendered_scenes.append(updated_scene)
                        video_generated = True
                        logger.info(f"FramePack generated video for scene {i}")
                
                # Try WanGP if FramePack not used or failed
                if not video_generated and self.wangp_adapter.is_available():
                    video_result = self.wangp_adapter.generate_video(
                        prompt=scene_prompt.get("prompt", ""),
                        output_path=str(scene_output),
                        negative_prompt=scene_prompt.get("negative_prompt", ""),
                        duration_seconds=scene_prompt.get("duration", 5)
                    )
                    
                    if video_result.get("success"):
                        updated_scene["status"] = "completed"
                        updated_scene["video_path"] = str(scene_output)
                        updated_scene["provider"] = "WanGP"
                        rendered_scenes.append(updated_scene)
                        video_generated = True
                
                # Fallback: FFmpeg (vídeo estático com texto)
                if not video_generated:
                    logger.info(f"WanGP/FramePack não disponível, usando FFmpeg para cena {i}")
                    # Usa scene_text ou prompt como texto
                    text_for_video = scene_prompt.get("scene_text") or scene_prompt.get("prompt", "Cena")
                    ffmpeg_result = self.ffmpeg_adapter.create_static_video(
                        text=text_for_video,
                        output_path=str(scene_output),
                        duration=scene_prompt.get("duration", 5)
                    )
                    
                    if ffmpeg_result.get("success"):
                        updated_scene["status"] = "completed"
                        updated_scene["video_path"] = str(scene_output)
                        updated_scene["provider"] = "FFmpeg"
                        rendered_scenes.append(updated_scene)
                    else:
                        updated_scene["status"] = "failed"
                        updated_scene["error"] = ffmpeg_result.get("error", "Erro desconhecido")
                        logger.warning(f"Falha ao gerar vídeo para cena {i}: {ffmpeg_result.get('error')}")
                else:
                    # Already added to rendered_scenes
                    pass
            
            return self._create_result(True, {
                "rendered_scenes": rendered_scenes
            })
            
        except Exception as e:
            logger.error(f"Error in video generation: {e}")
            return self._create_result(False, error=str(e))