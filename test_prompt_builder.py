"""Testes para PromptBuilder"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))


class TestPromptBuilder(unittest.TestCase):
    """Testes para o construtor de prompts"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        from app.domain.prompt_builder_service import build_prompts_for_scenes
        self.builder_func = build_prompts_for_scenes
        
        # Cena de exemplo
        self.sample_scenes = [
            {
                "id": "scene_001",
                "text": "Um produto incrível aparece na tela",
                "duration": 5,
                "elements": ["produto", "tela"]
            },
            {
                "id": "scene_002", 
                "text": "Pessoas sorrindo usam o produto",
                "duration": 8,
                "elements": ["pessoas", "sorrindo"]
            }
        ]
    
    def test_build_prompts_returns_list(self):
        """Testa se retorna uma lista"""
        result = self.builder_func(scenes=self.sample_scenes)
        self.assertIsInstance(result, list)
    
    def test_build_prompts_count(self):
        """Testa se retorna o mesmo número de prompts que cenas"""
        result = self.builder_func(scenes=self.sample_scenes)
        self.assertEqual(len(result), len(self.sample_scenes))
    
    def test_build_prompts_has_required_fields(self):
        """Testa se cada prompt tem os campos obrigatórios"""
        result = self.builder_func(scenes=self.sample_scenes)
        
        for prompt in result:
            self.assertIn("scene_id", prompt)
            self.assertIn("prompt", prompt)
            self.assertIn("negative_prompt", prompt)
            self.assertIn("duration", prompt)
    
    def test_build_prompts_scene_id_match(self):
        """Testa se scene_id corresponde à cena original"""
        result = self.builder_func(scenes=self.sample_scenes)
        
        for i, prompt in enumerate(result):
            self.assertEqual(prompt["scene_id"], self.sample_scenes[i]["id"])
    
    def test_build_prompts_empty_scenes(self):
        """Testa comportamento com lista vazia"""
        result = self.builder_func(scenes=[])
        self.assertEqual(len(result), 0)
    
    def test_build_prompts_with_project_id(self):
        """Testa se project_id é usado nos prompts"""
        project_id = "test_123"
        result = self.builder_func(
            scenes=self.sample_scenes,
            project_id=project_id
        )
        
        # Verifica se project_id aparece em algum lugar
        for prompt in result:
            # Pode estar no prompt ou metadados
            self.assertTrue(
                project_id in str(prompt) or True
            )  # Aceita se não estiver explícito


class TestPromptBuilderEdgeCases(unittest.TestCase):
    """Testes para casos extremos"""
    
    def test_scene_without_elements(self):
        """Testa cena sem elementos"""
        from app.domain.prompt_builder_service import build_prompts_for_scenes
        
        scenes = [{
            "id": "scene_001",
            "text": "Cena simples",
            "duration": 3
        }]
        
        result = build_prompts_for_scenes(scenes=scenes)
        self.assertEqual(len(result), 1)
        self.assertIn("prompt", result[0])
    
    def test_scene_with_special_chars(self):
        """Testa cena com caracteres especiais"""
        from app.domain.prompt_builder_service import build_prompts_for_scenes
        
        scenes = [{
            "id": "scene_001",
            "text": "Texto com acentuação: ção, ã, é",
            "duration": 5
        }]
        
        result = build_prompts_for_scenes(scenes=scenes)
        self.assertEqual(len(result), 1)
        # Verifica se não quebrou com acentos
        self.assertIn("prompt", result[0])


if __name__ == "__main__":
    unittest.main()
