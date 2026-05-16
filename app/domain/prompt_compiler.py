"""PromptCompiler schema (VIS-503).

Compilador que traduz SceneContract em prompts específicos
por engine (FFmpeg, WanGP, VACE). Cada engine recebe instruções
no formato adequado para seu pipeline de render.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.exceptions import ConfigError
from app.domain.scene_contract import (
    CameraMovement,
    SceneContract,
    ShotSize,
    TransitionType,
)


class EngineType(str, Enum):
    """Motores de render suportados."""
    WAN_GP = "wangp"
    FFMPEG = "ffmpeg"
    VACE = "vace"


class PromptFormat(str, Enum):
    """Formatos de saída do compilador."""
    PLAIN_TEXT = "plain_text"
    STRUCTURED = "structured"
    JSON = "json"


class EngineParameter(BaseModel):
    """Parâmetro específico de engine para compilação."""
    key: str
    value: Any
    description: str = ""


class CompiledPrompt(BaseModel):
    """Prompt compilado para uma engine específica."""
    id: str = Field(default_factory=lambda: f"cp_{uuid4().hex[:12]}")
    scene_contract_id: str
    engine: EngineType
    prompt_text: str
    negative_prompt: str = ""
    parameters: List[EngineParameter] = Field(default_factory=list)
    format: PromptFormat = PromptFormat.PLAIN_TEXT
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptCompilerService:
    """Compilador de prompts por engine.

    Traduz SceneContracts em instruções específicas para cada
    motor de render, aproveitando diretivas de câmera,
    ingredientes e transições.
    """

    def __init__(self):
        self._compiled: Dict[str, CompiledPrompt] = {}

    def compile(self, contract: SceneContract, engine: EngineType) -> CompiledPrompt:
        """Compila um SceneContract em prompt para a engine especificada."""
        if engine == EngineType.WAN_GP:
            return self._compile_for_wangp(contract)
        elif engine == EngineType.FFMPEG:
            return self._compile_for_ffmpeg(contract)
        elif engine == EngineType.VACE:
            return self._compile_for_vace(contract)
        else:
            raise ConfigError(f"Unsupported engine: {engine}", param="engine")

    def compile_all(
        self,
        contracts: List[SceneContract],
        engine: EngineType,
    ) -> List[CompiledPrompt]:
        """Compila múltiplos contratos para uma engine."""
        return [self.compile(c, engine) for c in contracts]

    def compile_multi_engine(
        self,
        contract: SceneContract,
        engines: List[EngineType],
    ) -> List[CompiledPrompt]:
        """Compila um contrato para múltiplas engines."""
        return [self.compile(contract, e) for e in engines]

    def _describe_camera(self, contract: SceneContract) -> str:
        """Gera descrição textual da diretiva de câmera."""
        cam = contract.camera
        parts = [f"ângulo {cam.angle}"]
        if cam.movement != CameraMovement.STATIC:
            parts.append(f"movimento {cam.movement.value}")
        parts.append(f"plano {cam.shot_size.value.replace('_', ' ')}")
        if cam.notes:
            parts.append(f"({cam.notes})")
        return ", ".join(parts)

    def _describe_ingredients(self, contract: SceneContract) -> str:
        """Gera descrição textual dos ingredientes na cena."""
        if not contract.ingredients:
            return ""
        descs = []
        for ing in contract.ingredients:
            base = ing.ingredient_name
            if ing.placement:
                base += f" ({ing.placement})"
            descs.append(base)
        return "Cena contém: " + "; ".join(descs) + "."

    def _compile_for_wangp(self, contract: SceneContract) -> CompiledPrompt:
        """Compila prompt detalhado para WanGP (vídeo gerado por IA).

        Inclui descrição cinematográfica completa, diretivas de
        câmera, ingredientes e referências visuais.
        """
        parts = [contract.description]

        camera_desc = self._describe_camera(contract)
        parts.append(f"Câmera: {camera_desc}")

        ingredients_desc = self._describe_ingredients(contract)
        if ingredients_desc:
            parts.append(ingredients_desc)

        if contract.style:
            parts.append(f"Estilo: {contract.style}")

        if contract.prompt_positive:
            parts.append(contract.prompt_positive)

        prompt_text = ". ".join(parts)

        negative = contract.prompt_negative or "blurry, low quality, distorted, bad anatomy, inconsistent"

        params = [
            EngineParameter(key="duration", value=contract.duration, description="Duração em segundos"),
            EngineParameter(key="transition_in", value=contract.transition_in.value, description="Transição de entrada"),
            EngineParameter(key="transition_out", value=contract.transition_out.value, description="Transição de saída"),
        ]

        if contract.ingredients:
            for ing in contract.ingredients:
                if ing.visual_bible_ref:
                    params.append(
                        EngineParameter(
                            key=f"visual_bible_ref_{ing.ingredient_id}",
                            value=ing.visual_bible_ref,
                            description=f"Referência visual bible para {ing.ingredient_name}",
                        )
                    )

        return CompiledPrompt(
            scene_contract_id=contract.id,
            engine=EngineType.WAN_GP,
            prompt_text=prompt_text,
            negative_prompt=negative,
            parameters=params,
            format=PromptFormat.STRUCTURED,
        )

    def _compile_for_ffmpeg(self, contract: SceneContract) -> CompiledPrompt:
        """Compila prompt para FFmpeg (vídeo estático com texto).

        Gera instruções para criar um vídeo estático com overlay
        de texto, usado como fallback quando WanGP não disponível.
        """
        prompt_text = contract.description

        negative = ""

        params = [
            EngineParameter(key="duration", value=contract.duration, description="Duração em segundos"),
            EngineParameter(key="text_overlay", value=contract.description[:200], description="Texto a exibir no vídeo"),
            EngineParameter(key="transition_in", value=contract.transition_in.value, description="Transição de entrada"),
            EngineParameter(key="transition_out", value=contract.transition_out.value, description="Transição de saída"),
        ]

        if contract.style:
            params.append(
                EngineParameter(key="style", value=contract.style, description="Estilo visual")
            )

        return CompiledPrompt(
            scene_contract_id=contract.id,
            engine=EngineType.FFMPEG,
            prompt_text=prompt_text,
            negative_prompt=negative,
            parameters=params,
            format=PromptFormat.STRUCTURED,
        )

    def _compile_for_vace(self, contract: SceneContract) -> CompiledPrompt:
        """Compila prompt para VACE (edição de vídeo avançada).

        Formato preparado para futuro motor VACE.
        """
        parts = [
            f"Scene {contract.scene_number}: {contract.description}",
            f"Duration: {contract.duration}s",
            f"Camera: angle={contract.camera.angle}, movement={contract.camera.movement.value}, shot={contract.camera.shot_size.value}",
        ]

        if contract.ingredients:
            ing_list = "; ".join(
                f"{ing.ingredient_name} ({ing.placement or 'default'})"
                for ing in contract.ingredients
            )
            parts.append(f"Ingredients: {ing_list}")

        params = [
            EngineParameter(key="duration", value=contract.duration),
            EngineParameter(key="transition_in", value=contract.transition_in.value),
            EngineParameter(key="transition_out", value=contract.transition_out.value),
            EngineParameter(key="camera_angle", value=contract.camera.angle),
            EngineParameter(key="camera_movement", value=contract.camera.movement.value),
            EngineParameter(key="shot_size", value=contract.camera.shot_size.value),
        ]

        return CompiledPrompt(
            scene_contract_id=contract.id,
            engine=EngineType.VACE,
            prompt_text="\n".join(parts),
            parameters=params,
            format=PromptFormat.STRUCTURED,
        )

    def save(self, prompt: CompiledPrompt) -> str:
        """Armazena um prompt compilado no registry interno."""
        self._compiled[prompt.id] = prompt
        return prompt.id

    def get(self, prompt_id: str) -> Optional[CompiledPrompt]:
        """Recupera prompt compilado por ID."""
        return self._compiled.get(prompt_id)

    def list_by_engine(self, engine: EngineType) -> List[CompiledPrompt]:
        """Lista prompts compilados para uma engine específica."""
        return [p for p in self._compiled.values() if p.engine == engine]

    def list_by_contract(self, contract_id: str) -> List[CompiledPrompt]:
        """Lista prompts compilados para um contrato específico."""
        return [p for p in self._compiled.values() if p.scene_contract_id == contract_id]

    def clear(self) -> None:
        """Limpa registry de prompts compilados."""
        self._compiled.clear()
