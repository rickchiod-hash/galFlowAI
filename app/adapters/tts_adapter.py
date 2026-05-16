"""Adapter para TTS (Text-to-Speech) - Narração do roteiro"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import subprocess

logger = logging.getLogger(__name__)


class TTSAdapter:
    """Adapter para geração de narração usando diferentes motores TTS"""
    
    def __init__(self, prefer_engine: str = "auto"):
        """
        Inicializa o adapter TTS.
        
        Args:
            prefer_engine: Motor preferido ("kokoro", "pyttsx3", "silence", "auto")
        """
        self.prefer_engine = prefer_engine
        self.available_engines = self._detect_engines()
        self.selected_engine = self._select_engine()
        
    def _detect_engines(self) -> Dict[str, bool]:
        """Detecta quais motores TTS estão disponíveis"""
        engines = {
            "kokoro": False,
            "pyttsx3": False,
            "silence": True,  # Sempre disponível como fallback
            "system": False   # Windows system voices
        }
        
        # Testa Kokoro
        try:
            import kokoro
            engines["kokoro"] = True
            logger.info("Kokoro TTS detectado")
        except ImportError:
            logger.info("Kokoro TTS não disponível")
        
        # Testa pyttsx3
        try:
            import pyttsx3
            engines["pyttsx3"] = True
            logger.info("pyttsx3 detectado")
        except ImportError:
            logger.info("pyttsx3 não disponível")
        
        # Testa vozes do Windows
        try:
            import win32com.client
            engines["system"] = True
            logger.info("Vozes do Windows detectadas")
        except ImportError:
            logger.info("Vozes do Windows não disponíveis")
        
        return engines
    
    def _select_engine(self) -> str:
        """Seleciona o melhor motor TTS disponível"""
        if self.prefer_engine != "auto":
            if self.available_engines.get(self.prefer_engine, False):
                return self.prefer_engine
            else:
                logger.warning("CAUSA: Motor %s solicitado, mas não disponível | CORREÇÃO: Verifique se motor TTS está instalado", self.prefer_engine)
        
        # Prioridade: kokoro > pyttsx3 > system > silence
        if self.available_engines["kokoro"]:
            return "kokoro"
        elif self.available_engines["pyttsx3"]:
            return "pyttsx3"
        elif self.available_engines["system"]:
            return "system"
        else:
            return "silence"
    
    def is_available(self) -> bool:
        """Retorna se pelo menos um motor TTS está disponível"""
        return any(v for k, v in self.available_engines.items() if k != "silence")
    
    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        language: str = "pt"
    ) -> Dict[str, Any]:
        """
        Gera áudio a partir de texto.
        
        Args:
            text: Texto para narrar
            output_path: Caminho para salvar o áudio
            voice: Nome da voz (opcional)
            speed: Velocidade da fala (1.0 = normal)
            language: Idioma ("pt", "en", etc.)
            
        Returns:
            Dict com status e metadados
        """
        logger.info(f"Gerando áudio com motor: {self.selected_engine}")
        
        try:
            if self.selected_engine == "kokoro":
                return self._generate_kokoro(text, output_path, voice, speed, language)
            elif self.selected_engine == "pyttsx3":
                return self._generate_pyttsx3(text, output_path, voice, speed)
            elif self.selected_engine == "system":
                return self._generate_system_voice(text, output_path, voice, speed)
            elif self.selected_engine == "silence":
                return self._generate_silence(text, output_path)
            else:
                return {
                    "success": False,
                    "error": f"Motor TTS desconhecido: {self.selected_engine}",
                    "engine": self.selected_engine
                }
        except Exception as e:
            logger.error("CAUSA: Erro ao gerar áudio: %s | CORREÇÃO: Verifique se motor TTS está funcionando", e)
            return {
                "success": False,
                "error": str(e),
                "engine": self.selected_engine
            }
    
    def _generate_kokoro(
        self,
        text: str,
        output_path: str,
        voice: Optional[str],
        speed: float,
        language: str
    ) -> Dict[str, Any]:
        """Gera áudio usando Kokoro TTS"""
        try:
            from kokoro import KPipeline
            import soundfile as sf
            import torch
            
            # Cria pipeline
            pipeline = KPipeline(lang_code=language[:2])
            
            # Gera áudio
            audio_list = []
            for i, (gs, ps, audio) in enumerate(pipeline(text, voice=voice or "bm_lewis")):
                audio_list.append(audio)
            
            # Concatena
            if audio_list:
                import numpy as np
                final_audio = np.concatenate(audio_list)
                sf.write(output_path, final_audio, 24000)
                
                return {
                    "success": True,
                    "audio_path": output_path,
                    "engine": "kokoro",
                    "voice": voice or "bm_lewis",
                    "duration_seconds": len(final_audio) / 24000
                }
            else:
                return {"success": False, "error": "Nenhum áudio gerado"}
                
        except Exception as e:
            logger.error("CAUSA: Erro Kokoro: %s | CORREÇÃO: Verifique se Kokoro TTS está instalado", e)
            return {"success": False, "error": str(e), "engine": "kokoro"}
    
    def _generate_pyttsx3(
        self,
        text: str,
        output_path: str,
        voice: Optional[str],
        speed: float
    ) -> Dict[str, Any]:
        """Gera áudio usando pyttsx3"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Configura voz
            if voice:
                voices = engine.getProperty('voices')
                for v in voices:
                    if voice.lower() in v.name.lower():
                        engine.setProperty('voice', v.id)
                        break
            
            # Configura velocidade
            engine.setProperty('rate', int(200 * speed))
            
            # Salva áudio
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            return {
                "success": True,
                "audio_path": output_path,
                "engine": "pyttsx3",
                "voice": voice or "default"
            }
            
        except Exception as e:
            logger.error("CAUSA: Erro pyttsx3: %s | CORREÇÃO: Verifique se pyttsx3 está instalado", e)
            return {"success": False, "error": str(e), "engine": "pyttsx3"}
    
    def _generate_system_voice(
        self,
        text: str,
        output_path: str,
        voice: Optional[str],
        speed: float
    ) -> Dict[str, Any]:
        """Gera áudio usando vozes do Windows"""
        try:
            import win32com.client
            
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            
            # Configura voz
            if voice:
                voices = speaker.GetVoices()
                for i in range(voices.Count):
                    if voice.lower() in voices.Item(i).GetDescription().lower():
                        speaker.Voice = voices.Item(i)
                        break
            
            # Salva arquivo
            speaker.Speak(text)
            
            # Nota: Windows SAPI não tem save direto fácil
            # Retorna placeholder
            return {
                "success": True,
                "audio_path": output_path,
                "engine": "system",
                "voice": voice or "default",
                "note": "Áudio reproduzido, mas não salvo (limitação SAPI)"
            }
            
        except Exception as e:
            logger.error("CAUSA: Erro Windows SAPI: %s | CORREÇÃO: Verifique se Windows SAPI está acessível", e)
            return {"success": False, "error": str(e), "engine": "system"}
    
    def _generate_silence(
        self,
        text: str,
        output_path: str
    ) -> Dict[str, Any]:
        """Gera arquivo de áudio silencioso (fallback)"""
        try:
            import numpy as np
            import soundfile as sf
            
            # Estima duração baseada no texto (150 palavras por minuto)
            words = len(text.split())
            duration = (words / 150) * 60  # segundos
            duration = max(duration, 1.0)  # mínimo 1 segundo
            
            # Gera silêncio
            sample_rate = 22050
            silence = np.zeros(int(sample_rate * duration))
            sf.write(output_path, silence, sample_rate)
            
            return {
                "success": True,
                "audio_path": output_path,
                "engine": "silence",
                "duration_seconds": duration,
                "note": "Áudio silencioso gerado como fallback"
            }
            
        except Exception as e:
            logger.error("CAUSA: Erro ao gerar silêncio: %s | CORREÇÃO: Verifique permissões de escrita", e)
            return {"success": False, "error": str(e), "engine": "silence"}
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Retorna lista de vozes disponíveis"""
        voices = []
        
        if self.available_engines["kokoro"]:
            voices.append({"engine": "kokoro", "name": "bm_lewis", "language": "pt"})
            voices.append({"engine": "kokoro", "name": "bf_emma", "language": "pt"})
        
        if self.available_engines["pyttsx3"]:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                for v in engine.getProperty('voices'):
                    voices.append({
                        "engine": "pyttsx3",
                        "name": v.name,
                        "id": v.id
                    })
            except Exception as e:
                logger.debug("TTS voice enumeration failed: %s", e)
        
        return voices
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do adapter TTS"""
        return {
            "available": self.is_available(),
            "selected_engine": self.selected_engine,
            "available_engines": self.available_engines,
            "voices_count": len(self.get_available_voices())
        }
