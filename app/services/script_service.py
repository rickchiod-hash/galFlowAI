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
from app.adapters.llm.base_provider import TemplateProvider

logger = setup_logger()

# TODO_TECNICO(SCRIPT_SERVICE):
# 1) Separar IO de arquivos da regra de negócio (SRP).
# 2) Garantir idempotência para salvar/aprovar versões de roteiro.
# 3) Introduzir Result Object padronizado para erros/retornos.
# 4) Criar testes unitários para geração, versionamento e aprovação.

# ========== Generation ==========

_PROVIDER_CLASSES = {
    "template": ("app.adapters.llm.base_provider", "TemplateProvider"),
    "lmstudio": ("app.adapters.llm.lmstudio_provider", "LMStudioProvider"),
    "koboldcpp": ("app.adapters.llm.koboldcpp_provider", "KoboldCppProvider"),
    "llamacpp": ("app.adapters.llm.llamacpp_provider", "LlamaCppProvider"),
    "gpt4all": ("app.adapters.llm.gpt4all_provider", "GPT4AllProvider"),
}


# TODO(GAL-902, type=follow-up): enhanced prompt with template context should trim template to key structure only
# Contexto: full template script (6 cenas) sent as context — may overwhelm small models
# Dependencia: GAL-900 (performance)
# Criterio de aceite: template context condensed to scene headers + key elements only
# Backlog: docs/project-control/05_BACKLOG_PRIORIZADO.md#gal-902

def _condense_template(template_script: str) -> str:
    """Extract scene headers and all content fields from template script."""
    lines = template_script.split("\n")
    condensed = []
    for line in lines:
        stripped = line.strip()
        if (stripped.startswith("[Cena") or stripped.startswith("Texto:")
                or stripped.startswith("Narracao:") or stripped.startswith("Prompt")):
            condensed.append(stripped)
    if len(condensed) < 3:
        return template_script[:500]
    return "\n".join(condensed)


def _build_enhanced_prompt(briefing: str, template_script: str) -> str:
    """Build enriched prompt: briefing + condensed template context + pt-BR instruction."""
    condensed = _condense_template(template_script)
    return (
        briefing + "\n\n"
        "---\n"
        "Estrutura de referencia (melhore o conteudo em pt-BR):\n"
        + condensed + "\n\n"
        "---\n"
        "IMPORTANTE: Escreva TODO o roteiro em portugues brasileiro (pt-BR). "
        "Use linguagem natural, criativa e autenticamente brasileira. "
        "Mantenha a estrutura de cenas com tempos, textos na tela, narracao e prompts visuais.\n\n"
        "Roteiro melhorado em pt-BR:\n"
    )


def generate_script_with_provider(briefing: str, provider_name: str = "auto") -> Dict:
    """Generate script using a specific named provider.

    Fluxo:
      1. Se nao for template, gera roteiro base via TemplateProvider como contexto.
      2. Envia briefing + contexto + instrucao pt-BR para o provider real.
      3. Se o provider real falhar, usa TemplateProvider como fallback.

    Args:
        briefing: The product briefing text (min 10 chars)
        provider_name: One of "auto", "template", "lm_studio",
                       "koboldcpp", "llamacpp", "gpt4all"

    Returns:
        Dict with keys: ok, script, provider, time, quality, error
    """
    FALLBACK_TIMEOUT = 120

    if provider_name == "auto":
        return generate_script_with_llm(briefing, mode="auto")

    if provider_name not in _PROVIDER_CLASSES:
        return {"ok": False, "error": f"Provider desconhecido: {provider_name}"}

    if provider_name == "template":
        return _call_template(briefing)

    # Gera base via TemplateProvider como contexto
    template_result = _call_template(briefing)
    template_script = template_result["script"]
    enhanced_prompt = _build_enhanced_prompt(briefing, template_script)

    mod_path, cls_name = _PROVIDER_CLASSES[provider_name]
    try:
        mod = __import__(mod_path, fromlist=[cls_name])
        cls = getattr(mod, cls_name)
        provider = cls()
        actual_cls_name = cls_name

        start = time.time()
        try:
            result = provider.generate(enhanced_prompt, timeout=FALLBACK_TIMEOUT)
            elapsed = time.time() - start
        except Exception as e:
            elapsed = time.time() - start
            result = None
            logger.warning(
                "Provider %s falhou em %.1fs: %s. Usando TemplateProvider como fallback.",
                provider_name, elapsed, e
            )

        if result and isinstance(result, str) and len(result.strip()) > 50:
            script_text = result
            logger.info(
                "Script generated via %s com contexto template (time: %.2fs)",
                actual_cls_name, elapsed
            )
            return {
                "ok": True,
                "script": script_text,
                "provider": actual_cls_name,
                "time": elapsed,
                "quality": "template",
            }

        if result is None:
            logger.warning(
                "Provider %s falhou em %.1fs (timeout=%ds), usando TemplateProvider como fallback.",
                provider_name, elapsed, FALLBACK_TIMEOUT
            )
        else:
            logger.warning(
                "Provider %s retornou resultado invalido em %.1fs, usando TemplateProvider como fallback.",
                provider_name, elapsed
            )

        fallback_start = time.time()
        fallback_result = _call_template(briefing)
        fallback_elapsed = time.time() - fallback_start

        script_text = fallback_result["script"]
        logger.info(
            "Fallback: Script generated via TemplateProvider (time: %.2fs)",
            fallback_elapsed
        )
        return {
            "ok": True,
            "script": script_text,
            "provider": "TemplateProvider",
            "time": elapsed + fallback_elapsed,
            "quality": "fallback",
        }

    except Exception as e:
        logger.error("Falha ao gerar roteiro com %s: %s", provider_name, e)
        return {"ok": False, "error": str(e)}


def _call_template(briefing: str) -> Dict:
    """Generate script using TemplateProvider directly."""
    provider = TemplateProvider()
    start = time.time()
    script = provider.generate(briefing)
    elapsed = time.time() - start
    text = script if isinstance(script, str) else ""
    return {
        "ok": True,
        "script": text,
        "provider": "TemplateProvider",
        "time": elapsed,
        "quality": "template",
    }


def get_provider_diagnostics() -> Dict[str, Any]:
    """Get full provider diagnostics including router's detect_available."""
    status = get_provider_status()
    router = ProviderRouter("auto")
    available = router.detect_available()
    return {
        "status": status,
        "router_available": available,
    }


def get_provider_status() -> Dict[str, bool]:
    """Check availability of all providers."""
    status = {}
    for name, (mod_path, cls_name) in _PROVIDER_CLASSES.items():
        try:
            mod = __import__(mod_path, fromlist=[cls_name])
            cls = getattr(mod, cls_name)
            provider = cls()
            status[name] = provider.is_available()
        except Exception:
            status[name] = False
    return status


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
        return {
            "ok": True,
            "script": result.get("script", ""),
            "provider": result.get("provider", "Unknown"),
            "time": result.get("time", 0),
            "quality": result.get("quality", "fallback")
        }
    except Exception as e:
        logger.error("CAUSA: Script generation failed | CORREÇÃO: Check LLM provider availability")
        return {"ok": False, "error": str(e)}


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
        return json.loads(versions_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("CAUSA: Failed to load versions: %s | CORREÇÃO: Verify script_versions.json exists and is valid JSON", e)
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
        else:
            return {"ok": False, "error": "Previous version file not found"}
        
        return {"ok": True, "script": script, "version": version}
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
