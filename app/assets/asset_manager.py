"""Asset Manager for GalFlowAI - Gerencia imagens de referência"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AssetManager:
    """Gerencia assets (imagens de referência) para projetos"""
    
    def __init__(self, base_assets_dir: Optional[Path] = None):
        """
        Initialize asset manager
        
        Args:
            base_assets_dir: Diretório base para assets (opcional)
        """
        if base_assets_dir:
            self.base_dir = Path(base_assets_dir)
        else:
            # Padrão: K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/assets
            self.base_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/assets")
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"AssetManager initialized: {self.base_dir}")
    
    def save_reference_image(
        self,
        project_id: str,
        image_path: Path,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Save a reference image for a project
        
        Args:
            project_id: Project identifier
            image_path: Path to the image file
            description: Optional description
            
        Returns:
            Dict with save result
        """
        try:
            if not image_path.exists():
                return {"success": False, "error": f"Image not found: {image_path}"}
            
            # Create project assets directory
            project_assets = self.base_dir / project_id
            project_assets.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = image_path.suffix or ".png"
            new_filename = f"ref_{timestamp}{ext}"
            target_path = project_assets / new_filename
            
            # Copy image
            shutil.copy2(image_path, target_path)
            logger.info(f"Reference image saved: {target_path}")
            
            return {
                "success": True,
                "asset_path": str(target_path),
                "filename": new_filename,
                "description": description,
                "project_id": project_id,
                "timestamp": timestamp
            }
            
        except Exception as e:
            logger.error(f"Error saving reference image: {e}")
            return {"success": False, "error": str(e)}
    
    def get_project_assets(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all assets for a project
        
        Args:
            project_id: Project identifier
            
        Returns:
            List of asset dictionaries
        """
        try:
            project_assets = self.base_dir / project_id
            if not project_assets.exists():
                return []
            
            assets = []
            for img in project_assets.glob("*.*"):
                if img.is_file() and img.suffix.lower() in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
                    assets.append({
                        "filename": img.name,
                        "path": str(img),
                        "size": img.stat().st_size,
                        "modified": datetime.fromtimestamp(img.stat().st_mtime).isoformat()
                    })
            
            return sorted(assets, key=lambda x: x["modified"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error getting project assets: {e}")
            return []
    
    def delete_asset(self, project_id: str, filename: str) -> Dict[str, Any]:
        """
        Delete an asset
        
        Args:
            project_id: Project identifier
            filename: Filename to delete
            
        Returns:
            Dict with deletion result
        """
        try:
            asset_path = self.base_dir / project_id / filename
            if not asset_path.exists():
                return {"success": False, "error": f"Asset not found: {filename}"}
            
            asset_path.unlink()
            logger.info(f"Asset deleted: {asset_path}")
            return {"success": True, "filename": filename}
            
        except Exception as e:
            logger.error(f"Error deleting asset: {e}")
            return {"success": False, "error": str(e)}
    
    def get_asset_for_prompt(
        self,
        project_id: str,
        description: Optional[str] = None
    ) -> Optional[str]:
        """
        Get asset path for use in prompts (latest or matching description)
        
        Args:
            project_id: Project identifier
            description: Optional description to match
            
        Returns:
            Path to asset or None
        """
        assets = self.get_project_assets(project_id)
        if not assets:
            return None
        
        if description:
            # Try to find matching description
            for asset in assets:
                if description.lower() in asset.get("description", "").lower():
                    return asset["path"]
        
        # Return latest asset
        return assets[0]["path"] if assets else None
    
    def integrate_with_video_generation(
        self,
        scene_prompts: list,
        project_id: str
    ) -> list:
        """
        Integrate assets into scene prompts
        
        Args:
            scene_prompts: List of scene prompt dictionaries
            project_id: Project identifier
            
        Returns:
            Updated scene prompts with asset references
        """
        assets = self.get_project_assets(project_id)
        if not assets:
            logger.info(f"No assets found for project {project_id}")
            return scene_prompts
        
        updated = []
        for prompt in scene_prompts:
            p = prompt.copy()
            # Add asset reference to prompt if not already present
            if "reference_image" not in p and assets:
                # Use latest asset for first scene, cycle through others
                scene_num = p.get("scene_number", 1) - 1
                asset_idx = scene_num % len(assets)
                p["reference_image"] = assets[asset_idx]["path"]
                logger.info(f"Added reference image to scene {p.get('id')}: {assets[asset_idx]['filename']}")
            updated.append(p)
        
        return updated
