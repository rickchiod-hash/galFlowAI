"""
Tests for script service.
"""
import sys
import os
import json
sys.path.insert(0, "K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")

from app.services.script_service import (
    generate_script_with_llm,
    save_manual_edit,
    improve_script,
    complement_script,
    make_script_more_viral,
    make_script_more_premium,
    make_script_more_direct,
    create_new_version,
    restore_previous_version,
    approve_script,
    load_current_script,
    load_script_versions
)
from app.logging_config import setup_logger
from app.config import PROJECTS_DIR
from pathlib import Path
import shutil

logger = setup_logger()

def setup_test_project(project_id="test_service"):
    """Create a minimal test project."""
    proj_dir = PROJECTS_DIR / project_id
    if proj_dir.exists():
        shutil.rmtree(proj_dir)
    proj_dir.mkdir(parents=True)
    
    # Create basic project.json
    proj_file = proj_dir / "project.json"
    proj_data = {
        "id": project_id,
        "name": "Test Project",
        "status": "initialized"
    }
    proj_file.write_text(json.dumps(proj_data, indent=2), encoding="utf-8")
    
    # Create necessary subdirectories
    (proj_dir / "script").mkdir()
    (proj_dir / "prompts").mkdir()
    (proj_dir / "storyboard").mkdir()
    (proj_dir / "renders").mkdir()
    (proj_dir / "audio").mkdir()
    (proj_dir / "final").mkdir()
    (proj_dir / "logs").mkdir()
    
    return proj_dir

def teardown_test_project(project_id="test_service"):
    """Clean up test project."""
    proj_dir = PROJECTS_DIR / project_id
    if proj_dir.exists():
        shutil.rmtree(proj_dir)

def test_script_service_versioning_and_approve():
    """Test script versioning and approval workflow."""
    project_id = "test_service_versioning"
    
    try:
        # Setup
        proj_dir = setup_test_project(project_id)
        
        # 1. Generate initial script
        briefing = "Teste de versionamento de roteiro"
        result = generate_script_with_llm(briefing, mode="template")
        initial_script = result["script"]
        assert initial_script is not None
        assert len(initial_script) > 0
        
        # 2. Save as initial version (this happens automatically in generate_script_with_llm?)
        # Actually, generate_script_with_llm doesn't save, we need to use save_manual_edit or create_new_version
        # Let's save the initial script
        save_result = save_manual_edit(project_id, initial_script, "Initial version")
        assert "version" in save_result
        version1 = save_result["version"]
        
        # 3. Load current script
        current = load_current_script(project_id)
        assert current["script"] == initial_script
        
        # 4. Create a new version by editing
        edited_script = initial_script.replace("Teste", "Edição")
        edit_result = save_manual_edit(project_id, edited_script, "Edited version")
        assert "version" in edit_result
        version2 = edit_result["version"]
        assert version2 != version1
        
        # 5. Check versions list
        versions = load_script_versions(project_id)
        print(f"Versions found: {versions}")
        assert len(versions) >= 2
        # Versions are in ascending order (oldest first) based on _save_versions implementation
        assert versions[0]["version"] == version1
        assert versions[1]["version"] == version2
        
        # 6. Restore previous version
        restore_result = restore_previous_version(project_id)
        assert restore_result["script"] == initial_script
        
        # 7. Approve current script (the latest version is the edited one)
        approve_result = approve_script(project_id)
        assert approve_result["script"] == edited_script
        assert approve_result["status"] == "Approved"
        
        # After approval, load_current_script should return version "approved"
        current = load_current_script(project_id)
        assert current["version"] == "approved"
        assert current["script"] == edited_script
        
        print("test_script_service_versioning_and_approve: PASSED")
        
    finally:
        teardown_test_project(project_id)

if __name__ == "__main__":
    test_script_service_versioning_and_approve()
    print("\nAll script service tests PASSED!")