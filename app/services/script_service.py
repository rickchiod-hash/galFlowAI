"""
Script Service - Single layer for script business logic.
Provides: generate, edit, improve, versioning, approval.
"""
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.logging_config import setup_logger
from app.config import PROJECTS_DIR
from app.adapters.llm import ProviderRouter

logger = setup_logger()

# TODO_TECNICO(SCRIPT_SERVICE):
# 1) Separar IO de arquivos da regra de negócio (SRP).
# 2) Garantir idempotência para salvar/aprovar versões de roteiro.
# 3) Introduzir Result Object padronizado para erros/retornos.
# 4) Criar testes unitários para geração, versionamento e aprovação.

# ========== Generation ==========

def generate_script_with_llm(briefing: str, mode: str = "auto") -> Dict:
    """
    Generate script using available LLM providers.
    mode: 'fast', 'quality', 'safe', 'template'
    """
    router = ProviderRouter(mode)
    
    # Detect available providers
    available = router.detect_available()
    logger.info("Available providers: %s", available)
    
    # Use appropriate mode
    if mode == "auto":
        if any(v for k, v in available.items() if k != "template"):
            mode = "safe"  # Try LLMs first
        else:
            mode = "fast"  # Only template available
    
    try:
        if mode in ("fast", "quality"):
            # Check if there's a running event loop to avoid asyncio.run conflicts
            try:
                asyncio.get_running_loop()
                # Running loop exists (e.g., FastAPI endpoint), use safe mode
                result = router.generate_script_safe(briefing)
            except RuntimeError:
                # No running loop, safe to use asyncio.run for async providers
                if mode == "fast":
                    result = asyncio.run(router.generate_script_fast(briefing))
                else:  # quality
                    result = asyncio.run(router.generate_script_quality(briefing))
        else:  # safe or auto
            result = router.generate_script_safe(briefing)
        
        logger.info(
            "Script generated using %s (time: %.2fs, quality: %s)",
            result["provider"], result["time"], result["quality"]
        )
        return result
    except Exception as e:
        logger.error("Script generation failed: %s", e)
        # Ultimate fallback
        from app.adapters.llm.base_provider import TemplateProvider
        tp = TemplateProvider()
        return {
            "script": tp.generate(briefing),
            "provider": "TemplateProvider",
            "time": 0,
            "quality": "fallback"
        }


# ========== Version Management ==========

def _get_script_dir(project_id: str) -> Path:
    """Get script directory for project."""
    return PROJECTS_DIR / project_id / "script"


def _load_versions(project_id: str) -> List[Dict]:
    """Load all script versions."""
    script_dir = _get_script_dir(project_id)
    versions_file = script_dir / "script_versions.json"
    
    if not versions_file.exists():
        return []
    
    try:
        return json.loads(versions_file.read_text(encoding="utf-8"
    except Exception as e:
        logger.error("Failed to load versions: %s", e)
        return []


def _save_versions(project_id: str, versions: List[Dict]):
    """Save versions list."""
    script_dir = _get_script_dir(project_id)
    script_dir.mkdir(parents=True, exist_ok=True)
    versions_file = script_dir / "script_versions.json"
    versions_file.write_text(
        json.dumps(versions, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def _next_version(project_id: str) -> str:
    """Get next version number."""
    versions = _load_versions(project_id)
    if not versions:
        return "v001"
    last = versions[-1]["version"]
    num = int(last[1:]) + 1
    return "v{:03d}".format(num)


def save_manual_edit(project_id: str, script_markdown: str, note: str = "Edição manual") -> Dict:
    """Save manually edited script as new version."""
    try:
        version = _next_version(project_id)
        script_dir = _get_script_dir(project_id)
        script_dir.mkdir(parents=True, exist_ok=True)
        
        # Save version file
        md_file = script_dir / f"script_{version}.md"
        md_file.write_text(script_markdown, encoding="utf-8")
        
        # Save metadata
        json_file = script_dir / f"script_{version}.json"
        metadata = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "note": note,
            "provider_used": "Manual",
            "response_time_seconds": 0,
            "quality_score": 0,
            "status": "Draft"
        }
        json_file.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        
        # Update versions list
        versions = _load_versions(project_id)
        versions.append(metadata)
        _save_versions(project_id, versions)
        
        logger.info("Manual edit saved as %s", version)
        return {"ok": True, "version": version, "script": script_markdown}
    except Exception as e:
        logger.error("Failed to save manual edit: %s", e)
        return {"ok": False, "error": str(e)}


# ========== Improvement ==========

def improve_script(project_id: str, briefing: str = "") -> Dict:
    """Improve existing script."""
    try:
        current = load_current_script(project_id)
        if not current.get("script"):
            return {"ok": False, "error": "No current script found"}
        
        # Use LLM to improve
        from app.pipeline.script_generator import generate_script
        improved = generate_script(briefing if briefing else current["script"], project_id)
        
        # Save as new version
        result = save_manual_edit(project_id, improved, "Script improved")
        return {"ok": True, "script": improved, "version": result["version"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def complement_script(project_id: str) -> Dict:
    """Complement existing script."""
    try:
        current = load_current_script(project_id)
        if not current.get("script"):
            return {"ok": False, "error": "No current script found"}
        
        # Add complementary content
        script = current["script"]
        if "[Complemento]" not in script:
            script += "\n\n[Complemento - 10s]\nInformações adicionais sobre o produto.\nTexto: 'Saiba mais detalhes.'"
        
        result = save_manual_edit(project_id, script, "Complementado")
        return {"ok": True, "script": script, "version": result["version"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def make_script_more_viral(project_id: str) -> Dict:
    """Make script more viral."""
    try:
        current = load_current_script(project_id)
        if not current.get("script"):
            return {"ok": False, "error": "No current script found"}
        
        script = current["script"]
        # Add viral elements
        if "Hook" not in script:
            script = "[Hook - 3s]\nTexto: 'Voce nao pode perder isso!'\n\n" + script
        
        result = save_manual_edit(project_id, script, "Mais viral")
        return {"ok": True, "script": script, "version": result["version"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def make_script_more_premium(project_id: str) -> Dict:
    """Make script more premium."""
    try:
        current = load_current_script(project_id)
        if not current.get("script"):
            return {"ok": False, "error": "No current script found"}
        
        script = current["script"]
        # Add premium elements
        script = script.replace("Texto:", "Texto premium:")
        script = script.replace("Narracao:", "Narracao premium:")
        
        result = save_manual_edit(project_id, script, "Mais premium")
        return {"ok": True, "script": script, "version": result["version"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def make_script_more_direct(project_id: str) -> Dict:
    """Make script more direct for sales."""
    try:
        current = load_current_script(project_id)
        if not current.get("script"):
            return {"ok": False, "error": "No current script found"}
        
        script = current["script"]
        # Make calls to action more direct
        if "CTA" not in script:
            script += "\n\n[Cena CTA - 3s]\nTexto: 'Compre agora!'\nNarracao: 'Nao perca tempo.'"
        
        result = save_manual_edit(project_id, script, "Mais direto")
        return {"ok": True, "script": script, "version": result["version"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ========== Version Control ==========

def create_new_version(project_id: str) -> Dict:
    """Create new empty version."""
    try:
        version = _next_version(project_id)
        script_dir = _get_script_dir(project_id)
        script_dir.mkdir(parents=True, exist_ok=True)
        
        # Create empty script
        md_file = script_dir / f"script_{version}.md"
        md_file.write_text("[Nova versão]\nAdicione o conteudo aqui.", encoding="utf-8")
        
        # Save metadata
        json_file = script_dir / f"script_{version}.json"
        metadata = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "note": "Nova versão criada",
            "provider_used": "Manual",
            "response_time_seconds": 0,
            "quality_score": 0,
            "status": "Draft"
        }
        json_file.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        
        # Update versions list
        versions = _load_versions(project_id)
        versions.append(metadata)
        _save_versions(project_id, versions)
        
        logger.info("New version created: %s", version)
        return {"ok": True, "version": version, "script": md_file.read_text(encoding="utf-8")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def restore_previous_version(project_id: str) -> Dict:
    """Restore previous version as current."""
    try:
        versions = _load_versions(project_id)
        if len(versions) < 2:
            return {"ok": False, "error": "No previous version to restore"}
        
        # Get previous version
        prev = versions[-2]
        version = prev["version"]
        
        # Load that version's script
        script_dir = _get_script_dir(project_id)
        md_file = script_dir / f"script_{version}.md"
        if md_file.exists():
            script = md_file.read_text(encoding="utf-8")
            return {"ok": True, "script": script, "version": version}
        else:
            return {"ok": False, "error": "Previous version file not found"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def approve_script(project_id: str) -> Dict:
    """Approve current script for production."""
    try:
        current = load_current_script(project_id)
        if not current.get("script"):
            return {"ok": False, "error": "No current script to approve"}
        
        script = current["script"]
        script_dir = _get_script_dir(project_id)
        
        # Save as approved
        approved_md = script_dir / "script_approved.md"
        approved_md.write_text(script, encoding="utf-8")
        
        approved_json = script_dir / "script_approved.json"
        metadata = {
            "approved_at": datetime.now().isoformat(),
            "version": current.get("version", "unknown"),
            "script": script
        }
        approved_json.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        
        # Update status in versions
        versions = _load_versions(project_id)
        for v in versions:
            if v["version"] == current.get("version"):
                v["status"] = "Approved"
                break
        _save_versions(project_id, versions)
        
        logger.info("Script approved: %s", current.get("version"))
        return {"ok": True, "script": script, "status": "Approved"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ========== Load Functions ==========

def load_current_script(project_id: str) -> Dict:
    """Load current script (approved if exists, else latest)."""
    try:
        script_dir = _get_script_dir(project_id)
        
        # Try approved first
        approved = script_dir / "script_approved.md"
        if approved.exists():
            version = "approved"
            script = approved.read_text(encoding="utf-8")
        else:
            # Load latest version
            versions = _load_versions(project_id)
            if not versions:
                return {"ok": False, "error": "No script found"}
            latest = versions[-1]
            version = latest["version"]
            md_file = script_dir / f"script_{version}.md"
            if md_file.exists():
                script = md_file.read_text(encoding="utf-8")
            else:
                return {"ok": False, "error": "Script file not found"}
        
        return {"ok": True, "script": script, "version": version}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def load_script_versions(project_id: str) -> List[Dict]:
    """Load all script versions."""
    try:
        versions = _load_versions(project_id)
        return [{"version": v["version"], "note": v.get("note", ""), "status": v.get("status", "Draft")} for v in versions]
    except Exception as e:
        logger.error("Failed to load script versions: %s", e)
        return []


# ========== Validation ==========

def validate_script_quality(script: str) -> Dict:
    """Validate script quality."""
    result = {"valid": True, "score": 80, "issues": []}
    
    if not script or len(script.strip()) < 100:
        result["valid"] = False
        result["score"] = 0
        result["issues"].append("Script too short")
    
    # Check for robotic phrases
    bad_phrases = [
        "Apresentamos", "Solucao completa", "Adquira agora",
        "pessoas que tem interesse", "produto de qualidade"
    ]
    script_lower = script.lower()
    for phrase in bad_phrases:
        if phrase in script_lower:
            result["score"] = 40
            result["issues"].append("Contains robotic phrase: " + phrase)
            break
    
    # Check for required elements
    if "[Cena" not in script:
        result["valid"] = False
        result["score"] = 30
        result["issues"].append("No scenes found")
    
    if "CTA" not in script and "Chamada" not in script:
        result["score"] = max(result["score"] - 20, 0)
        result["issues"].append("Missing call to action")
    
    return result


# ========== Async Support ==========

import asyncio

async def generate_script_fast(briefing: str, timeout: int = 5) -> Dict:
    """Async wrapper for fast mode."""
    return generate_script_with_llm(briefing, mode="fast")


async def generate_script_quality(briefing: str, timeout: int = 15) -> Dict:
    """Async wrapper for quality mode."""
    return generate_script_with_llm(briefing, mode="quality")
