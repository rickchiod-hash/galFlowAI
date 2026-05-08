# app/adapters/translator_adapter.py — [NOVO]
# Usar modelo de tradução local via Ollama (sem custo)

from app.logging_config import setup_logger

logger = setup_logger()

FALLBACK_DICT = {
    "produto": "product", "venda": "sale", "boneco": "figure",
    "colecionável": "collectible", "animado": "animated",
    "comercial": "commercial", "vídeo": "video",
    "3d": "3d", "medabee": "medabee", "medabots": "medabots",
    # ... expandir conforme uso
}

class TranslatorAdapter:
    """
    Traduz prompts de cenas do PT-BR para EN para o WanGP.
    Usa Ollama local com modelo leve (ex: gemma:2b ou llama3.2:1b)
    Fallback: tradução por dicionário de termos comuns de comercial
    """
    
    def __init__(self):
        self.ollama_available = self._check_ollama()
    
    def _check_ollama(self) -> bool:
        try:
            import subprocess
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def traduzir(self, texto_ptbr: str) -> str:
        """Traduz texto do PT-BR para EN"""
        if self.ollama_available:
            try:
                import subprocess
                prompt = "Translate to English (only output the translation): {}".format(texto_ptbr)
                result = subprocess.run(
                    ["ollama", "run", "gemma:2b", prompt],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    translated = result.stdout.strip()
                    logger.info("Traduzido via Ollama: %s", translated[:50])
                    return translated
            except Exception as e:
                logger.warning("CAUSA: Erro Ollama: %s | CORREÇÃO: Verifique se Ollama está rodando e modelo disponível", str(e))
        
        # Fallback: dicionário
        return self._traduzir_fallback(texto_ptbr)
    
    def _traduzir_fallback(self, texto: str) -> str:
        """Tradução básica por substituição de palavras"""
        result = texto.lower()
        for pt, en in FALLBACK_DICT.items():
            result = result.replace(pt, en)
        return result.capitalize()
