"""Testes para o Dashboard de Projetos - FlowForgeAI"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta")))

from app.main import load_projects, get_project_details


class TestDashboardProjects:
    """Testes para o Dashboard de Projetos"""
    
    def setup_method(self):
        """Limpa diretório de projetos antes de cada teste"""
        self.projects_dir = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/projects")
        if self.projects_dir.exists():
            import shutil
            for item in self.projects_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
    
    def test_load_projects_empty(self):
        """Testa carregar projetos com diretório vazio"""
        projects, count, status, details = load_projects()
        assert count == 0
        assert "encontrados" in status.lower() or "não encontrado" in status.lower()
    
    def test_load_projects_with_data(self, tmp_path):
        """Testa carregar projetos com dados"""
        # Cria um projeto fake
        proj_dir = self.projects_dir / "20260504_120000_test_proj"
        proj_dir.mkdir(parents=True, exist_ok=True)
        
        # Adiciona arquivos
        (proj_dir / "brief").mkdir(exist_ok=True)
        (proj_dir / "script").mkdir(exist_ok=True)
        (proj_dir / "final").mkdir(exist_ok=True)
        (proj_dir / "final" / "commercial.mp4").write_text("fake video")
        
        # Cria project.json
        proj_data = {
            "project_id": "20260504_120000_test_proj",
            "name": "test_proj",
            "status": "completed",
            "created_at": datetime.now().isoformat()
        }
        (proj_dir / "project.json").write_text(
            json.dumps(proj_data, indent=2),
            encoding="utf-8"
        )
        
        projects, count, status, details = load_projects()
        assert count >= 1
        assert any("test_proj" in str(p) for p in projects)
    
    def test_get_project_details_exists(self):
        """Testa detalhes de projeto existente"""
        proj_dir = self.projects_dir / "20260504_120000_test_proj2"
        proj_dir.mkdir(parents=True, exist_ok=True)
        
        proj_data = {
            "project_id": "20260504_120000_test_proj2",
            "name": "test_proj2",
            "status": "completed"
        }
        (proj_dir / "project.json").write_text(
            json.dumps(proj_data, indent=2),
            encoding="utf-8"
        )
        
        details, status = get_project_details("20260504_120000_test_proj2")
        assert "id" in details
        assert details["id"] == "20260504_120000_test_proj2"
        assert "files" in details
    
    def test_get_project_details_not_exists(self):
        """Testa detalhes de projeto inexistente"""
        details, status = get_project_details("nonexistent_project")
        assert details == {}
        assert "não encontrado" in status.lower() or "erro" in status.lower()
    
    def test_project_structure_detection(self):
        """Testa detecção de estrutura do projeto"""
        proj_dir = self.projects_dir / "20260504_120000_structure_test"
        proj_dir.mkdir(parents=True, exist_ok=True)
        
        # Cria estrutura completa
        for subdir in ["brief", "script", "prompts", "storyboard", "renders", "audio", "final"]:
            (proj_dir / subdir).mkdir(exist_ok=True)
        
        details, _ = get_project_details("20260504_120000_structure_test")
        assert details.get("files", {}).get("brief") is True
        assert details.get("files", {}).get("script") is True
        assert details.get("files", {}).get("final") is True
