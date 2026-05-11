"""RenderPlan schema (RND-600, RND-602).

Plano que escolhe engine por cena com base em:
(1) disponibilidade da engine,
(2) VRAM disponível,
(3) perfil de qualidade configurado,
(4) perfil de GPU (GTX 1660 Super, etc).
Decide qual engine renderiza cada cena.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
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


@dataclass
class GpuProfile:
    """Perfil de GPU definindo  orçamento de VRAM e resoluções seguras.

    Cada perfil documenta uma GPU conhecida com seus limites reais
    para evitar OOM durante renderização com engine IA.
    """
    name: str
    vram_total_mb: int
    max_resolution: Tuple[int, int]
    recommended_resolution: Tuple[int, int]
    wangp_vram_per_scene_mb: int
    ffmpeg_vram_per_scene_mb: int = 128
    vace_vram_per_scene_mb: int = 2048


class GpuProfileCatalog:
    """Catálogo de perfis de GPU pré-definidos.

    Fornece os perfis conhecidos e testados para o RenderPlanService.
    O perfil GTX 1660 Super (6GB) é o mínimo suportado.
    """

    _profiles: Dict[str, GpuProfile] = {}

    @classmethod
    def _init(cls) -> None:
        if not cls._profiles:
            profiles = [
                GpuProfile(
                    name="GTX 1660 Super (6GB)",
                    vram_total_mb=6144,
                    max_resolution=(832, 512),
                    recommended_resolution=(640, 480),
                    wangp_vram_per_scene_mb=3072,
                ),
                GpuProfile(
                    name="RTX 3060 (12GB)",
                    vram_total_mb=12288,
                    max_resolution=(1024, 576),
                    recommended_resolution=(832, 512),
                    wangp_vram_per_scene_mb=4096,
                ),
                GpuProfile(
                    name="Fallback (CPU/FFmpeg)",
                    vram_total_mb=512,
                    max_resolution=(480, 360),
                    recommended_resolution=(480, 360),
                    wangp_vram_per_scene_mb=0,
                ),
            ]
            cls._profiles = {p.name: p for p in profiles}

    @classmethod
    def get(cls, name: str) -> Optional[GpuProfile]:
        cls._init()
        return cls._profiles.get(name)

    @classmethod
    def get_default(cls) -> GpuProfile:
        cls._init()
        return cls._profiles.get("GTX 1660 Super (6GB)")

    @classmethod
    def list_profiles(cls) -> List[GpuProfile]:
        cls._init()
        return list(cls._profiles.values())

    @classmethod
    def get_profile_for_vram(cls, vram_mb: int) -> GpuProfile:
        """Retorna o perfil mais adequado para a VRAM disponível."""
        cls._init()
        sorted_profiles = sorted(
            cls._profiles.values(),
            key=lambda p: p.vram_total_mb,
        )
        best = sorted_profiles[0]
        for p in sorted_profiles:
            if p.vram_total_mb <= vram_mb:
                best = p
        return best


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
    resolution: Tuple[int, int] = (640, 480)


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
    max_resolution: Tuple[int, int] = (832, 512)


class RenderPlanService:
    """Service que gera RenderPlan a partir de cenas e disponibilidade.

    Regras:
    1. WanGP é a engine preferida (se disponível e VRAM suficiente)
    2. FFmpeg é fallback universal (sempre disponível)
    3. VACE é futuro, não selecionado automaticamente
    4. Cada atribuição registra motivo da escolha
    5. Perfil de GPU define resoluções e  orçamento de VRAM
    """

    def __init__(self, vram_total_mb: int = 6144, gpu_profile: Optional[GpuProfile] = None):
        self._plans: Dict[str, RenderPlan] = {}
        self.vram_total_mb = vram_total_mb
        self.gpu_profile = gpu_profile or GpuProfileCatalog.get_default()

    def generate_plan(
        self,
        scene_ids: List[str],
        project_id: str = "",
        engine_availability: Optional[Dict[str, bool]] = None,
        quality: RenderQuality = RenderQuality.STANDARD,
        gpu_profile: Optional[GpuProfile] = None,
    ) -> RenderPlan:
        """Generate render plan for a list of scene contracts.

        Args:
            scene_ids: List of scene contract IDs (in order).
            project_id: Optional project identifier.
            engine_availability: Dict like {"wangp": True, "ffmpeg": True}.
            quality: Quality profile for rendering.
            gpu_profile: Optional GPU profile override.

        Returns:
            RenderPlan with per-scene engine assignments.
        """
        if engine_availability is None:
            engine_availability = {"wangp": False, "ffmpeg": True, "vace": False}

        profile = gpu_profile or self.gpu_profile
        vram_total = profile.vram_total_mb
        resolution = self._resolve_resolution(profile, quality)

        assignments: List[SceneRenderAssignment] = []

        for i, sc_id in enumerate(scene_ids):
            engine, reason, detail = self._select_engine(
                engine_availability, quality, profile
            )
            assignment = SceneRenderAssignment(
                scene_number=i + 1,
                scene_contract_id=sc_id,
                engine=engine,
                reason=reason,
                reason_detail=detail,
                estimated_vram_mb=self._estimate_vram(engine, profile),
                quality=quality,
                resolution=resolution,
            )
            assignments.append(assignment)

        plan = RenderPlan(
            project_id=project_id,
            assignments=assignments,
            gpu_profile=profile.name,
            vram_total_mb=vram_total,
            quality=quality,
            max_resolution=profile.max_resolution,
        )
        self._plans[plan.id] = plan
        return plan

    def _resolve_resolution(
        self, profile: GpuProfile, quality: RenderQuality
    ) -> Tuple[int, int]:
        """Resolve resolução baseada no perfil e qualidade."""
        if quality == RenderQuality.HIGH:
            return profile.max_resolution
        if quality == RenderQuality.DRAFT:
            return (480, 360)
        return profile.recommended_resolution

    def _select_engine(
        self,
        availability: Dict[str, bool],
        quality: RenderQuality,
        profile: Optional[GpuProfile] = None,
    ) -> Tuple[EngineType, EngineSelectionReason, str]:
        """Select best engine based on availability and profile.

        Returns:
            (EngineType, EngineSelectionReason, detail_string)
        """
        wangp_avail = availability.get("wangp", False)
        ffmpeg_avail = availability.get("ffmpeg", True)
        p = profile or self.gpu_profile
        vram_per_scene = p.wangp_vram_per_scene_mb
        vram_total = p.vram_total_mb

        if wangp_avail and vram_per_scene > 0 and vram_per_scene <= vram_total:
            if quality == RenderQuality.HIGH:
                return (
                    EngineType.WAN_GP,
                    EngineSelectionReason.QUALITY_PROFILE,
                    f"WanGP por perfil {quality.value}, perfil {p.name}, {vram_per_scene}MB < {vram_total}MB",
                )
            return (
                EngineType.WAN_GP,
                EngineSelectionReason.PREFERRED_AVAILABLE,
                f"WanGP disponivel, perfil {p.name}, VRAM {vram_per_scene}MB < {vram_total}MB",
            )

        if wangp_avail and (vram_per_scene <= 0 or vram_per_scene > vram_total):
            return (
                EngineType.FFMPEG,
                EngineSelectionReason.FALLBACK_VRAM_LIMIT,
                f"WanGP requer {vram_per_scene}MB, mas VRAM {vram_total}MB (perfil {p.name})",
            )

        if ffmpeg_avail:
            return (
                EngineType.FFMPEG,
                EngineSelectionReason.FALLBACK_NO_GPU,
                f"WanGP indisponivel, perfil {p.name}, FFmpeg fallback universal",
            )

        return (
            EngineType.FFMPEG,
            EngineSelectionReason.FALLBACK_UNAVAILABLE,
            "Nenhuma engine disponivel, FFmpeg fallback final",
        )

    def _estimate_vram(self, engine: EngineType, profile: Optional[GpuProfile] = None) -> int:
        """Estimate VRAM usage per scene for given engine and profile."""
        p = profile or self.gpu_profile
        estimates = {
            EngineType.WAN_GP: p.wangp_vram_per_scene_mb,
            EngineType.FFMPEG: p.ffmpeg_vram_per_scene_mb,
            EngineType.VACE: p.vace_vram_per_scene_mb,
        }
        return estimates.get(engine, 0)

    def get_plan(self, plan_id: str) -> Optional[RenderPlan]:
        """Retrieve a stored plan by ID."""
        return self._plans.get(plan_id)

    def list_plans(self) -> List[RenderPlan]:
        """List all stored plans."""
        return list(self._plans.values())
