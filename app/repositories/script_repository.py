import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from app.core.result import Result
from app.config import PROJECTS_DIR
from app.logging_config import setup_logger

logger = setup_logger()

VERSION_METADATA_FIELDS = [
    "version", "timestamp", "note", "provider_used",
    "response_time_seconds", "quality_score", "status",
]


class ScriptRepository:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self._script_dir: Optional[Path] = None

    @property
    def script_dir(self) -> Path:
        if self._script_dir is None:
            self._script_dir = PROJECTS_DIR / self.project_id / "script"
        return self._script_dir

    def load_versions_list(self) -> List[Dict]:
        versions_file = self.script_dir / "script_versions.json"
        if not versions_file.exists():
            return []
        try:
            return json.loads(versions_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error("Failed to load versions: %s", e)
            return []

    def save_versions_list(self, versions: List[Dict]) -> Result[None]:
        try:
            self.script_dir.mkdir(parents=True, exist_ok=True)
            versions_file = self.script_dir / "script_versions.json"
            versions_file.write_text(
                json.dumps(versions, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            return Result.success(None)
        except Exception as e:
            return Result.failure(error=str(e), code="VERSIONS_SAVE_FAILED")

    def next_version(self) -> Result[str]:
        versions = self.load_versions_list()
        if not versions:
            return Result.success("v001")
        last = versions[-1]["version"]
        num = int(last[1:]) + 1
        return Result.success(f"v{num:03d}")

    def save_version_files(self, version: str, script_markdown: str, note: str = "") -> Result[Dict]:
        try:
            self.script_dir.mkdir(parents=True, exist_ok=True)
            md_file = self.script_dir / f"script_{version}.md"
            md_file.write_text(script_markdown, encoding="utf-8")

            metadata = {
                "version": version,
                "timestamp": datetime.now().isoformat(),
                "note": note,
                "provider_used": "Manual",
                "response_time_seconds": 0,
                "quality_score": 0,
                "status": "Draft",
            }
            json_file = self.script_dir / f"script_{version}.json"
            json_file.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            versions = self.load_versions_list()
            versions.append(metadata)
            save_result = self.save_versions_list(versions)
            if not save_result:
                return Result.failure(
                    error=save_result.error or "Failed to save versions list",
                    code=save_result.code,
                )

            return Result.success({"version": version, "script": script_markdown, "metadata": metadata})
        except Exception as e:
            return Result.failure(error=str(e), code="VERSION_SAVE_FAILED")

    def load_version_file(self, version: str) -> Result[str]:
        try:
            md_file = self.script_dir / f"script_{version}.md"
            if not md_file.exists():
                return Result.failure(error=f"Version file not found: {version}", code="VERSION_FILE_NOT_FOUND")
            return Result.success(md_file.read_text(encoding="utf-8"))
        except Exception as e:
            return Result.failure(error=str(e), code="VERSION_FILE_LOAD_FAILED")

    def load_approved_script(self) -> Result[Dict]:
        try:
            approved_md = self.script_dir / "script_approved.md"
            if not approved_md.exists():
                return Result.failure(error="No approved script found", code="NOT_APPROVED")

            script = approved_md.read_text(encoding="utf-8")
            return Result.success({"script": script, "version": "approved"})
        except Exception as e:
            return Result.failure(error=str(e), code="APPROVED_LOAD_FAILED")

    def load_current_script(self) -> Result[Dict]:
        approved_result = self.load_approved_script()
        if approved_result:
            return approved_result

        versions = self.load_versions_list()
        if not versions:
            return Result.failure(error="No script found", code="NO_SCRIPT")

        latest = versions[-1]
        version = latest["version"]
        script_result = self.load_version_file(version)
        if not script_result:
            return Result.failure(error=script_result.error or "Script file not found", code="SCRIPT_FILE_NOT_FOUND")

        return Result.success({
            "script": script_result.data,
            "version": version,
        })

    def save_approved(self, script: str, version: str) -> Result[Dict]:
        try:
            self.script_dir.mkdir(parents=True, exist_ok=True)

            approved_md = self.script_dir / "script_approved.md"
            approved_md.write_text(script, encoding="utf-8")

            metadata = {
                "approved_at": datetime.now().isoformat(),
                "version": version,
                "script": script,
            }
            approved_json = self.script_dir / "script_approved.json"
            approved_json.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            versions = self.load_versions_list()
            for v in versions:
                if v["version"] == version:
                    v["status"] = "Approved"
                    break
            self.save_versions_list(versions)

            return Result.success({"script": script, "status": "Approved"})
        except Exception as e:
            return Result.failure(error=str(e), code="APPROVE_SAVE_FAILED")

    def load_versions_summary(self) -> List[Dict]:
        versions = self.load_versions_list()
        return [
            {
                "version": v["version"],
                "note": v.get("note", ""),
                "status": v.get("status", "Draft"),
            }
            for v in versions
        ]

    def find_previous_version(self) -> Result[Dict]:
        versions = self.load_versions_list()
        if len(versions) < 2:
            return Result.failure(error="No previous version to restore", code="NO_PREVIOUS_VERSION")

        prev = versions[-2]
        version = prev["version"]
        script_result = self.load_version_file(version)
        if not script_result:
            return Result.failure(
                error=script_result.error or "Previous version file not found",
                code="PREVIOUS_FILE_NOT_FOUND",
            )

        return Result.success({"script": script_result.data, "version": version})
