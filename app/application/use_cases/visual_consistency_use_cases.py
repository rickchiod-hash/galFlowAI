"""Use cases for Visual Consistency (V2.6 / H17)."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base import UseCase
from pydantic import BaseModel, Field
from pathlib import Path
import json


class VisualBible(BaseModel):
    """Visual Bible for brand consistency."""
    project_id: str
    version: str = "1.0"
    created_at: str = ""
    
    # Visual identity
    color_palette: List[str] = Field(default_factory=lambda: ["#FFFFFF", "#000000"])
    fonts: List[str] = Field(default_factory=lambda: ["Arial", "Helvetica"])
    style_keywords: List[str] = Field(default_factory=lambda: ["cinematic", "modern"])
    
    # Brand elements
    logo_path: str = ""
    reference_images: List[str] = Field(default_factory=list)
    
    # Scene consistency
    scene_templates: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    negative_prompt_base: str = "blurry, low quality, static, bad anatomy, distorted"


class SceneContract(BaseModel):
    """Contract for scene generation."""
    scene_id: str
    scene_number: int
    description: str
    duration: int = 5
    
    # Visual consistency
    prompt_pos: str = ""
    prompt_neg: str = ""
    style: str = "cinematic"
    
    # Metadata
    source_script: str = ""
    visual_bible_version: str = "1.0"


class CreateVisualBibleUseCase(UseCase):
    """Create Visual Bible for project.
    
    3-point standard:
    1. Validate project_id and visual elements
    2. Create Visual Bible with defaults
    3. Save to disk and return
    """
    
    def __init__(self):
        super().__init__()
        self.bibles_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/projects")
    
    def execute(
        self,
        project_id: str,
        color_palette: Optional[List[str]] = None,
        style_keywords: Optional[List[str]] = None,
        logo_path: str = ""
    ) -> Dict[str, Any]:
        """Execute create Visual Bible."""
        try:
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            bible = VisualBible(
                project_id=project_id,
                color_palette=color_palette or ["#FFFFFF", "#000000"],
                style_keywords=style_keywords or ["cinematic", "modern"],
                logo_path=logo_path
            )
            
            self._save_bible(bible)
            
            return self._build_success(data=bible.dict())
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        return bool(project_id)
    
    def _save_bible(self, bible: VisualBible):
        """Save Visual Bible to disk."""
        bible_dir = self.bibles_dir / bible.project_id / "visual"
        bible_dir.mkdir(parents=True, exist_ok=True)
        
        bible_path = bible_dir / "visual_bible.json"
        bible_path.write_text(
            json.dumps(bible.dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


class GenerateScenePromptsUseCase(UseCase):
    """Generate scene prompts with visual consistency.
    
    3-point standard:
    1. Validate script, scenes, and Visual Bible
    2. Generate prompts with anti-hallucination
    3. Return scene contracts
    """
    
    def __init__(self):
        super().__init__()
        self.bibles_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/projects")
    
    def execute(
        self,
        project_id: str,
        script: str,
        scenes: List[Dict[str, Any]],
        visual_bible: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute generate scene prompts."""
        try:
            if not self._validate(project_id=project_id, script=script, scenes=scenes):
                return self._build_error("Invalid parameters")
            
            # Load or use provided Visual Bible
            bible_data = visual_bible or self._load_bible(project_id)
            
            # Generate scene contracts
            contracts = []
            for i, scene in enumerate(scenes):
                contract = self._build_scene_contract(
                    scene=scene,
                    scene_number=i+1,
                    script=script,
                    bible_data=bible_data
                )
                contracts.append(contract.dict())
            
            # Save contracts
            self._save_contracts(project_id, contracts)
            
            return self._build_success(data={
                "scene_contracts": contracts,
                "count": len(contracts),
                "visual_bible_version": bible_data.get("version", "1.0") if bible_data else "none"
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        script = kwargs.get("script", "")
        scenes = kwargs.get("scenes", [])
        return bool(project_id) and bool(script) and isinstance(scenes, list)
    
    def _load_bible(self, project_id: str) -> Optional[Dict]:
        """Load Visual Bible from disk."""
        bible_path = self.bibles_dir / project_id / "visual" / "visual_bible.json"
        if not bible_path.exists():
            return None
        try:
            return json.loads(bible_path.read_text(encoding="utf-8"))
        except:
            return None
    
    def _build_scene_contract(
        self,
        scene: Dict[str, Any],
        scene_number: int,
        script: str,
        bible_data: Optional[Dict]
    ) -> SceneContract:
        """Build scene contract with visual consistency."""
        scene_id = scene.get("id", f"scene_{scene_number}")
        description = scene.get("description", scene.get("prompt", ""))
        duration = scene.get("duration", 5)
        
        # Build positive prompt with visual consistency
        style = bible_data.get("style_keywords", ["cinematic"])[0] if bible_data else "cinematic"
        prompt_pos = f"{description}, {style} style, high quality"
        
        # Add color palette if available
        if bible_data and bible_data.get("color_palette"):
            colors = ", ".join(bible_data["color_palette"][:3])
            prompt_pos += f", colors: {colors}"
        
        # Build negative prompt (anti-hallucination)
        neg_base = bible_data.get("negative_prompt_base", "") if bible_data else ""
        prompt_neg = f"{neg_base}, inconsistent lighting, color mismatch, brand violation"
        
        # Add Brazilian Portuguese negative prompt for anti-hallucination
        prompt_neg += ", borrão, baixa qualidade, estático, má anatomia, distorcido, inconsciente"
        
        return SceneContract(
            scene_id=scene_id,
            scene_number=scene_number,
            description=description,
            duration=duration,
            prompt_pos=prompt_pos,
            prompt_neg=prompt_neg,
            style=style,
            source_script=script[:100],
            visual_bible_version=bible_data.get("version", "1.0") if bible_data else "none"
        )
    
    def _save_contracts(self, project_id: str, contracts: List[Dict]):
        """Save scene contracts to disk."""
        contracts_dir = self.bibles_dir / project_id / "contracts"
        contracts_dir.mkdir(parents=True, exist_ok=True)
        
        contracts_path = contracts_dir / "scene_contracts.json"
        contracts_path.write_text(
            json.dumps(contracts, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


class ValidateVisualConsistencyUseCase(UseCase):
    """Validate visual consistency across scenes.
    
    3-point standard:
    1. Validate scene contracts
    2. Check consistency rules
    3. Return validation results
    """
    
    def __init__(self):
        super().__init__()
    
    def execute(self, contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute visual consistency validation."""
        try:
            if not self._validate(contracts=contracts):
                return self._build_error("Invalid contracts")
            
            issues = []
            
            # Check all scenes have required fields
            for i, contract in enumerate(contracts):
                if not contract.get("prompt_pos"):
                    issues.append(f"Scene {i+1} missing prompt_pos")
                if not contract.get("prompt_neg"):
                    issues.append(f"Scene {i+1} missing prompt_neg")
                if not contract.get("style"):
                    issues.append(f"Scene {i+1} missing style")
            
            # Check style consistency
            styles = set(c.get("style", "") for c in contracts)
            if len(styles) > 1:
                issues.append(f"Multiple styles detected: {', '.join(styles)}")
            
            is_valid = len(issues) == 0
            
            return self._build_success(data={
                "valid": is_valid,
                "issues": issues,
                "scene_count": len(contracts),
                "styles_detected": list(styles)
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        contracts = kwargs.get("contracts", [])
        return isinstance(contracts, list) and len(contracts) > 0
