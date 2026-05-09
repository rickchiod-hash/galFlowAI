"""Otimizador de texto de narração para TTS (Text-to-Speech)"""

import re
from typing import List, Dict, Any
from app.logging_config import setup_logger

logger = setup_logger()

class VoiceScriptOptimizer:
    """Otimiza texto de narração por cena para melhorar a qualidade do TTS"""
    
    def __init__(self, max_chars_per_scene: int = 150):
        """
        Inicializa o otimizador.
        
        Args:
            max_chars_per_scene: Número máximo de caracteres por cena (padrão: 150)
        """
        self.max_chars_per_scene = max_chars_per_scene
        
        # Expressões regulares para limpeza
        self.redundant_patterns = [
            (r'\s+', ' '),  # Múltiplos espaços para um único espaço
            (r'\.{2,}', '.'),  # Múltiplos pontos para um único ponto
            (r'[,;:]{2,}', ','),  # Múltiplas vírgulas/ponto e vírgula para uma vírgula
            (r'\s+[,.!?;:]', lambda m: m.group().strip()),  # Espaço antes de pontuação
            (r'[,.!?;:]\s*([,.!?;:])', r'\1'),  # Pontuação duplicada
        ]
        
        # Palavras/preposições comuns que podem ser removidas em contextos específicos
        self.filler_words = [
            'na verdade', 'como você sabe', 'é bom lembrar que', 'é importante destacar que',
            'pode-se dizer que', 'como já foi mencionado', 'vale ressaltar que'
        ]
    
    def optimize_scene_text(self, scene_text: str, scene_id: str = "") -> str:
        """
        Otimiza o texto de uma cena para TTS.
        
        Args:
            scene_text: Texto original da cena
            scene_id: ID da cena (para logging)
            
        Returns:
            Texto otimizado para TTS
        """
        if not scene_text or not scene_text.strip():
            return scene_text
            
        original_text = scene_text
        optimized = scene_text.strip()
        
        # 1. Remover palavras de preenchimento (fillers)
        for filler in self.filler_words:
            optimized = re.sub(
                re.escape(filler), 
                '', 
                optimized, 
                flags=re.IGNORECASE
            )
        
        # 2. Aplicar padrões de limpeza
        for pattern, replacement in self.redundant_patterns:
            if callable(replacement):
                optimized = re.sub(pattern, replacement, optimized)
            else:
                optimized = re.sub(pattern, replacement, optimized)
        
        # 3. Remover espaços extras no início/final e múltiplos espaços
        optimized = re.sub(r'\s+', ' ', optimized).strip()
        
        # 4. Garantir pontuação adequada no final
        if optimized and optimized[-1] not in '.!?':
            optimized += '.'
        
        # 5. Limitar tamanho se exceder o máximo
        if len(optimized) > self.max_chars_per_scene:
            optimized = self._truncate_text(optimized)
        
        # Log se houve otimização significativa
        if optimized != original_text:
            logger.info(
                f"Texto otimizado para cena {scene_id}: "
                f"{len(original_text)} -> {len(optimized)} caracteres"
            )
            if len(optimized) < len(original_text) * 0.8:  # Redução significativa
                logger.debug(
                    f"Otimização significativa: '{original_text[:50]}...' -> "
                    f"'{optimized[:50]}...'"
                )
        
        return optimized
    
    def _truncate_text(self, text: str) -> str:
        """
        Trunca o texto respeitando limites de frases quando possível.
        
        Args:
            text: Texto a ser truncado
            
        Returns:
            Texto truncado
        """
        if len(text) <= self.max_chars_per_scene:
            return text
            
        # Tentar truncar em uma quebra de frase natural
        truncated = text[:self.max_chars_per_scene]
        
        # Procurar por um ponto, exclamação ou interrogação seguido de espaço
        last_sentence_end = max(
            truncated.rfind('. '),
            truncated.rfind('! '),
            truncated.rfind('? ')
        )
        
        if last_sentence_end > self.max_chars_per_scene * 0.7:  # Se encontrou um corte razoável
            return truncated[:last_sentence_end + 1]  # Incluir o ponto
        
        # Se não encontrou um bom corte de frase, tentar por vírgula
        last_comma = truncated.rfind(', ')
        if last_comma > self.max_chars_per_scene * 0.8:  # Se vírgula estiver perto do fim
            return truncated[:last_comma + 1]  # Incluir a vírgula
            
        # Como último recurso, cortar no limite e adicionar elipse
        return truncated.rstrip() + '...'
    
    def optimize_scenes_batch(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Otimiza os textos de narração de um lote de cenas.
        
        Args:
            scenes: Lista de dicionários representando as cenas
            
        Returns:
            Lista de cenas com textos otimizados
        """
        optimized_scenes = []
        
        for scene in scenes:
            # Criar cópia para não modificar o original
            optimized_scene = scene.copy()
            
            # Otimizar o texto se existir
            if "scene_text" in optimized_scene:
                original_text = optimized_scene["scene_text"]
                optimized_text = self.optimize_scene_text(
                    original_text, 
                    optimized_scene.get("id", "unknown")
                )
                optimized_scene["scene_text"] = optimized_text
                
                # Atualizar também o prompt se for baseado no texto da cena
                if "prompt" in optimized_scene and not optimized_scene["prompt"]:
                    optimized_scene["prompt"] = optimized_text
            
            optimized_scenes.append(optimized_scene)
        
        return optimized_scenes


def optimize_scene_text_for_tts(scene_text: str, max_chars: int = 150) -> str:
    """
    Função utilitária para otimizar texto de cena para TTS.
    
    Args:
        scene_text: Texto da cena a ser otimizado
        max_chars: Número máximo de caracteres
        
    Returns:
        Texto otimizado
    """
    optimizer = VoiceScriptOptimizer(max_chars_per_scene=max_chars)
    return optimizer.optimize_scene_text(scene_text)


# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    optimizer = VoiceScriptOptimizer()
    
    test_texts = [
        "Esta é uma frase de teste simples.",
        "Esta  é   uma    frase   com   muitos   espaços.",
        "Esta frase tem.. múltiplos pontos... e vírgulas,,,",
        "Esta frase tem um espaço antes do ponto . e depois da vírgula ,",
        "Na verdade, é importante destacar que este produto é revolucionário, como você sabe.",
        "A" * 200,  # Texto muito longo
    ]
    
    for i, text in enumerate(test_texts):
        optimized = optimizer.optimize_scene_text(text, f"test_{i}")
        print(f"Original ({len(text)}): {text}")
        print(f"Otimizado ({len(optimized)}): {optimized}")
        print("-" * 50)