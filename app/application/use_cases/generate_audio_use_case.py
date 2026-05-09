"""Use case for generating audio narration."""
from typing import Dict, Any
from app.application.use_cases.base_use_case import BaseUseCase
from app.adapters.tts_adapter import TTSAdapter

class GenerateAudioUseCase(BaseUseCase):
    """Generate audio narration for scenes.
    
    3-point standard:
    1. Validate script text and project_id
    2. Generate audio using TTS adapter
    3. Save audio file and return path
    """
    
    def execute(self, project_id: str, text: str, output_name: str = "narration.mp3") -> Dict[str, Any]:
        """Execute audio generation use case."""
        try:
            # 1. Validate input
            if not self._validate(project_id=project_id, text=text):
                return self._build_error("Invalid project_id or text")
            
            # 2. Execute business logic
            adapter = TTSAdapter()
            audio_path = adapter.generate_audio(text, project_id, output_name)
            
            # 3. Return result with status
            return self._build_success(
                data={
                    "audio_path": str(audio_path) if audio_path else None,
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
