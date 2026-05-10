"""RenderPlan schema (RND-600).

Plano que escolhe engine por cena com base em:
(1) disponibilidade da engine,
(2) VRAM disponível,
(3) perfil de qualidade configurado.
Decide qual engine renderiza cada cena.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.prompt_compiler import EngineType


class RenderQuality(str, Enum):
    """Perfis de qualidade de renderização."""
    DRAFT = "draft"
    STANDARD = "standard"
    HIGH = "high"


class EngineSelectionReason(str, Enum):
    """Motivos para escolha de engine."""
    PREFERRED_AVAILABLE = "preferred_available"
    FALLBACK_NO_GPU = "fallback_no_gpu"
    FALLBACK_VRAM_LIMIT = "fallback_vram_limit"
    FALLBACK_UNAVAILABLE = "fallback_unavailable"
    QUALITY_PROFILE = "quality_profile"
    USER_OVERRIDE = "user_override"


class SceneRenderAssignment(BaseModel):
    """Atribuição de engine para uma cena específica."""
    id: str = Field(default_factory=lambda: f"sra_{uuid4().hex[:12]}")
    scene_number: int
    scene_contract_id: str
    engine: EngineType
    reason: EngineSelectionReason
    reason_detail: str = ""
    estimated_vram_mb: int = 0
    quality: RenderQuality = RenderQuality.STANDARD


class RenderPlan(BaseModel):
    """Plano de renderização para um conjunto de cenas.

    Contém a atribuição de engine por cena, metadados
    de hardware considerado e perfil de qualidade.
    """
    id: str = Field(default_factory=lambda: f"rp_{uuid4().hex[:12]}")
    project_id: str = ""
    assignments: List[SceneRenderAssignment] = Field(default_factory=list)
    gpu_profile: str = "GTX 1660 Super (6GB)"
    vram_total_mb: int = 6144
    quality: RenderQuality = RenderQuality.STANDARD
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1


class RenderPlanService:
    """Service que gera RenderPlan a partir de cenas e disponibilidade.

    Regras:
    1. WanGP é a engine preferida (se disponível e VRAM suficiente)
    2. FFmpeg é fallback universal (sempre disponível)
    3. VACE é futuro, não selecionado automaticamente
    4. Cada atribuição registra motivo da escolha
    """

    def __init__(self, vram_total_mb: int = 6144):
        self._plans: Dict[str, RenderPlan] = {}
        self.vram_total_mb = vram_total_mb

    def generate_plan(
        self,
        scene_ids: List[str],
        project_id: str = "",
        engine_availability: Optional[Dict[str, bool]] = None,
        quality: RenderQuality = RenderQuality.STANDARD,
    ) -> RenderPlan:
        """Generate render plan for a list of scene contracts.

        Args:
            scene_ids: List of scene contract IDs (in order).
            project_id: Optional project identifier.
            engine_availability: Dict like {"wangp": True, "ffmpeg": True}.
            quality: Quality profile for rendering.

        Returns:
            RenderPlan with per-scene engine assignments.
        """
        if engine_availability is None:
            engine_availability = {"wangp": False, "ffmpeg": True, "vace": False}

        assignments: List[SceneRenderAssignment] = []

        for i, sc_id in enumerate(scene_ids):
            engine, reason, detail = self._select_engine(
                engine_availability, quality
            )
            assignment = SceneRenderAssignment(
                scene_number=i + 1,
                scene_contract_id=sc_id,
                engine=engine,
                reason=reason,
                reason_detail=detail,
                estimated_vram_mb=self._estimate_vram(engine),
                quality=quality,
            )
            assignments.append(assignment)

        plan = RenderPlan(
            project_id=project_id,
            assignments=assignments,
            vram_total_mb=self.vram_total_mb,
            quality=quality,
        )
        self._plans[plan.id] = plan
        return plan

    def _select_engine(
        self,
        availability: Dict[str, bool],
        quality: RenderQuality,
    ) -> tuple:
        """Select best engine based on availability and profile.

        Returns:
            (EngineType, EngineSelectionReason, detail_string)
        """
        wangp_avail = availability.get("wangp", False)
        ffmpeg_avail = availability.get("ffmpeg", True)
        vram_per_scene = 3072  # ~3GB per scene for WanGP 1.3B

        if wangp_avail and vram_per_scene <= self.vram_total_mb:
            if quality == RenderQuality.HIGH:
                return (
                    EngineType.WAN_GP,
                    EngineSelectionReason.QUALITY_PROFILE,
                    f"WanGP selecionado por perfil {quality.value} com {vram_per_scene}MB VRAM disponivel",
                )
            return (
                EngineType.WAN_GP,
                EngineSelectionReason.PREFERRED_AVAILABLE,
                f"WanGP disponivel, VRAM {vram_per_scene}MB < {self.vram_total_mb}MB total",
            )

        if wangp_avail and vram_per_scene > self.vram_total_mb:
            return (
                EngineType.FFMPEG,
                EngineSelectionReason.FALLBACK_VRAM_LIMIT,
                f"WanGP requer {vram_per_scene}MB, mas VRAM total é {self.vram_total_mb}MB",
            )

        if ffmpeg_avail:
            return (
                EngineType.FFMPEG,
                EngineSelectionReason.FALLBACK_NO_GPU,
                "WanGP indisponivel, FFmpeg fallback universal",
            )

        return (
            EngineType.FFMPEG,
            EngineSelectionReason.FALLBACK_UNAVAILABLE,
            "Nenhuma engine disponivel, FFmpeg fallback final",
        )

    def _estimate_vram(self, engine: EngineType) -> int:
        """Estimate VRAM usage per scene for given engine."""
        estimates = {
            EngineType.WAN_GP: 3072,
            EngineType.FFMPEG: 128,
            EngineType.VACE: 2048,
        }
        return estimates.get(engine, 0)

    def get_plan(self, plan_id: str) -> Optional[RenderPlan]:
        """Retrieve a stored plan by ID."""
        return self._plans.get(plan_id)

    def list_plans(self) -> List[RenderPlan]:
        """List all stored plans."""
        return list(self._plans.values())
