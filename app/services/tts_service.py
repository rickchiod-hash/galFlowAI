"""TTS Service - Geração de áudio offline usando pyttsx3"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TTSService:
    """Serviço para geração de áudio offline (TTS)"""
    
    def __init__(self):
        self.available = self._check_available()
        self.engine = None
        if self.available:
            self._init_engine()
    
    def _check_available(self) -> bool:
        """Verifica se pyttsx3 está disponível"""
        try:
            import pyttsx3
            return True
        except ImportError:
            logger.warning("pyttsx3 não instalado. TTS offline indisponível.")
            return False
    
    def _init_engine(self):
        """Inicializa o motor TTS"""
        if not self.available:
            return
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            # Configurações padrão
            self.engine.setProperty('rate', 150)    # Velocidade da fala
            self.engine.setProperty('volume', 0.9)  # Volume (0.0 a 1.0)
            logger.info("TTS engine inicializado com sucesso")
        except Exception as e:
            logger.error("Erro ao inicializar TTS: %s", e)
            self.available = False
            self.engine = None
    
    def is_available(self) -> bool:
        """Retorna se TTS está disponível"""
        return self.available and self.engine is not None
    
    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        rate: int = 150,
        volume: float = 0.9
    ) -> Dict[str, Any]:
        """
        Gera arquivo de áudio a partir de texto.
        
        Args:
            text: Texto para narrar
            output_path: Caminho para salvar o áudio
            voice: Nome da voz (opcional)
            rate: Velocidade da fala (palavras por minuto)
            volume: Volume (0.0 a 1.0)
            
        Returns:
            Dict com status e metadados
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "TTS não disponível",
                "fallback_suggested": True
            }
        
        try:
            # Configura propriedades
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            if voice:
                voices = self.engine.getProperty('voices')
                for v in voices:
                    if voice.lower() in v.name.lower():
                        self.engine.setProperty('voice', v.id)
                        break
            
            # Gera áudio
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            
            self.engine.save_to_file(text, str(output))
            self.engine.runAndWait()
            
            if output.exists():
                logger.info("Áudio gerado: %s", output.name)
                return {
                    "success": True,
                    "audio_path": str(output),
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "provider": "pyttsx3"
                }
            else:
                return {
                    "success": False,
                    "error": "Arquivo de áudio não foi criado"
                }
                
        except Exception as e:
            logger.error("Erro ao gerar áudio: %s", e)
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_available_voices(self) -> list:
        """Retorna lista de vozes disponíveis"""
        if not self.is_available():
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{"id": v.id, "name": v.name, "lang": v.languages} for v in voices]
        except Exception as e:
            logger.error("Erro ao listar vozes: %s", e)
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do serviço TTS"""
        return {
            "available": self.is_available(),
            "provider": "pyttsx3",
            "offline": True,
            "voices_count": len(self.get_available_voices()) if self.is_available() else 0
        }
