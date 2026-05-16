"""Repository for prompt I/O (save/load prompts to/from disk)."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from app.core.result import Result
from app.config import PROJECTS_DIR
from app.logging_config import setup_logger

logger = setup_logger()


class PromptRepository:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self._prompt_dir: Optional[Path] = None

    @property
    def prompt_dir(self) -> Path:
        if self._prompt_dir is None:
            self._prompt_dir = PROJECTS_DIR / self.project_id / "prompts"
        return self._prompt_dir

    def save_prompts(self, prompts: List[Dict]) -> Result[Path]:
        try:
            self.prompt_dir.mkdir(parents=True, exist_ok=True)

            prompts_file = self.prompt_dir / "prompts.json"
            prompts_file.write_text(
                json.dumps(prompts, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            readable_file = self.prompt_dir / "prompts.txt"
            with open(readable_file, "w", encoding="utf-8") as f:
                for p in prompts:
                    f.write("[Cena %s]\n" % p.get("scene_id", ""))
                    f.write("Prompt: %s\n" % p.get("prompt", ""))
                    f.write("Negativo: %s\n" % p.get("negative_prompt", ""))
                    f.write("Duração: %ss\n\n" % p.get("duration", 0))

            logger.info("Prompts salvos em: %s", prompts_file)
            return Result.success(prompts_file)
        except Exception as e:
            return Result.failure(error=str(e), code="PROMPTS_SAVE_FAILED")

    def load_prompts(self) -> Result[List[Dict]]:
        try:
            prompts_file = self.prompt_dir / "prompts.json"
            if not prompts_file.exists():
                return Result.failure(error="No prompts file found", code="PROMPTS_NOT_FOUND")
            prompts = json.loads(prompts_file.read_text(encoding="utf-8"))
            return Result.success(prompts)
        except Exception as e:
            return Result.failure(error=str(e), code="PROMPTS_LOAD_FAILED")
