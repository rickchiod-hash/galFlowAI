"""Checkpoint manager for pipeline resumption"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time

logger = logging.getLogger(__name__)


class CheckpointManager:
    """Manages checkpoints for pipeline stages"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.checkpoint_dir = project_dir / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.current_checkpoint_file = None
    
    def save_checkpoint(self, stage_name: str, data: Dict[str, Any]) -> Path:
        """
        Save checkpoint for a stage
        
        Args:
            stage_name: Name of the stage (e.g., 'scene_generation', 'video_generation')
            data: Data to save (scenes, results, etc.)
            
        Returns:
            Path to checkpoint file
        """
        timestamp = int(time.time())
        checkpoint_file = self.checkpoint_dir / f"{stage_name}_{timestamp}.json"
        
        checkpoint_data = {
            "stage": stage_name,
            "timestamp": timestamp,
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }
        
        try:
            checkpoint_file.write_text(
                json.dumps(checkpoint_data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            logger.info(f"Checkpoint saved: {checkpoint_file.name}")
            self.current_checkpoint_file = checkpoint_file
            return checkpoint_file
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            return None
    
    def load_latest_checkpoint(self, stage_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Load latest checkpoint, optionally filtered by stage name
        
        Args:
            stage_name: If provided, only load checkpoint for this stage
            
        Returns:
            Checkpoint data or None if not found
        """
        try:
            checkpoints = list(self.checkpoint_dir.glob("*.json"))
            if not checkpoints:
                return None
            
            # Filter by stage name if provided
            if stage_name:
                checkpoints = [cp for cp in checkpoints if cp.stem.startswith(stage_name)]
                if not checkpoints:
                    return None
            
            # Get most recent checkpoint
            latest = max(checkpoints, key=lambda p: p.stat().st_mtime)
            
            data = json.loads(latest.read_text(encoding="utf-8"))
            logger.info(f"Loaded checkpoint: {latest.name}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None
    
    def clear_checkpoints(self, stage_name: Optional[str] = None) -> int:
        """
        Clear checkpoints, optionally filtered by stage name
        
        Args:
            stage_name: If provided, only clear checkpoints for this stage
            
        Returns:
            Number of checkpoints cleared
        """
        try:
            checkpoints = list(self.checkpoint_dir.glob("*.json"))
            if stage_name:
                checkpoints = [cp for cp in checkpoints if cp.stem.startswith(stage_name)]
            
            count = 0
            for cp in checkpoints:
                cp.unlink()
                count += 1
            
            logger.info(f"Cleared {count} checkpoints")
            return count
            
        except Exception as e:
            logger.error(f"Failed to clear checkpoints: {e}")
            return 0
