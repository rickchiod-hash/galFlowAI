"""Video concatenation stage"""

from app.pipeline.stages.base_stage import BaseStage
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class VideoConcatenationStage(BaseStage):
    """Stage for concatenating scene videos into final video"""
    
    def __init__(self, ffmpeg_adapter):
        super().__init__()
        self.ffmpeg_adapter = ffmpeg_adapter
    
    def execute(self, rendered_scenes: list, project_id: str, projects_dir: str = None, **kwargs) -> dict:
        """
        Concatenate scene videos into final video
        
        Args:
            rendered_scenes: List of scene dictionaries with video_path
            project_id: Project identifier
            projects_dir: Base directory for projects
            **kwargs: Additional parameters
            
        Returns:
            Dict with concatenation results
        """
        try:
            logger.info(f"Concatenating {len(rendered_scenes)} scene videos")
            
            # Create final directory
            if projects_dir:
                final_dir = Path(projects_dir) / project_id / "final"
            else:
                final_dir = Path(kwargs.get('final_dir', '')) / project_id / "final"
            final_dir.mkdir(parents=True, exist_ok=True)
            final_video_path = final_dir / "commercial.mp4"
            
            # Get video files from rendered scenes
            video_files = [s["video_path"] for s in rendered_scenes if s.get("video_path")]
            
            if not video_files:
                return self._create_result(False, error="Nenhum vídeo de cena foi gerado")
            
            # Concatenate videos (audio is optional)
            concat_result = self.ffmpeg_adapter.concat_videos(
                video_paths=video_files,
                output_path=str(final_video_path),
                audio_path=None  # Audio per scene can be added in post-processing
            )
            
            if not concat_result.get("success"):
                return self._create_result(False, error=f"Falha ao montar vídeo final: {concat_result.get('error')}")
            
            return self._create_result(True, {
                "final_video_path": str(final_video_path),
                "video_files_used": video_files
            })
            
        except Exception as e:
            logger.error(f"Error in video concatenation: {e}")
            return self._create_result(False, error=str(e))
