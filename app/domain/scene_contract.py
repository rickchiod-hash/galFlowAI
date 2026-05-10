"""SceneContract schema (VIS-502).

Define contratos por cena: descrição visual, ingredientes
referenciados, duração, transição, diretivas de câmera.
Transforma roteiro em instruções testáveis para a engine de render.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class SceneContractStatus(str, Enum):
    """Status de um contrato de cena."""
    DRAFT = "draft"
    FINALIZED = "finalized"
    APPROVED = "approved"


class TransitionType(str, Enum):
    """Tipos de transição entre cenas."""
    CUT = "cut"
    FADE = "fade"
    DISSOLVE = "dissolve"
    WIPE = "wipe"


class ShotSize(str, Enum):
    """Tamanhos de plano cinematográfico."""
    EXTREME_WIDE = "extreme_wide"
    WIDE = "wide"
    FULL = "full"
    MEDIUM = "medium"
    CLOSE_UP = "close_up"
    EXTREME_CLOSE_UP = "extreme_close_up"


class CameraMovement(str, Enum):
    """Movimentos de câmera."""
    STATIC = "static"
    PAN = "pan"
    TILT = "tilt"
    TRACK = "track"
    DOLLY = "dolly"
    CRANE = "crane"
    HANDHELD = "handheld"


class CameraDirective(BaseModel):
    """Diretiva de câmera para uma cena."""
    angle: str = "frontal"
    movement: CameraMovement = CameraMovement.STATIC
    shot_size: ShotSize = ShotSize.MEDIUM
    notes: str = ""


class IngredientAssignment(BaseModel):
    """Ingrediente referenciado em uma cena.

    Vincula um ingrediente do Registry à sua posição/uso
    na cena, com referência opcional à Visual Bible.
    """
    ingredient_id: str
    ingredient_name: str
    placement: str = ""
    visual_bible_ref: Optional[str] = None


class SceneContract(BaseModel):
    """Contrato de renderização para uma cena.

    Transforma o roteiro em instruções testáveis: descrição
    narrativa, prompts compilados, ingredientes, câmera,
    transições e metadados de versionamento.
    """
    id: str = Field(default_factory=lambda: f"sc_{uuid4().hex[:12]}")
    scene_number: int
    description: str
    prompt_positive: str = ""
    prompt_negative: str = ""
    duration: int = 5
    transition_in: TransitionType = TransitionType.CUT
    transition_out: TransitionType = TransitionType.CUT
    camera: CameraDirective = Field(default_factory=CameraDirective)
    ingredients: List[IngredientAssignment] = Field(default_factory=list)
    style: str = ""
    status: SceneContractStatus = SceneContractStatus.DRAFT
    notes: str = ""
    version: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SceneContractService:
    """Serviço de contratos de cena.

    Mantém o conjunto de contratos que traduzem o roteiro
    em instruções precisas para cada engine de render.
    """

    def __init__(self):
        self._contracts: Dict[str, SceneContract] = {}

    def create(self, contract: SceneContract) -> str:
        """Registra um novo contrato de cena."""
        if not contract.description.strip():
            raise ValueError("description cannot be empty")
        if contract.scene_number < 0:
            raise ValueError("scene_number must be non-negative")
        now = datetime.now(timezone.utc)
        contract.version = 1
        contract.created_at = now
        contract.updated_at = now
        self._contracts[contract.id] = contract
        return contract.id

    def get(self, contract_id: str) -> Optional[SceneContract]:
        """Busca contrato por ID."""
        return self._contracts.get(contract_id)

    def get_by_scene_number(self, scene_number: int) -> Optional[SceneContract]:
        """Busca contrato pelo número da cena."""
        for c in self._contracts.values():
            if c.scene_number == scene_number:
                return c
        return None

    def update(self, contract_id: str, **updates: Any) -> SceneContract:
        """Atualiza campos de um contrato.

        Incrementa a versão automaticamente.
        """
        contract = self._contracts.get(contract_id)
        if not contract:
            raise KeyError(f"SceneContract not found: {contract_id}")

        for key, value in updates.items():
            if hasattr(contract, key) and key not in ("id", "scene_number", "created_at", "version"):
                setattr(contract, key, value)

        contract.version += 1
        contract.updated_at = datetime.now(timezone.utc)
        return contract

    def delete(self, contract_id: str) -> bool:
        """Remove um contrato."""
        if contract_id not in self._contracts:
            return False
        del self._contracts[contract_id]
        return True

    def list(
        self,
        status: Optional[SceneContractStatus] = None,
        sort_by_scene: bool = True,
    ) -> List[SceneContract]:
        """Lista contratos, opcionalmente filtrados por status."""
        result = list(self._contracts.values())
        if status is not None:
            result = [c for c in result if c.status == status]
        if sort_by_scene:
            result.sort(key=lambda c: c.scene_number)
        return result

    def search(self, query: str) -> List[SceneContract]:
        """Busca contratos por descrição ou notas (case-insensitive)."""
        q = query.lower()
        return [
            c for c in self._contracts.values()
            if q in c.description.lower() or q in c.notes.lower()
        ]

    def get_contracts_for_ingredient(self, ingredient_id: str) -> List[SceneContract]:
        """Busca todas as cenas que referenciam um ingrediente."""
        return [
            c for c in self._contracts.values()
            if any(ing.ingredient_id == ingredient_id for ing in c.ingredients)
        ]

    def reorder(self, contract_ids: List[str]) -> List[SceneContract]:
        """Reordena cenas, reatribuindo scene_number sequencialmente."""
        reordered = []
        next_number = 1
        for cid in contract_ids:
            contract = self._contracts.get(cid)
            if contract:
                contract.scene_number = next_number
                next_number += 1
                contract.version += 1
                contract.updated_at = datetime.now(timezone.utc)
                reordered.append(contract)
        reordered.sort(key=lambda c: c.scene_number)
        return reordered

    def count(self) -> int:
        """Número total de contratos."""
        return len(self._contracts)

    def clear(self) -> None:
        """Limpa todos os contratos (útil para testes)."""
        self._contracts.clear()
