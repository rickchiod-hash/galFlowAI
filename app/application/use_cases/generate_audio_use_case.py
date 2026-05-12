"""Use case for generating audio narration."""
from typing import Dict, Any
from pathlib import Path
from app.application.use_cases.base_use_case import BaseUseCase
from app.adapters.tts_adapter import TTSAdapter
from app.config import PROJECTS_DIR

class GenerateAudioUseCase(BaseUseCase):
    """Generate audio narration for scenes.
    
    3-point standard:
    1. Validate script text and project_id
    2. Generate audio using TTS adapter
    3. Save audio file and return path
    """
    
    def execute(self, project_id: str, text: str, output_name: str = "narration.wav") -> Dict[str, Any]:
        """Execute audio generation use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, text=text):
                return self._build_error("Invalid project_id or text")
            
            # 2. Execute business logic
            adapter = TTSAdapter()
            output_path = str(Path(PROJECTS_DIR) / project_id / "audio" / output_name)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            result = adapter.generate_audio(text=text, output_path=output_path)
            
            audio_path = None
            if result.get("success"):
                audio_path = result.get("audio_path", output_path)
            
            # 3. Return result with status
            return self._build_success(
                data={
                    "audio_path": audio_path,
                    "text_length": len(text)
                },
                project_id=project_id
            )
        except Exception as e:
            return self._build_error(str(e), project_id=project_id)
    
    def _validate(self, **kwargs) -> bool:
        """Validate project_id and text."""
        project_id = kwargs.get("project_id", "")
        text = kwargs.get("text", "")
        return bool(project_id and text and len(text.strip()) > 0)
