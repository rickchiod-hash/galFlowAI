"""Use case for rendering video using WanGP."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.adapters.wangp_adapter import WanGPAdapter

class RenderVideoUseCase(BaseUseCase):
    """Render video using WanGP adapter.
    
    3-point standard:
    1. Validate scene and project data
    2. Render video using WanGP with safe preset
    3. Return video path and metadata
    """
    
    def execute(self, project_id: str, scene: Dict[str, Any], preset: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute video rendering use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, scene=scene):
                return self._build_error("Invalid project_id or scene data")
            
            # 2. Execute business logic
            adapter = WanGPAdapter()
            if not adapter.disponivel():
                return self._build_error("WanGP not available", project_id=project_id)
            
            # Use safe preset for 6GB VRAM
            if preset is None:
                from app.hardware import get_recommended_preset
                from app.hardware import get_gpu_info
                gpu = get_gpu_info()
                preset = get_recommended_preset(gpu["vram_gb"], gpu["name"])
            
            # Render scene
            result = adapter.render_scene(project_id, scene, preset)
            
            # 3. Return result with status
            return self._build_success(
                data={
                    "video_path": result.get("video_path"),
                    "scene_id": scene.get("id"),
                    "preset": preset.get("model", "1.3B")
                },
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id and scene."""
        project_id = kwargs.get("project_id", "")
        scene = kwargs.get("scene", {})
        return bool(project_id and scene and "id" in scene)
