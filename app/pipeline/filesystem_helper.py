"""Filesystem helpers for pipeline operations"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class FilesystemHelper:
    """Helper class for filesystem operations in the pipeline"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize filesystem helper
        
        Args:
            base_dir: Base directory for operations (optional)
        """
        self.base_dir = base_dir
    
    def ensure_dir_exists(self, path: Path) -> Path:
        """
        Ensure directory exists, create if not
        
        Args:
            path: Directory path
            
        Returns:
            The path (for chaining)
        """
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def write_json(self, path: Path, data: Any, indent: int = 2) -> bool:
        """
        Write data as JSON to file
        
        Args:
            path: File path
            data: Data to write
            indent: JSON indentation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.ensure_dir_exists(path.parent)
            path.write_text(
                json.dumps(data, indent=indent, ensure_ascii=False),
                encoding="utf-8"
            )
            logger.debug(f"JSON written to {path}")
            return True
        except Exception as e:
            logger.error(f"Error writing JSON to {path}: {e}")
            return False
    
    def write_text(self, path: Path, text: str, encoding: str = "utf-8") -> bool:
        """
        Write text to file
        
        Args:
            path: File path
            text: Text to write
            encoding: File encoding
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.ensure_dir_exists(path.parent)
            path.write_text(text, encoding=encoding)
            logger.debug(f"Text written to {path}")
            return True
        except Exception as e:
            logger.error(f"Error writing text to {path}: {e}")
            return False
    
    def read_json(self, path: Path) -> Optional[Any]:
        """
        Read JSON from file
        
        Args:
            path: File path
            
        Returns:
            Parsed JSON data or None if error
        """
        try:
            if not path.exists():
                logger.warning(f"File not found: {path}")
                return None
            text = path.read_text(encoding="utf-8")
            return json.loads(text)
        except Exception as e:
            logger.error(f"Error reading JSON from {path}: {e}")
            return None
    
    def read_text(self, path: Path) -> Optional[str]:
        """
        Read text from file
        
        Args:
            path: File path
            
        Returns:
            File text or None if error
        """
        try:
            if not path.exists():
                logger.warning(f"File not found: {path}")
                return None
            return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Error reading text from {path}: {e}")
            return None
    
    def save_script(self, project_dir: Path, script_text: str) -> Path:
        """Save script to project directory"""
        script_path = project_dir / "script" / "script_approved.md"
        if self.write_text(script_path, script_text):
            return script_path
        return None
    
    def save_scenes(self, project_dir: Path, scenes: List[Dict]) -> Path:
        """Save scenes to project directory"""
        scenes_path = project_dir / "storyboard" / "scenes.json"
        if self.write_json(scenes_path, scenes):
            return scenes_path
        return None
    
    def save_prompts(self, project_dir: Path, prompts: List[Dict], optimized: bool = False) -> Path:
        """Save prompts to project directory"""
        filename = "prompts_optimized.json" if optimized else "prompts.json"
        prompts_path = project_dir / "prompts" / filename
        if self.write_json(prompts_path, prompts):
            return prompts_path
        return None
    
    def get_project_paths(self, project_dir: Path) -> Dict[str, Path]:
        """Get all standard project paths"""
        return {
            "project": project_dir,
            "script": project_dir / "script",
            "storyboard": project_dir / "storyboard",
            "prompts": project_dir / "prompts",
            "audio": project_dir / "audio",
            "renders": project_dir / "renders",
            "final": project_dir / "final"
        }
