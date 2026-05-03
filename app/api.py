"""
FastAPI V2 for Gal AI / FlowForgeAI - Local-first internal API.
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import GRADIO_HOST, GRADIO_PORT
from app.logging_config import setup_logger

logger = setup_logger()

app = FastAPI(
    title="Gal AI API",
    description="Local-first API for commercial video generation",
    version="2.0"
)

# CORS for local access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:7860", "http://localhost:7860"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Health ==========

class HealthResponse(BaseModel):
    status: str
    app: str
    mode: str
    ui: str
    fastapi: bool
    version: str


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": "Gal AI",
        "mode": "local",
        "ui": "gradio",
        "fastapi": True,
        "version": "2.0"
    }


# ========== LLM Providers ==========

class LLMProviderResponse(BaseModel):
    template: bool
    lmstudio: bool
    koboldcpp: bool
    gpt4all: bool
    llamacpp: bool
    openai_compatible_local: bool


@app.get("/api/llm/providers", response_model=LLMProviderResponse)
async def get_llm_providers():
    """Check which LLM providers are available."""
    try:
        from app.adapters.llm import ProviderRouter
        router = ProviderRouter()
        available = router.detect_available()
        return available
    except Exception as e:
        logger.error("Failed to detect providers: %s", e)
        return {
            "template": True,
            "lmstudio": False,
            "koboldcpp": False,
            "gpt4all": False,
            "llamacpp": False,
            "openai_compatible_local": False
        }


# ========== Script Generation ==========

class ScriptGenerateRequest(BaseModel):
    briefing: str
    project_id: Optional[str] = None
    provider: str = "auto"
    mode: str = "first_valid"
    timeout_seconds: int = 10
    endpoint: Optional[str] = None


class ScriptGenerateResponse(BaseModel):
    ok: bool
    provider_used: str
    fallback_used: bool
    response_time_seconds: float
    quality_score: int
    script_markdown: str
    script_json: Dict[str, Any]
    logs: List[str]


@app.post("/api/llm/script", response_model=ScriptGenerateResponse)
async def generate_script_api(request: ScriptGenerateRequest):
    """Generate script using LLM providers."""
    start = time.time()
    
    try:
        from app.services.script_service import generate_script_with_llm
        result = generate_script_with_llm(request.briefing, request.provider)
        
        return {
            "ok": True,
            "provider_used": result.get("provider", "Unknown"),
            "fallback_used": result.get("quality", "fallback") == "fallback",
            "response_time_seconds": result.get("time", 0),
            "quality_score": 0,
            "script_markdown": result.get("script", ""),
            "script_json": {},
            "logs": []
        }
    except Exception as e:
        logger.error("Script generation failed: %s", e)
        return {
            "ok": False,
            "provider_used": "TemplateProvider",
            "fallback_used": True,
            "response_time_seconds": time.time() - start,
            "quality_score": 0,
            "script_markdown": "",
            "script_json": {},
            "logs": [str(e)]
        }


# ========== Script Editing ==========

class ScriptSaveRequest(BaseModel):
    project_id: str
    script_markdown: str
    version_note: Optional[str] = None


@app.post("/api/projects/{project_id}/script/save-manual-edit")
async def save_manual_edit(project_id: str, request: ScriptSaveRequest):
    """Save manually edited script."""
    try:
        from app.services.script_service import save_manual_edit
        result = save_manual_edit(project_id, request.script_markdown, request.version_note)
        return {"ok": True, "version": result.get("version")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/improve")
async def improve_script(project_id: str, briefing: str = ""):
    """Improve existing script."""
    try:
        from app.services.script_service import improve_script
        result = improve_script(project_id, briefing)
        return {"ok": True, "script": result.get("script")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/more-viral")
async def make_more_viral(project_id: str):
    """Make script more viral."""
    try:
        from app.services.script_service import make_more_viral
        result = make_more_viral(project_id)
        return {"ok": True, "script": result.get("script")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/more-premium")
async def make_more_premium(project_id: str):
    """Make script more premium."""
    try:
        from app.services.script_service import make_more_premium
        result = make_more_premium(project_id)
        return {"ok": True, "script": result.get("script")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/more-direct")
async def make_more_direct(project_id: str):
    """Make script more direct for sales."""
    try:
        from app.services.script_service import make_more_direct
        result = make_more_direct(project_id)
        return {"ok": True, "script": result.get("script")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/new-version")
async def create_new_version(project_id: str):
    """Create new script version."""
    try:
        from app.services.script_service import create_new_version
        result = create_new_version(project_id)
        return {"ok": True, "version": result.get("version")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/restore-previous")
async def restore_previous_version(project_id: str):
    """Restore previous script version."""
    try:
        from app.services.script_service import restore_previous_version
        result = restore_previous_version(project_id)
        return {"ok": True, "version": result.get("version")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/script/approve")
async def approve_script(project_id: str):
    """Approve script for production."""
    try:
        from app.services.script_service import approve_script
        result = approve_script(project_id)
        return {"ok": True, "script": result.get("script")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/script/current")
async def get_current_script(project_id: str):
    """Get current script."""
    try:
        from app.services.script_service import load_current_script
        result = load_current_script(project_id)
        return {"ok": True, "script": result.get("script")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/script/versions")
async def get_script_versions(project_id: str):
    """Get all script versions."""
    try:
        from app.services.script_service import load_script_versions
        versions = load_script_versions(project_id)
        return {"ok": True, "versions": versions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Hardware ==========

@app.get("/api/hardware")
async def get_hardware_info():
    """Get hardware information."""
    try:
        from app.hardware import get_gpu_info
        return get_gpu_info()
    except Exception as e:
        logger.error("Hardware check failed: %s", e)
        return {"error": str(e)}


# ========== Jobs (Placeholder) ==========

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status."""
    return {"job_id": job_id, "status": "pending", "progress": 0}


@app.post("/api/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a job."""
    return {"ok": True, "job_id": job_id}


# ========== Video Generation ==========

class VideoGenerationRequest(BaseModel):
    """Request model for video generation."""
    product: str
    target_audience: str
    duration_seconds: int = 30
    style: str = "viral"
    keywords: Optional[List[str]] = None


@app.post("/api/generate-video")
async def generate_video(request: VideoGenerationRequest):
    """
    Generate a complete commercial video.
    
    Flow: Briefing -> Script -> Scenes -> Prompts -> Video -> Final
    """
    try:
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        from datetime import datetime
        
        # Create project ID
        project_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + request.product.replace(" ", "_")
        
        # Initialize pipeline
        pipeline = VideoGenerationPipeline()
        
        # Generate commercial
        result = pipeline.generate_commercial(
            project_id=project_id,
            product=request.product,
            target_audience=request.target_audience,
            duration_seconds=request.duration_seconds,
            style=request.style,
            keywords=request.keywords
        )
        
        if result.get("success"):
            return {
                "success": True,
                "project_id": project_id,
                "final_video": result.get("final_video"),
                "scenes_count": result.get("scenes_count"),
                "provider_used": result.get("provider_used")
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Erro desconhecido")
            )
            
    except Exception as e:
        logger.error("Erro ao gerar video: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/video-status/{project_id}")
async def get_video_status(project_id: str):
    """Get status of video generation project."""
    from app.config import PROJECTS_DIR
    from pathlib import Path
    import json
    
    project_dir = Path(PROJECTS_DIR) / project_id
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Projeto nao encontrado")
    
    status = {
        "project_id": project_id,
        "exists": True,
        "has_script": (project_dir / "script" / "script_approved.md").exists(),
        "has_scenes": (project_dir / "storyboard" / "scenes.json").exists(),
        "has_prompts": (project_dir / "prompts" / "prompts.json").exists(),
        "has_final_video": (project_dir / "final" / "commercial.mp4").exists()
    }
    
    # Load scenes if available
    scenes_path = project_dir / "prompts" / "prompts.json"
    if scenes_path.exists():
        try:
            scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
            status["scenes"] = scenes
            status["scenes_completed"] = len([s for s in scenes if s.get("status") == "completed"])
            status["scenes_total"] = len(scenes)
        except:
            pass
    
    return status


# ========== Pipeline Status ==========

@app.get("/api/pipeline/status")
async def get_pipeline_status():
    """Get status of all pipeline components."""
    try:
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        status = pipeline.get_pipeline_status()
        
        return status
    except Exception as e:
        logger.error("Erro ao obter status do pipeline: %s", str(e))
        return {"error": str(e)}


# ========== WebSocket for Progress ==========

@app.websocket("/ws/jobs/{job_id}")
async def websocket_progress(websocket: WebSocket, job_id: str):
    """WebSocket for job progress updates."""
    await websocket.accept()
    try:
        while True:
            # Placeholder for progress updates
            await websocket.send_json({"job_id": job_id, "progress": 0, "status": "pending"})
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=GRADIO_HOST, port=8000)
