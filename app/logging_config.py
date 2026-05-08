import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

NIVEIS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "aviso": logging.WARNING,
    "erro": logging.ERROR,
}

class ColorConsoleHandler(logging.StreamHandler):
    """Handler com cores ANSI para o console Windows"""
    CORES = {
        logging.DEBUG:   "\033[36m",   # Ciano
        logging.INFO:    "\033[32m",   # Verde
        logging.WARNING: "\033[33m",   # Amarelo
        logging.ERROR:   "\033[31m",   # Vermelho
    }
    RESET = "\033[0m"
    
    def emit(self, record):
        cor = self.CORES.get(record.levelno, "")
        record.levelname = self._traduzir_nivel(record.levelname)
        record.msg = f"{cor}{record.msg}{self.RESET}"
        super().emit(record)
    
    def _traduzir_nivel(self, nivel):
        return {"DEBUG": "DEBUG", "INFO": "INFO", 
                "WARNING": "AVISO", "ERROR": "ERRO"}.get(nivel, nivel)

def setup_logger(name="galflowai", nivel="info", projeto_id=None):
    """
    Configura logs em 3 destinos:
    1. Console: colorido, humano legível, em PT-BR
    2. Arquivo geral: <BASE_DIR>/logs/galflowai.log
    3. Arquivo do projeto: <BASE_DIR>/projects/<id>/logs/pipeline.log
    """
    from app.config import BASE_DIR
    
    formato_console = "%(asctime)s [%(levelname)s] %(message)s"
    formato_arquivo = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    
    logger = logging.getLogger(name)
    logger.setLevel(NIVEIS.get(nivel, logging.INFO))
    
    # Handler console com cores
    if not any(isinstance(h, ColorConsoleHandler) for h in logger.handlers):
        console = ColorConsoleHandler()
        console.setFormatter(logging.Formatter(formato_console, datefmt="%H:%M:%S"))
        logger.addHandler(console)
    
    # Handler arquivo geral (rotação por tamanho)
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) for h in logger.handlers):
        log_dir = BASE_DIR / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        arquivo_geral = logging.handlers.RotatingFileHandler(
            log_dir / "galflowai.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        arquivo_geral.setFormatter(logging.Formatter(formato_arquivo))
        logger.addHandler(arquivo_geral)
    
    # Handler arquivo do projeto (se fornecido)
    if projeto_id:
        proj_log_dir = BASE_DIR / "projects" / projeto_id / "logs"
        proj_log_dir.mkdir(parents=True, exist_ok=True)
        arquivo_proj = logging.FileHandler(
            proj_log_dir / "pipeline.log", encoding="utf-8")
        arquivo_proj.setFormatter(logging.Formatter(formato_arquivo))
        logger.addHandler(arquivo_proj)
    
    return logger

def emitir_log_websocket(logger, tipo, msg, **kwargs):
    """Emite evento WebSocket para o frontend."""
    import json
    from datetime import datetime
    data = {
        "tipo": "log",
        "nivel": kwargs.get("level", "info"),
        "msg": msg,
        "ts": datetime.now().strftime("%H:%M:%S")
    }
    # Aqui seria emitido via WebSocket (implementar conforme necessário)
    logger.debug(f"WS emit: {json.dumps(data)}")

def log_progresso(logger, etapa, progresso, **kwargs):
    """Log de progresso para o frontend."""
    data = {
        "tipo": "progresso",
        "etapa": etapa,
        "progresso": progresso,
        "sub_progresso": kwargs.get("sub_progresso", 0),
        "tempo_decorrido": kwargs.get("tempo_decorrido", 0),
        "tempo_estimado": kwargs.get("tempo_estimado", 0)
    }
    logger.info(f"Progresso: {etapa} {progresso}%")
    # Aqui seria emitido via WebSocket
