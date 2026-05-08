"""Use cases for Prompt Context Pack (V2.2 / H14)."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base import UseCase
from pydantic import BaseModel, Field
from datetime import datetime
import json
from pathlib import Path


class PromptContextPack(BaseModel):
    """Schema for Prompt Context Pack."""
    project_id: str
    version: str = "1.0"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Script context
    script_summary: str = ""
    script_tone: str = ""
    script_target_audience: str = ""
    
    # Visual context
    visual_style: str = "cinematic"
    negative_prompt_base: str = "blurry, low quality, static, bad anatomy, distorted"
    reference_assets: List[str] = Field(default_factory=list)
    
    # Scene prompts
    scene_prompts: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Metadata
    engine: str = "wan2gp_1.3b"
    resolution: str = "512x512"
    created_by: str = "system"


class CreatePromptPackUseCase(UseCase):
    """Create a new Prompt Context Pack.
    
    3-point standard:
    1. Validate project_id and script data
    2. Build prompt pack with defaults and scene prompts
    3. Save to disk and return pack
    """
    
    def __init__(self):
        super().__init__()
        self.packs_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/projects")
    
    def execute(
        self,
        project_id: str,
        script: str = "",
        scenes: Optional[List[Dict]] = None,
        visual_style: str = "cinematic"
    ) -> Dict[str, Any]:
        """Execute create prompt pack."""
        try:
            if not self._validate(project_id=project_id, script=script):
                return self._build_error("Invalid project_id or script")
            
            # Build pack
            pack = PromptContextPack(
                project_id=project_id,
                script_summary=script[:200] if script else "",
                visual_style=visual_style
            )
            
            # Build scene prompts if scenes provided
            if scenes:
                for i, scene in enumerate(scenes):
                    scene_prompt = {
                        "scene_id": scene.get("id", f"scene_{i}"),
                        "prompt_pos": scene.get("prompt", ""),
                        "prompt_neg": pack.negative_prompt_base,
                        "duration": scene.get("duration", 5)
                    }
                    pack.scene_prompts.append(scene_prompt)
            
            # Save
            self._save_pack(pack)
            
            return self._build_success(data=pack.dict())
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        return bool(project_id)
    
    def _save_pack(self, pack: PromptContextPack):
        """Save prompt pack to disk."""
        project_dir = self.packs_dir / pack.project_id / "prompts"
        project_dir.mkdir(parents=True, exist_ok=True)
        
        pack_path = project_dir / "prompt_pack.json"
        pack_path.write_text(
            json.dumps(pack.dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


class LoadPromptPackUseCase(UseCase):
    """Load an existing Prompt Context Pack.
    
    3-point standard:
    1. Validate project_id
    2. Load pack from disk
    3. Return pack dict
    """
    
    def __init__(self):
        super().__init__()
        self.packs_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/projects")
    
    def execute(self, project_id: str) -> Dict[str, Any]:
        """Execute load prompt pack."""
        try:
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            pack_path = self.packs_dir / project_id / "prompts" / "prompt_pack.json"
            
            if not pack_path.exists():
                return self._build_error("Prompt pack not found")
            
            data = json.loads(pack_path.read_text(encoding="utf-8"))
            return self._build_success(data=data)
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        return bool(project_id)


class ValidatePromptConsistencyUseCase(UseCase):
    """Validate consistency between script and prompts.
    
    3-point standard:
    1. Validate pack data
    2. Check consistency rules
    3. Return validation results
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self, pack_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute validation."""
        try:
            if not self._validate(pack_data=pack_data):
                return self._build_error("Invalid pack data")
            
            issues = []
            
            # Check scene prompts exist
            if not pack_data.get("scene_prompts"):
                issues.append("No scene prompts found")
            
            # Check negative prompt base exists
            if not pack_data.get("negative_prompt_base"):
                issues.append("Missing negative_prompt_base")
            
            # Check scene prompts have required fields
            for i, scene in enumerate(pack_data.get("scene_prompts", [])):
                if not scene.get("prompt_pos"):
                    issues.append(f"Scene {i} missing prompt_pos")
                if not scene.get("duration"):
                    issues.append(f"Scene {i} missing duration")
            
            is_valid = len(issues) == 0
            
            return self._build_success(
                data={
                    "valid": is_valid,
                    "issues": issues,
                    "scene_count": len(pack_data.get("scene_prompts", []))
                }
            )
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        pack_data = kwargs.get("pack_data")
        return isinstance(pack_data, dict) and bool(pack_data.get("project_id"))
