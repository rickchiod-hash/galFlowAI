"""Adapter para Piper TTS - Motor de síntese de fala offline e de alta qualidade"""

import os
import sys
import logging
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class PiperAdapter:
    """Adapter para geração de áudio usando Piper TTS"""
    
    def __init__(self, piper_path: Optional[str] = None, voices_dir: Optional[str] = None):
        """
        Inicializa o adapter Piper TTS.
        
        Args:
            piper_path: Caminho para o executável piper (opcional, será detectado)
            voices_dir: Diretório contendo as vozes do Piper (opcional)
        """
        self.piper_path = piper_path or self._find_piper_executable()
        self.voices_dir = voices_dir or self._find_voices_directory()
        self.available = self._check_availability()
        self.available_voices = self._detect_available_voices() if self.available else []
        
        logger.info(f"PiperAdapter inicializado - Disponível: {self.available}")
        if self.available:
            logger.info(f"Piper encontrado em: {self.piper_path}")
            logger.info(f"Vozes disponíveis: {len(self.available_voices)}")
    
    def _find_piper_executable(self) -> Optional[str]:
        """Localiza o executável piper no sistema"""
        # Possíveis caminhos para o piper
        possible_paths = [
            # No diretório do projeto
            "piper",
            "./piper",
            "../piper",
            # No PATH do sistema
            "piper.exe",
            # Em diretórios comuns de instalação
            os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "piper", "piper.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "piper", "piper.exe"),
            # No diretório de ferramentas do projeto
            os.path.join(os.getcwd(), "tools", "piper", "piper.exe"),
            os.path.join(os.getcwd(), "piper", "piper.exe"),
        ]
        
        for path in possible_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
                
        # Tentar encontrar no PATH
        try:
            result = subprocess.run(["where", "piper"], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except Exception:
            pass
            
        return None
    
    def _find_voices_directory(self) -> Optional[str]:
        """Localiza o diretório com as vozes do Piper"""
        # Possíveis locais para as vozes
        possible_dirs = [
            # No diretório do projeto
            "./voices",
            "../voices",
            "voices",
            # Em diretórios comuns
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "piper", "voices"),
            os.path.join(os.environ.get("APPDATA", ""), "piper", "voices"),
            # No diretório de modelos do projeto
            os.path.join(os.getcwd(), "models", "piper", "voices"),
            os.path.join(os.getcwd(), "piper", "voices"),
            # No cache do HuggingFace (se baixado via huggingface_hub)
            os.path.join(os.environ.get("HF_HOME", ""), "piper", "voices"),
        ]
        
        for dir_path in possible_dirs:
            if os.path.isdir(dir_path):
                # Verificar se contém arquivos de voz (.onnx e .json)
                onnx_files = list(Path(dir_path).glob("*.onnx"))
                json_files = list(Path(dir_path).glob("*.json"))
                if onnx_files and json_files:
                    return dir_path
                    
        return None
    
    def _check_availability(self) -> bool:
        """Verifica se o Piper está disponível e funcional"""
        if not self.piper_path or not os.path.isfile(self.piper_path):
            logger.warning("Executável Piper não encontrado")
            return False
            
        if not self.voices_dir or not os.path.isdir(self.voices_dir):
            logger.warning("Diretório de vozes Piper não encontrado")
            return False
            
        # Testar se o piper funciona
        try:
            result = subprocess.run([self.piper_path, "--help"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Erro ao testar Piper: {e}")
            return False
    
    def _detect_available_voices(self) -> List[Dict[str, str]]:
        """Detecta as vozes disponíveis no diretório de vozes"""
        voices = []
        
        if not self.voices_dir or not os.path.isdir(self.voices_dir):
            return voices
            
        try:
            # Procurar por pares .onnx + .json
            for onnx_file in Path(self.voices_dir).glob("*.onnx"):
                voice_name = onnx_file.stem
                json_file = Path(self.voices_dir) / f"{voice_name}.json"
                
                if json_file.exists():
                    try:
                        # Ler metadados da voz
                        with open(json_file, 'r', encoding='utf-8') as f:
                            voice_data = json.load(f)
                        
                        voices.append({
                            "name": voice_name,
                            "language": voice_data.get("language", "unknown"),
                            "speaker_id": voice_data.get("speaker_id", 0),
                            "quality": voice_data.get("quality", "unknown"),
                            "onnx_path": str(onnx_file),
                            "json_path": str(json_file)
                        })
                    except Exception as e:
                        logger.warning(f"Erro ao ler metadados da voz {voice_name}: {e}")
                        # Adicionar voz mesmo sem metadados
                        voices.append({
                            "name": voice_name,
                            "language": "unknown",
                            "speaker_id": 0,
                            "quality": "unknown",
                            "onnx_path": str(onnx_file),
                            "json_path": str(json_file) if json_file.exists() else ""
                        })
                        
        except Exception as e:
            logger.error(f"Erro ao detectar vozes Piper: {e}")
            
        return voices
    
    def is_available(self) -> bool:
        """Retorna se o Piper TTS está disponível"""
        return self.available
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Retorna lista de vozes disponíveis"""
        return self.available_voices
    
    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        language: str = "pt",
        speaker_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Gera áudio a partir de texto usando Piper TTS.
        
        Args:
            text: Texto para narrar
            output_path: Caminho para salvar o áudio (WAV)
            voice: Nome da voz a ser usada (opcional)
            speed: Velocidade da fala (1.0 = normal, 0.5 = metade, 2.0 = dobro)
            language: Idioma ("pt", "en", etc.) - usado para seleção automática de voz
            speaker_id: ID do falante (opcional, sobrescreve voice se fornecido)
            
        Returns:
            Dict com status e metadados
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "Piper TTS não está disponível",
                "engine": "piper"
            }
        
        if not text or not text.strip():
            return {
                "success": False,
                "error": "Texto vazio fornecido",
                "engine": "piper"
            }
        
        # Determinar qual voz usar
        selected_voice = None
        selected_speaker_id = speaker_id
        
        if voice:
            # Procurar voz pelo nome
            for v in self.available_voices:
                if v["name"] == voice:
                    selected_voice = v
                    selected_speaker_id = v.get("speaker_id")
                    break
            
            if not selected_voice:
                logger.warning(f"Voz '{voice}' não encontrada, usando primeira disponível")
        elif self.available_voices:
            # Usar primeira voz disponível se nenhuma especificada
            selected_voice = self.available_voices[0]
            selected_speaker_id = selected_voice.get("speaker_id")
        
        if not selected_voice and self.available_voices:
            selected_voice = self.available_voices[0]
            selected_speaker_id = selected_voice.get("speaker_id")
        
        if not selected_voice:
            return {
                "success": False,
                "error": "Nenhuma voz Piper disponível",
                "engine": "piper"
            }
        
        # Preparar comando Piper
        cmd = [
            self.piper_path,
            "--model", selected_voice["onnx_path"],
            "--output_file", output_path
        ]
        
        # Adicionar ID do falante se especificado
        if selected_speaker_id is not None:
            cmd.extend(["--speaker", str(selected_speaker_id)])
        
        # Adicionar escala de comprimento (inversamente proporcional à velocidade)
        # Piper usa --length_scale onde 1.0 é normal, >1.0 é mais lento, <1.0 é mais rápido
        length_scale = 1.0 / max(speed, 0.1)  # Evitar divisão por zero
        cmd.extend(["--length_scale", str(length_scale)])
        
        try:
            logger.info(f"Gerando áudio com Piper: voz={selected_voice['name']}, speed={speed}")
            
            # Executar Piper com o texto como entrada
            result = subprocess.run(
                cmd,
                input=text.strip(),
                capture_output=True,
                text=False,  # Vamos lidar com bytes diretamente
                timeout=30  # Timeout de 30 segundos
            )
            
            if result.returncode == 0:
                # Verificar se o arquivo de saída foi criado
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    # Obter duração aproximada do áudio
                    duration_seconds = self._estimate_audio_duration(output_path, text, speed)
                    
                    return {
                        "success": True,
                        "audio_path": output_path,
                        "engine": "piper",
                        "voice": selected_voice["name"],
                        "speaker_id": selected_speaker_id,
                        "speed": speed,
                        "length_scale": length_scale,
                        "duration_seconds": duration_seconds,
                        "text_length": len(text)
                    }
                else:
                    return {
                        "success": False,
                        "error": "Arquivo de áudio não foi gerado",
                        "engine": "piper",
                        "stdout": result.stdout.decode('utf-8', errors='ignore') if result.stdout else "",
                        "stderr": result.stderr.decode('utf-8', errors='ignore') if result.stderr else ""
                    }
            else:
                error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else "Erro desconhecido"
                logger.error(f"Erro Piper: {error_msg}")
                return {
                    "success": False,
                    "error": f"Piper falhou: {error_msg}",
                    "engine": "piper",
                    "stdout": result.stdout.decode('utf-8', errors='ignore') if result.stdout else "",
                    "stderr": error_msg
                }
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao executar Piper")
            return {
                "success": False,
                "error": "Timeout ao geráudio com Piper (>30s)",
                "engine": "piper"
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao executar Piper: {e}")
            return {
                "success": False,
                "error": str(e),
                "engine": "piper"
            }
    
    def _estimate_audio_duration(self, audio_path: str, text: str, speed: float) -> float:
        """
        Estima a duração do áudio baseado no texto e velocidade.
        
        Args:
            audio_path: Caminho para o arquivo de áudio gerado
            text: Texto original
            speed: Fator de velocidade usado
            
        Returns:
            Duração estimada em segundos
        """
        try:
            # Tentar obter duração real do arquivo WAV
            import wave
            with wave.open(audio_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                return duration
        except Exception:
            # Fallback: estimativa baseada no texto
            # Taxa média de fala: ~150 palavras por minuto em português
            words = len(text.split())
            base_duration = (words / 150) * 60  # segundos
            return base_duration / max(speed, 0.1)  # Ajustar pela velocidade
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do adapter Piper"""
        return {
            "available": self.is_available(),
            "engine": "piper",
            "piper_path": self.piper_path,
            "voices_dir": self.voices_dir,
            "available_voices_count": len(self.available_voices),
            "available_voices": [{"name": v["name"], "language": v["language"]} 
                               for v in self.available_voices[:5]]  # Primeiras 5 vozes
        }

# Função de conveniência para criar instância padrão
def create_piper_adapter() -> PiperAdapter:
    """Cria e retorna uma instância padrão do PiperAdapter"""
    return PiperAdapter()

# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    adapter = PiperAdapter()
    
    if adapter.is_available():
        print(f"Piper disponível com {len(adapter.get_available_voices())} vozes")
        for voice in adapter.get_available_voices()[:3]:
            print(f"  - {voice['name']} ({voice['language']})")
        
        # Teste de geração de áudio
        test_text = "Olá, este é um teste do Piper TTS."
        output_file = "test_piper_output.wav"
        
        result = adapter.generate_audio(test_text, output_file)
        if result["success"]:
            print(f"Áudio gerado com sucesso: {output_file}")
            print(f"Duração: {result.get('duration_seconds', 0):.2f}s")
        else:
            print(f"Erro ao gerar áudio: {result['error']}")
    else:
        print("Piper TTS não está disponível")
        print("Para instalar:")
        print("  1. Baixe o Piper de: https://github.com/rhasspy/piper")
        print("  2. Baixe vozes de: https://huggingface.co/rhasspy/piper-voices")
        print("  3. Coloque o executável piper.exe em um diretório acessível")
        print("  4. Coloque as vozes (.onnx + .json) em um diretório de vozes")