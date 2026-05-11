"""AudioPlan schema (AUD-700).

Define o plano de narração para um conjunto de cenas:
mapeia cada cena ao seu texto de narração, estilo
e duração estimada. Gera narration_script.md como
artefato legível para revisão humana e entrada do TTS.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class AudioPlanStatus(str, Enum):
    """Status do plano de áudio."""
    DRAFT = "draft"
    FINALIZED = "finalized"


class NarrationEntry(BaseModel):
    """Entrada de narração para uma cena específica."""
    scene_number: int
    scene_contract_id: str = ""
    narration_text: str
    style_notes: str = ""
    duration_seconds: float = 0.0
    tts_voice: str = "default"
    language: str = "pt-BR"


class AudioPlan(BaseModel):
    """Plano de narração para um conjunto de cenas.

    Contém as entradas de narração por cena, status
    de aprovação e metadados de versionamento.
    """
    id: str = Field(default_factory=lambda: f"ap_{uuid4().hex[:12]}")
    project_id: str = ""
    narrations: List[NarrationEntry] = Field(default_factory=list)
    status: AudioPlanStatus = AudioPlanStatus.DRAFT
    version: int = 1
    notes: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AudioPlanService:
    """Serviço de planos de narração.

    Mantém planos de áudio que mapeiam cada cena ao seu
    texto de narração, permitindo revisão humana antes
    da geração TTS.
    """

    def __init__(self):
        self._plans: Dict[str, AudioPlan] = {}

    def create(self, plan: AudioPlan) -> str:
        """Registra um novo plano de áudio."""
        if not plan.project_id.strip():
            raise ValueError("project_id cannot be empty")
        now = datetime.now(timezone.utc)
        plan.version = 1
        plan.created_at = now
        plan.updated_at = now
        self._plans[plan.id] = plan
        return plan.id

    def get(self, plan_id: str) -> Optional[AudioPlan]:
        """Busca plano por ID."""
        return self._plans.get(plan_id)

    def get_by_project(self, project_id: str) -> Optional[AudioPlan]:
        """Busca plano pelo ID do projeto."""
        for p in self._plans.values():
            if p.project_id == project_id:
                return p
        return None

    def update(self, plan_id: str, **updates: Any) -> AudioPlan:
        """Atualiza campos de um plano.

        Incrementa a versão automaticamente.
        """
        plan = self._plans.get(plan_id)
        if not plan:
            raise KeyError(f"AudioPlan not found: {plan_id}")

        for key, value in updates.items():
            if hasattr(plan, key) and key not in ("id", "created_at", "version"):
                setattr(plan, key, value)

        plan.version += 1
        plan.updated_at = datetime.now(timezone.utc)
        return plan

    def delete(self, plan_id: str) -> bool:
        """Remove um plano."""
        if plan_id not in self._plans:
            return False
        del self._plans[plan_id]
        return True

    def list(
        self,
        status: Optional[AudioPlanStatus] = None,
    ) -> List[AudioPlan]:
        """Lista planos, opcionalmente filtrados por status."""
        result = list(self._plans.values())
        if status is not None:
            result = [p for p in result if p.status == status]
        return result

    def add_narration(self, plan_id: str, entry: NarrationEntry) -> AudioPlan:
        """Adiciona entrada de narração a um plano."""
        plan = self._plans.get(plan_id)
        if not plan:
            raise KeyError(f"AudioPlan not found: {plan_id}")
        plan.narrations.append(entry)
        plan.version += 1
        plan.updated_at = datetime.now(timezone.utc)
        return plan

    def remove_narration(self, plan_id: str, scene_number: int) -> AudioPlan:
        """Remove entrada de narração pelo número da cena."""
        plan = self._plans.get(plan_id)
        if not plan:
            raise KeyError(f"AudioPlan not found: {plan_id}")
        plan.narrations = [
            n for n in plan.narrations
            if n.scene_number != scene_number
        ]
        plan.version += 1
        plan.updated_at = datetime.now(timezone.utc)
        return plan

    def update_narration_text(
        self, plan_id: str, scene_number: int, narration_text: str
    ) -> AudioPlan:
        """Atualiza o texto de narração de uma cena."""
        plan = self._plans.get(plan_id)
        if not plan:
            raise KeyError(f"AudioPlan not found: {plan_id}")
        for n in plan.narrations:
            if n.scene_number == scene_number:
                n.narration_text = narration_text
                plan.version += 1
                plan.updated_at = datetime.now(timezone.utc)
                return plan
        raise ValueError(
            f"Narration not found for scene {scene_number}"
        )

    def generate_narration_script(self, plan_id: str) -> str:
        """Gera narration_script.md a partir do plano.

        Returns:
            Markdown string legível para revisão humana.
        """
        plan = self._plans.get(plan_id)
        if not plan:
            raise KeyError(f"AudioPlan not found: {plan_id}")

        lines = []
        lines.append(f"# Narration Script — Projeto: {plan.project_id}")
        lines.append("")
        lines.append(f"**Status:** {plan.status.value}")
        lines.append(f"**Versão:** {plan.version}")
        lines.append(f"**Idioma:** pt-BR")
        lines.append("")
        lines.append("---")
        lines.append("")

        sorted_narrations = sorted(
            plan.narrations, key=lambda n: n.scene_number
        )

        for i, entry in enumerate(sorted_narrations, 1):
            lines.append(f"## Cena {entry.scene_number}")
            lines.append("")
            lines.append(entry.narration_text)
            lines.append("")
            if entry.style_notes:
                lines.append(f"*Estilo:* {entry.style_notes}")
            if entry.duration_seconds > 0:
                lines.append(f"*Duração estimada:* {entry.duration_seconds:.1f}s")
            lines.append(f"*Voz TTS:* {entry.tts_voice}")
            lines.append("")
            if i < len(sorted_narrations):
                lines.append("---")
                lines.append("")

        total_duration = sum(n.duration_seconds for n in plan.narrations)
        lines.append("---")
        lines.append("")
        lines.append(f"**Total de cenas:** {len(sorted_narrations)}")
        lines.append(f"**Duração total estimada:** {total_duration:.1f}s")
        lines.append(f"**Idioma:** pt-BR")
        lines.append("")

        return "\n".join(lines)

    def count(self) -> int:
        """Número total de planos."""
        return len(self._plans)

    def clear(self) -> None:
        """Limpa todos os planos (útil para testes)."""
        self._plans.clear()
