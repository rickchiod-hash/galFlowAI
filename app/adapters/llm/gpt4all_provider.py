"""
GPT4All provider - local LLM using gpt4all package.
"""
import time
from typing import Optional
from pathlib import Path
from app.adapters.llm.base_provider import BaseLLMProvider

class GPT4AllProvider(BaseLLMProvider):
    """Provider using GPT4All Python package."""
    
    def __init__(self, model_dir: str = "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/models/gpt4all"):
        super().__init__("GPT4AllProvider")
        self.model_dir = Path(model_dir)
        self.model = None
        self.model_name = None
    
    def is_available(self) -> bool:
        """Check if GPT4All is installed and model exists."""
        try:
            from gpt4all import GPT4All
            if not self.model_dir.exists():
                self.last_error = f"Model dir not found: {self.model_dir}"
                self.available = False
                return False
            
            # Check for any model file
            model_files = list(self.model_dir.glob("*.gguf")) + list(self.model_dir.glob("*.bin"))
            if not model_files:
                self.last_error = "No model files found"
                self.available = False
                return False
            
            self.available = True
            return True
        except ImportError:
            self.last_error = "gpt4all package not installed"
            self.available = False
            return False
        except Exception as e:
            self.last_error = str(e)
            self.available = False
            return False
    
    def generate(self, prompt: str, timeout: int = 10) -> Optional[str]:
        """Generate script using GPT4All."""
        import time
        start = time.time()
        
        try:
            from gpt4all import GPT4All
            
            if not self.model:
                model_files = list(self.model_dir.glob("*.gguf")) + list(self.model_dir.glob("*.bin"))
                if not model_files:
                    return None
                self.model_name = model_files[0].name
                self.model = GPT4All(self.model_name, model_path=str(self.model_dir))
            
            response = self.model.generate(
                f"""Voce e um roteirista profissional. Crie um roteiro para comercial:

{prompt}

Roteiro:""",
                max_tokens=1000,
                temp=0.7
            )
            
            self.last_response_time = time.time() - start
            return response
            
        except Exception as e:
            self.last_response_time = time.time() - start
            self.last_error = str(e)
            return None
