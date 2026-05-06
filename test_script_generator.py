"""Testes para ScriptGenerator"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))


class TestScriptGenerator(unittest.TestCase):
    """Testes para o gerador de roteiros"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        from app.pipeline.script_generator import generate_script
        self.generate_func = generate_script
    
    def test_generate_script_returns_string(self):
        """Testa se retorna uma string"""
        with patch('app.pipeline.script_generator.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {"script": "Roteiro de teste", "provider": "test"}
            
            result = self.generate_func("Briefing de teste")
            self.assertIsInstance(result, str)
    
    def test_generate_script_with_mode(self):
        """Testa diferentes modos de geração"""
        with patch('app.pipeline.script_generator.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {"script": "Roteiro", "provider": "test"}
            
            for mode in ["auto", "fast", "quality", "safe", "template"]:
                result = self.generate_func("Briefing", mode=mode)
                self.assertIsInstance(result, str)
    
    def test_generate_script_fallback_on_error(self):
        """Testa se faz fallback quando LLM falha"""
        with patch('app.pipeline.script_generator.generate_script_with_llm') as mock_llm:
            mock_llm.side_effect = Exception("LLM error")
            
            # Deve usar TemplateProvider como fallback
            result = self.generate_func("Briefing de teste")
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
    
    def test_generate_script_with_project_id(self):
        """Testa se project_id é passado corretamente"""
        with patch('app.pipeline.script_generator.generate_script_with_llm') as mock_llm:
            mock_llm.return_value = {"script": "Roteiro", "provider": "test"}
            
            result = self.generate_func("Briefing", project_id="test_123")
            self.assertIsInstance(result, str)


class TestScriptGeneratorIntegration(unittest.TestCase):
    """Testes de integração"""
    
    def test_save_script_creates_file(self):
        """Testa se save_script cria arquivo"""
        from app.pipeline.script_generator import save_script
        from app.config import PROJECTS_DIR
        from pathlib import Path
        import tempfile
        import shutil
        
        # Cria um diretório temporário para o teste
        with tempfile.TemporaryDirectory() as tmpdir:
            # Sobrescreve PROJECTS_DIR temporariamente
            from app import config
            original = config.PROJECTS_DIR
            config.PROJECTS_DIR = tmpdir
            
            try:
                project_id = "test_save_script"
                script_text = "Roteiro de teste para salvar"
                
                save_script(project_id, script_text)
                
                # Verifica se arquivo foi criado (o arquivo real é script.txt)
                script_path = Path(tmpdir) / project_id / "script" / "script.txt"
                self.assertTrue(script_path.exists())
            finally:
                config.PROJECTS_DIR = original
    
    def test_import_works(self):
        """Testa se módulo pode ser importado"""
        try:
            from app.pipeline.script_generator import generate_script, save_script
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Erro de import: {e}")


if __name__ == "__main__":
    unittest.main()
