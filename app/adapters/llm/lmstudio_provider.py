"""
LM Studio provider - local server at localhost:1234.
"""
import requests
import time
from typing import Optional
from app.adapters.llm.base_provider import BaseLLMProvider

class LMStudioProvider(BaseLLMProvider):
    """Provider using LM Studio local server."""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        super().__init__("LMStudioProvider")
        self.base_url = base_url.rstrip('/')
        self.api_key = "local"  # Fake key for OpenAI-compatible clients
    
    def is_available(self) -> bool:
        """Check if LM Studio server is running."""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                timeout=2
            )
            self.available = response.status_code == 200
            return self.available
        except Exception as e:
            self.last_error = str(e)
            self.available = False
            return False
    
    def generate(self, prompt: str, timeout: int = 10) -> Optional[str]:
        """Generate script using LM Studio."""
        import time
        start = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "local-model",
                    "messages": [
                        {"role": "system", "content": "Voce e um roteirista profissional especializado em comerciais curtos para redes sociais. Crie roteiros estruturados com cenas, tempos, textos na tela, narracao e prompts visuais."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=timeout
            )
            
            self.last_response_time = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                self.last_error = f"HTTP {response.status_code}: {response.text}"
                return None
                
        except Exception as e:
            self.last_response_time = time.time() - start
            self.last_error = str(e)
            return None
