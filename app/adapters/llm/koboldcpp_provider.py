"""
KoboldCpp provider - local server for GGUF models.
"""
import requests
import time
from typing import Optional
from app.adapters.llm.base_provider import BaseLLMProvider

class KoboldCppProvider(BaseLLMProvider):
    """Provider using KoboldCpp local server."""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        super().__init__("KoboldCppProvider")
        self.base_url = base_url.rstrip('/')
    
    def is_available(self) -> bool:
        """Check if KoboldCpp server is running."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/models",
                timeout=2
            )
            self.available = response.status_code == 200
            return self.available
        except Exception as e:
            self.last_error = str(e)
            self.available = False
            return False
    
    def generate(self, prompt: str, timeout: int = 10) -> Optional[str]:
        """Generate script using KoboldCpp."""
        import time
        start = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/generate",
                json={
                    "prompt": f"""Voce e um roteirista profissional. Crie um roteiro para comercial seguindo este formato:

{prompt}

Roteiro:""",
                    "max_length": 1000,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                timeout=timeout
            )
            
            self.last_response_time = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                return data.get("text", "")
            else:
                self.last_error = f"HTTP {response.status_code}"
                return None
                
        except Exception as e:
            self.last_response_time = time.time() - start
            self.last_error = str(e)
            return None
