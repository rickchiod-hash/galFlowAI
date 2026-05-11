"""SFX Manifest schema (AUD-703).

Registra licenca, origem e metadados de assets sonoros
para prevenir uso indevido de assets sem licenca.

SFX manifest e documental — nao afeta a execucao do pipeline.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class SFXLicenseType(str, Enum):
    """Tipos de licenca para assets de audio."""
    FREE = "free"
    ROYALTY_FREE = "royalty_free"
    LICENSED = "licensed"
    CC0 = "cc0"
    CC_BY = "cc_by"
    CUSTOM = "custom"
    UNKNOWN = "unknown"


class SFXAsset(BaseModel):
    """Schema de um asset sonoro no manifesto.

    Cada asset possui origem, licenca e metadados para
    rastreamento de uso e conformidade legal.
    """
    id: str = Field(default_factory=lambda: f"sfx_{uuid4().hex[:12]}")
    name: str
    file_path: str
    license_type: SFXLicenseType = SFXLicenseType.UNKNOWN
    license_url: str = ""
    origin: str = ""
    description: str = ""
    duration_seconds: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SFXManifest:
    """Catalogo versionado de assets sonoros.

    Mantem registro de licenca e origem de cada SFX.
    """

    def __init__(self):
        self._assets: Dict[str, SFXAsset] = {}

    def register(self, asset: SFXAsset) -> str:
        """Registra um novo asset sonoro."""
        if not asset.name.strip():
            raise ValueError("SFX name cannot be empty")
        if not asset.file_path.strip():
            raise ValueError("SFX file_path cannot be empty")
        now = datetime.now(timezone.utc)
        asset.version = 1
        asset.created_at = now
        asset.updated_at = now
        self._assets[asset.id] = asset
        return asset.id

    def get(self, asset_id: str) -> Optional[SFXAsset]:
        """Busca asset por ID."""
        return self._assets.get(asset_id)

    def get_by_name(self, name: str) -> Optional[SFXAsset]:
        """Busca asset por nome (case-insensitive, primeira correspondencia)."""
        for a in self._assets.values():
            if a.name.lower() == name.lower():
                return a
        return None

    def update(
        self, asset_id: str, **updates: Any
    ) -> SFXAsset:
        """Atualiza campos de um asset.

        Incrementa a versao automaticamente.
        """
        asset = self._assets.get(asset_id)
        if not asset:
            raise KeyError(f"SFXAsset not found: {asset_id}")

        protected = {"id", "created_at", "version"}
        for key, value in updates.items():
            if hasattr(asset, key) and key not in protected:
                setattr(asset, key, value)

        asset.version += 1
        asset.updated_at = datetime.now(timezone.utc)
        return asset

    def delete(self, asset_id: str) -> bool:
        """Remove um asset."""
        if asset_id not in self._assets:
            return False
        del self._assets[asset_id]
        return True

    def list(
        self,
        license_type: Optional[SFXLicenseType] = None,
    ) -> List[SFXAsset]:
        """Lista assets, opcionalmente filtrados por tipo de licenca."""
        result = list(self._assets.values())
        if license_type is not None:
            result = [a for a in result if a.license_type == license_type]
        return result

    def search(
        self,
        query: str,
    ) -> List[SFXAsset]:
        """Busca assets por nome ou descricao (case-insensitive)."""
        q = query.lower()
        return [
            a for a in self._assets.values()
            if q in a.name.lower() or q in a.description.lower()
        ]

    def count(self) -> int:
        """Numero total de assets."""
        return len(self._assets)

    def clear(self) -> None:
        """Limpa todos os assets (util para testes)."""
        self._assets.clear()
