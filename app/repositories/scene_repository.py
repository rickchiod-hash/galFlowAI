"""Repository for scene I/O (save/load scenes to/from disk)."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from app.core.result import Result
from app.config import PROJECTS_DIR
from app.logging_config import setup_logger

logger = setup_logger()


class SceneRepository:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self._scene_dir: Optional[Path] = None

    @property
    def scene_dir(self) -> Path:
        if self._scene_dir is None:
            self._scene_dir = PROJECTS_DIR / self.project_id / "storyboard"
        return self._scene_dir

    def save_scenes(self, scenes: List[Dict]) -> Result[Path]:
        try:
            self.scene_dir.mkdir(parents=True, exist_ok=True)
            scenes_path = self.scene_dir / "scenes.json"
            scenes_path.write_text(
                json.dumps(scenes, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            proj_file = PROJECTS_DIR / self.project_id / "project.json"
            if proj_file.exists():
                content = json.loads(proj_file.read_text(encoding="utf-8"))
                content["scenes"] = scenes
                content["status"] = "scenes_created"
            else:
                content = {
                    "project_id": self.project_id,
                    "scenes": scenes,
                    "status": "scenes_created",
                    "created_at": ""
                }
            proj_file.write_text(
                json.dumps(content, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            logger.info("Cenas salvas para %s: %d cenas", self.project_id, len(scenes))
            return Result.success(scenes_path)
        except Exception as e:
            return Result.failure(error=str(e), code="SCENES_SAVE_FAILED")

    def load_scenes(self) -> Result[List[Dict]]:
        try:
            scenes_path = self.scene_dir / "scenes.json"
            if not scenes_path.exists():
                return Result.failure(error="No scenes file found", code="SCENES_NOT_FOUND")
            scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
            return Result.success(scenes)
        except Exception as e:
            return Result.failure(error=str(e), code="SCENES_LOAD_FAILED")
