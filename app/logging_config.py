import logging
from pathlib import Path

def setup_logger(name="galflowai", log_file=None):
    if log_file is None:
        log_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "galflowai.log"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger
