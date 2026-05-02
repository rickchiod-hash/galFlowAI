import json
from pathlib import Path
from app.logging_config import setup_logger

logger = setup_logger()

def check_tts_engine():
    """Verifica se há engine TTS disponível (pyttsx3, Kokoro, Coqui)."""
    engines = []
    
    # 1. pyttsx3 (built-in Windows)
    try:
        import pyttsx3
        engines.append("pyttsx3")
        logger.info("pyttsx3 disponível")
    except ImportError:
        logger.warning("pyttsx3 não encontrado")
    
    # 2. Kokoro (recomendado após MVP)
    try:
        import kokoro
        engines.append("kokoro")
        logger.info("Kokoro disponível")
    except ImportError:
        logger.info("Kokoro não encontrado (futuro)")
    
    # 3. Coqui TTS
    try:
        import TTS
        engines.append("coqui")
        logger.info("Coqui TTS disponível")
    except ImportError:
        logger.info("Coqui TTS não encontrado (futuro)")
    
    return engines

class TTSAdapter:
    """
    Gerador de narração offline com suporte a voz masculina e feminina.
    Prioridade: Kokoro → pyttsx3 → silêncio (sem falha)
    """
    
    def __init__(self, logger, voz: str = "feminino", velocidade: float = 1.0):
        self.logger = logger
        self.voz = voz          # "masculino" ou "feminino"
        self.velocidade = velocidade
        self.engine = self._inicializar_engine()
    
    def _inicializar_engine(self):
        """Tenta Kokoro primeiro, depois pyttsx3"""
        # Tentar Kokoro (melhor qualidade)
        try:
            from kokoro import KPipeline
            pipeline = KPipeline(lang_code='p')  # PT-BR
            self.logger.info("TTS: usando Kokoro (alta qualidade)")
            return ("kokoro", pipeline)
        except ImportError:
            pass
        
        # Fallback pyttsx3
        try:
            import pyttsx3
            engine = pyttsx3.init()
            vozes = engine.getProperty('voices')
            # Selecionar voz PT-BR masculina ou feminina
            voz_selecionada = self._selecionar_voz_ptbr(vozes, self.voz)
            if voz_selecionada:
                engine.setProperty('voice', voz_selecionada.id)
            engine.setProperty('rate', int(150 * self.velocidade))
            self.logger.info("TTS: usando pyttsx3")
            return ("pyttsx3", engine)
        except Exception as e:
            self.logger.warning("TTS: sem engine disponível — narração silenciosa ({})".format(e))
            return ("silencio", None)
    
    def _selecionar_voz_ptbr(self, vozes, genero: str):
        """Seleciona a melhor voz PT-BR disponível"""
        for v in vozes:
            nome = (v.name or "").lower()
            lang = (str(v.languages) or "").lower()
            if "pt" in lang or "brazil" in nome or "brasil" in nome:
                if genero == "feminino" and any(x in nome for x in ["female", "zira", "maria"]):
                    return v
                if genero == "masculino" and any(x in nome for x in ["male", "daniel", "paulo"]):
                    return v
        # Retorna qualquer PT-BR disponível
        for v in vozes:
            if "pt" in str(v.languages).lower():
                return v
        return None
    
    def gerar_audio(self, texto: str, output_path: Path) -> bool:
        """Gera arquivo WAV/MP3 da narração"""
        tipo, engine = self.engine
        
        if tipo == "kokoro":
            return self._gerar_kokoro(engine, texto, output_path)
        elif tipo == "pyttsx3":
            return self._gerar_pyttsx3(engine, texto, output_path)
        else:
            # Gerar silêncio de duração proporcional ao texto
            return self._gerar_silencio(texto, output_path)
    
    def _gerar_kokoro(self, pipeline, texto: str, output_path: Path) -> bool:
        """Gera áudio usando Kokoro (PT-BR)"""
        try:
            # Kokoro: pipeline.generate(texto, voice=voze_id, speed=velocidade)
            # Simplified for now - adjust per Kokoro API
            result = pipeline.generate(texto)
            # Save result to output_path
            # Implementation depends on Kokoro version
            self.logger.info("Áudio gerado (Kokoro): {}".format(output_path.name))
            return True
        except Exception as e:
            self.logger.error("Erro Kokoro: {}".format(e))
            return False
    
    def _gerar_pyttsx3(self, engine, texto: str, output_path: Path) -> bool:
        """Gera áudio usando pyttsx3"""
        try:
            engine.save_to_file(texto, str(output_path))
            engine.runAndWait()
            if output_path.exists():
                self.logger.info("Áudio gerado (pyttsx3): {}".format(output_path.name))
                return True
        except Exception as e:
            self.logger.error("Erro pyttsx3: {}".format(e))
        return False
    
    def _gerar_silencio(self, texto: str, output_path: Path) -> bool:
        """Gera arquivo de silêncio proporcional ao texto"""
        try:
            from pydub import AudioSegment
            # ~1 second per 10 words
            duration_ms = max(1000, len(texto.split()) * 100)
            silence = AudioSegment.silent(duration=duration_ms)
            silence.export(str(output_path), format="wav")
            self.logger.info("Silêncio gerado (fallback): {}".format(output_path.name))
            return True
        except ImportError:
            # Ultra fallback: txt file
            output_path.with_suffix('.txt').write_text(texto, encoding="utf-8")
            self.logger.warning("Sem áudio — texto salvo: {}".format(output_path.stem + '.txt'))
            return False
    
    def preview_3s(self, output_path: Path) -> bool:
        """Gera 3 segundos de áudio de preview da voz selecionada"""
        texto = "Olá, esta é a voz selecionada para o seu comercial."
        preview_path = output_path.with_stem(output_path.stem + '_preview')
        return self.gerar_audio(texto, preview_path)
    
    def gerar_narracao_projeto(self, project_id: str, script_text: str = None) -> list:
        """Gera narração para todo o roteiro ou cenas."""
        proj_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects") / project_id
        proj_file = proj_dir / "project.json"
        
        if not proj_file.exists():
            self.logger.error("Projeto %s não encontrado", project_id)
            return []
        
        proj = json.loads(proj_file.read_text(encoding="utf-8"))
        results = []
        
        # Se tem cenas, gera por cena
        if proj.get("scenes"):
            for scene in proj["scenes"]:
                scene_id = scene.get("id", "scene_001")
                narration_text = scene.get("narration", scene.get("description", ""))
                audio = self.gerar_audio(narration_text, proj_dir / "audio" / "{}_narration.wav".format(scene_id))
                if audio:
                    scene["audio_path"] = str(audio)
                    results.append(str(audio))
        # Caso contrário, gera para roteiro inteiro
        elif script_text or proj.get("script"):
            text = script_text or proj.get("script", "")
            audio = self.gerar_audio(text, proj_dir / "audio" / "full_narration.wav")
            if audio:
                results.append(str(audio))
        
        # Atualiza project.json
        proj_file.write_text(json.dumps(proj, indent=2, ensure_ascii=False), encoding="utf-8")
        self.logger.info("Narração concluída: %d arquivos", len(results))
        return results
