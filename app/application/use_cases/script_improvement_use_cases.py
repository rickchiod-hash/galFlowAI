"""Use cases for Advanced Script Editing (V2.5 / H16)."""
from typing import Dict, Any, List, Optional
from app.application.use_cases.base import UseCase
from app.config import PROJECTS_DIR
from pathlib import Path
import json
from datetime import datetime


class ImproveScriptUseCase(UseCase):
    """Improve script based on type.
    
    3-point standard:
    1. Validate script and improvement type
    2. Apply improvement strategy
    3. Return improved script with metadata
    """
    
    def __init__(self):
        super().__init__()
        self.improvements_dir = PROJECTS_DIR
    
    def execute(
        self,
        project_id: str,
        script: str,
        improvement_type: str = "general"
    ) -> Dict[str, Any]:
        """Execute script improvement."""
        try:
            if not self._validate(project_id=project_id, script=script):
                return self._build_error("Invalid project_id or script")
            
            # Apply improvement
            improved = self._apply_improvement(script, improvement_type)
            
            # Save version
            self._save_version(project_id, script, improved, improvement_type)
            
            return self._build_success(data={
                "original": script,
                "improved": improved,
                "improvement_type": improvement_type,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        script = kwargs.get("script", "")
        return bool(project_id) and bool(script)
    
    def _apply_improvement(self, script: str, improvement_type: str) -> str:
        """Apply improvement strategy."""
        if improvement_type == "viral":
            return self._make_viral(script)
        elif improvement_type == "premium":
            return self._make_premium(script)
        elif improvement_type == "direct":
            return self._make_direct(script)
        else:
            return self._general_improve(script)
    
    def _make_viral(self, script: str) -> str:
        """Make script more viral."""
        lines = script.split("\n")
        viral_lines = []
        for line in lines:
            viral_lines.append(line)
            if "!" not in line and len(line) > 10:
                viral_lines.append(line + "!")
        return "\n".join(viral_lines)
    
    def _make_premium(self, script: str) -> str:
        """Make script more premium."""
        premium = script.replace("bom", "excelente").replace("grande", "extraordinário")
        if "exclusivo" not in premium.lower():
            premium += "\n\nOferta exclusiva por tempo limitado!"
        return premium
    
    def _make_direct(self, script: str) -> str:
        """Make script more direct."""
        sentences = script.split(".")
        direct = ". ".join(sentence.strip() for sentence in sentences if sentence.strip())
        return direct
    
    def _general_improve(self, script: str) -> str:
        """General improvement."""
        return script.strip() + "\n\nCrie agora seu próprio comercial!"
    
    def _save_version(self, project_id: str, original: str, improved: str, imp_type: str):
        """Save script version."""
        versions_dir = self.improvements_dir / project_id / "script_versions"
        versions_dir.mkdir(parents=True, exist_ok=True)
        
        version_data = {
            "timestamp": datetime.now().isoformat(),
            "improvement_type": imp_type,
            "original": original,
            "improved": improved
        }
        
        version_file = versions_dir / f"version_{int(datetime.now().timestamp())}.json"
        version_file.write_text(
            json.dumps(version_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


class ApproveScriptUseCase(UseCase):
    """Approve or reject script.
    
    3-point standard:
    1. Validate project_id and script
    2. Save approval status
    3. Return approval status
    """
    
    def __init__(self):
        super().__init__()
        self.approvals_dir = PROJECTS_DIR
    
    def execute(
        self,
        project_id: str,
        script: str,
        approved: bool = True
    ) -> Dict[str, Any]:
        """Execute script approval."""
        try:
            if not self._validate(project_id=project_id, script=script):
                return self._build_error("Invalid project_id or script")
            
            # Save approval status
            self._save_approval(project_id, script, approved)
            
            return self._build_success(data={
                "approved": approved,
                "project_id": project_id,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        script = kwargs.get("script", "")
        return bool(project_id) and bool(script)
    
    def _save_approval(self, project_id: str, script: str, approved: bool):
        """Save approval status."""
        approval_dir = self.approvals_dir / project_id
        approval_dir.mkdir(parents=True, exist_ok=True)
        
        approval_data = {
            "approved": approved,
            "script": script,
            "timestamp": datetime.now().isoformat()
        }
        
        approval_file = approval_dir / "approval_status.json"
        approval_file.write_text(
            json.dumps(approval_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )


class GetScriptVersionsUseCase(UseCase):
    """Get all script versions for a project.
    
    3-point standard:
    1. Validate project_id
    2. Load versions from disk
    3. Return versions list
    """
    
    def __init__(self):
        super().__init__()
        self.versions_dir = PROJECTS_DIR
    
    def execute(self, project_id: str) -> Dict[str, Any]:
        """Execute get script versions."""
        try:
            if not self._validate(project_id=project_id):
                return self._build_error("Invalid project_id")
            
            versions = self._load_versions(project_id)
            
            return self._build_success(data={
                "project_id": project_id,
                "versions": versions,
                "count": len(versions)
            })
        except Exception as e:
            return self._build_error(str(e))
    
    def _validate(self, **kwargs) -> bool:
        project_id = kwargs.get("project_id", "")
        return bool(project_id)
    
    def _load_versions(self, project_id: str) -> List[Dict]:
        """Load all versions from disk."""
        versions_dir = self.versions_dir / project_id / "script_versions"
        if not versions_dir.exists():
            return []
        
        versions = []
        for version_file in versions_dir.glob("version_*.json"):
            try:
                data = json.loads(version_file.read_text(encoding="utf-8"))
                versions.append(data)
            except Exception:
                continue
        
        return sorted(versions, key=lambda x: x.get("timestamp", ""), reverse=True)
