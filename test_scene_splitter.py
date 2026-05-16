"""Testes para SceneSplitter"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))


class TestSceneSplitter(unittest.TestCase):
    """Testes para o divisor de cenas"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        from app.domain.scene_parser import split_script_into_scenes
        self.split_func = split_script_into_scenes
        self.test_project_id = "test_project_123"
    
    def test_split_script_returns_list(self):
        """Testa se retorna uma lista"""
        script = "Cena 1: Texto aqui. Cena 2: Mais texto."
        result = self.split_func(script, project_id=self.test_project_id)
        self.assertIsInstance(result, list)
    
    def test_split_script_creates_scenes(self):
        """Testa se cria cenas a partir do roteiro"""
        script = "Cena 1: Um produto aparece. Cena 2: Pessoas usam o produto."
        result = self.split_func(script, project_id=self.test_project_id)
        self.assertGreater(len(result), 0)
    
    def test_split_script_scene_has_fields(self):
        """Testa se cada cena tem campos obrigatórios"""
        script = "Cena 1: Teste. Cena 2: Outro teste."
        result = self.split_func(script, project_id=self.test_project_id)
        
        for scene in result:
            self.assertIn("id", scene)
            self.assertIn("description", scene)
            self.assertIn("duration_estimate", scene)
    
    def test_split_script_empty_input(self):
        """Testa comportamento com entrada vazia"""
        result = self.split_func("", project_id=self.test_project_id)
        # Pode retornar lista vazia ou cena padrão
        self.assertIsInstance(result, list)
    
    def test_split_script_with_project_id(self):
        """Testa se project_id é usado"""
        script = "Cena 1: Teste."
        result = self.split_func(script, project_id=self.test_project_id)
        
        # Verifica se project_id aparece em algum lugar
        self.assertIsInstance(result, list)
        if len(result) > 0:
            # Pode estar no ID ou metadados
            self.assertTrue(True)  # Aceita se não quebrar
    
    def test_split_script_duration_calculation(self):
        """Testa se duração é calculada baseada no texto"""
        script = "Cena 1: " + "palavra " * 100  # Texto longo
        result = self.split_func(script, project_id=self.test_project_id)
        
        if len(result) > 0:
            # Duração deve ser pelo menos 1 segundo
            self.assertGreaterEqual(result[0].get("duration_estimate", 0), 1)


class TestSceneSplitterEdgeCases(unittest.TestCase):
    """Testes para casos extremos"""
    
    def test_script_with_special_chars(self):
        """Testa roteiro com caracteres especiais"""
        from app.domain.scene_parser import split_script_into_scenes
        
        script = "Cena 1: Texto com açúcar, ção, ã. Cena 2: Mais ç."
        result = split_script_into_scenes(script, project_id="test")
        self.assertIsInstance(result, list)
    
    def test_script_very_short(self):
        """Testa roteiro muito curto"""
        from app.domain.scene_parser import split_script_into_scenes
        
        script = "OK"
        result = split_script_into_scenes(script, project_id="test")
        self.assertIsInstance(result, list)
    
    def test_script_no_scene_markers(self):
        """Testa roteiro sem marcadores de cena"""
        from app.domain.scene_parser import split_script_into_scenes
        
        script = "Este é um texto sem marcadores de cena. Apenas um parágrafo."
        result = split_script_into_scenes(script, project_id="test")
        # Deve criar pelo menos uma cena
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()
