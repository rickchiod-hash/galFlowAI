import shutil
from pathlib import Path
from datetime import datetime

def backup_file(file_path: Path) -> Path | None:
    """Cria backup do arquivo em .backup/ com timestamp antes de sobrescrever."""
    if not file_path.exists():
        return None
    backup_dir = file_path.parent / ".backup"
    backup_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{ts}{file_path.suffix}"
    backup_path = backup_dir / backup_name
    shutil.copy2(file_path, backup_path)
    return backup_path
