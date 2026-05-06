"""
FastAPI V2 for Gal AI - local-first internal API.
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

from app.config import GRADIO_HOST
from app.logging_config import setup_logger

logger = setup_logger()


# ========== Standardized Error/Success Envelope ==========

class ApiResponse(BaseModel):
    """Standardized API response envelope."""
    ok: bool
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[Any] = None


def success_response(data: Any = None, message: str = "Success") -> Dict:
    """Create standardized success response."""
    return {
        "ok": True,
        "code": "SUCCESS",
        "message": message,
        "details": data
    }


def error_response(code: str, message: str, details: Any = None, status_code: int = 400) -> HTTPException:
    """Create standardized error response as HTTPException."""
    return HTTPException(
        status_code=status_code,
        detail={
            "ok": False,
            "code": code,
            "message": message,
            "details": details
        }
    )

# TODO_TECNICO(API_MODULARIZACAO):
# 1) Extrair regras de negócio para app/application/use_cases (controller fino). ✅
# 2) Padronizar envelope de erro/sucesso: {ok, code, message, details}. ✅
# 3) Adicionar testes de contrato FastAPI para rotas críticas (/api/health, /api/llm/*, /api/projects/*).
# 4) Manter compatibilidade de endpoints atuais durante refatoração (sem breaking changes). ✅

# Import use cases
from app.application.use_cases.script_generation import GenerateScriptUseCase, SaveManualEditUseCase
from app.application.use_cases.project_use_cases import CreateProjectUseCase

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


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return success_response({
        "status": "ok",
        "app": "Gal AI",
        "mode": "local",
        "ui": "gradio",
        "fastapi": True,
        "version": "2.0"
    }, "Service is healthy")


# ========== LLM Providers ==========

class LLMProviderResponse(BaseModel):
    template: bool
    lmstudio: bool
    koboldcpp: bool
    gpt4all: bool
    llamacpp: bool
    openai_compatible_local: bool


@app.get("/api/llm/providers")
async def get_llm_providers():
    """Check which LLM providers are available."""
    try:
        from app.adapters.llm import ProviderRouter
        router = ProviderRouter()
        available = router.detect_available()
        # Mapear nomes de providers para o formato esperado pela UI
        return {
            "template": available.get("template", True),
            "lmstudio": available.get("LMStudioProvider", False),
            "koboldcpp": available.get("KoboldCppProvider", False),
            "gpt4all": available.get("GPT4AllProvider", False),
            "llamacpp": available.get("LlamaCppProvider", False),
            "openai_compatible_local": False  # Não implementado ainda
        }
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


@app.post("/api/llm/script")
async def generate_script_api(request: ScriptGenerateRequest):
    """Generate script using LLM providers."""
    try:
        # Use case: thin controller
        uc = GenerateScriptUseCase()
        result = uc.execute(briefing=request.briefing, project_id=request.project_id or "", provider=request.provider)
        
        if result["ok"]:
            return success_response({
                "provider_used": result["data"].get("provider_used", "Unknown"),
                "fallback_used": result["data"].get("fallback_used", False),
                "response_time_seconds": result["data"].get("response_time_seconds", 0),
                "quality_score": result["data"].get("quality_score", 0),
                "script_markdown": result["data"].get("script", ""),
                "script_json": {},
                "logs": [],
                "project_id": result.get("project_id")
            }, "Script generated successfully")
        else:
            raise error_response("SCRIPT_GENERATION_FAILED", result["error"], status_code=500)
    except Exception as e:
        logger.error("Script generation failed: %s", e)
        raise error_response("SCRIPT_GENERATION_FAILED", str(e), status_code=500)


# ========== Script Editing ==========

class ScriptSaveRequest(BaseModel):
    project_id: str
    script_markdown: str
    version_note: Optional[str] = None


@app.post("/api/projects/{project_id}/script/save-manual-edit")
async def save_manual_edit(project_id: str, request: ScriptSaveRequest):
    """Save manually edited script."""
    try:
        # Use case: thin controller
        uc = SaveManualEditUseCase()
        result = uc.execute(project_id=project_id, script_markdown=request.script_markdown, version_note=request.version_note)
        
        if result["ok"]:
            return success_response({"version": result["data"].get("version")}, "Script saved successfully")
        else:
            return error_response("SAVE_EDIT_FAILED", result["error"], status_code=500)
    except Exception as e:
        raise error_response("SAVE_EDIT_FAILED", str(e), status_code=500)


@app.post("/api/projects/{project_id}/script/improve")
async def improve_script(project_id: str, briefing: str = ""):
    """Improve existing script."""
    try:
        from app.application.use_cases.script_generation import ImproveScriptUseCase
        uc = ImproveScriptUseCase()
        result = uc.execute(project_id=project_id, briefing=briefing)
        
        if result["ok"]:
            return success_response({"script": result["data"].get("script")}, "Script improved successfully")
        else:
            return error_response("IMPROVE_FAILED", result["error"], status_code=500)
    except Exception as e:
        raise error_response("IMPROVE_FAILED", str(e), status_code=500)


@app.post("/api/projects/{project_id}/script/more-viral")
async def make_more_viral(project_id: str):
    """Make script more viral."""
    try:
        from app.services.script_service import make_more_viral
        result = make_more_viral(project_id)
        if result.get("ok"):
            return success_response({"script": result.get("script")}, "Script made more viral")
        else:
            raise error_response("VIRAL_FAILED", result.get("error", "Failed"), status_code=500)
    except Exception as e:
        raise error_response("VIRAL_FAILED", str(e), status_code=500)

@app.post("/api/projects/{project_id}/script/more-premium")
async def make_more_premium(project_id: str):
    """Make script more premium."""
    try:
        from app.services.script_service import make_more_premium
        result = make_more_premium(project_id)
        if result.get("ok"):
            return success_response({"script": result.get("script")}, "Script made more premium")
        else:
            raise error_response("PREMIUM_FAILED", result.get("error", "Failed"), status_code=500)
    except Exception as e:
        raise error_response("PREMIUM_FAILED", str(e), status_code=500)

@app.post("/api/projects/{project_id}/script/more-direct")
async def make_more_direct(project_id: str):
    """Make script more direct for sales."""
    try:
        from app.services.script_service import make_more_direct
        result = make_more_direct(project_id)
        if result.get("ok"):
            return success_response({"script": result.get("script")}, "Script made more direct")
        else:
            raise error_response("DIRECT_FAILED", result.get("error", "Failed"), status_code=500)
    except Exception as e:
        raise error_response("DIRECT_FAILED", str(e), status_code=500)

@app.post("/api/projects/{project_id}/script/new-version")
async def create_new_version(project_id: str):
    """Create new script version."""
    try:
        from app.services.script_service import create_new_version
        result = create_new_version(project_id)
        if result.get("ok"):
            return success_response({"version": result.get("version")}, "New version created")
        else:
            raise error_response("NEW_VERSION_FAILED", result.get("error", "Failed"), status_code=500)
    except Exception as e:
        raise error_response("NEW_VERSION_FAILED", str(e), status_code=500)

@app.post("/api/projects/{project_id}/script/restore-previous")
async def restore_previous_version(project_id: str):
    """Restore previous script version."""
    try:
        from app.services.script_service import restore_previous_version
        result = restore_previous_version(project_id)
        if result.get("ok"):
            return success_response({"version": result.get("version")}, "Previous version restored")
        else:
            raise error_response("RESTORE_FAILED", result.get("error", "Failed"), status_code=500)
    except Exception as e:
        raise error_response("RESTORE_FAILED", str(e), status_code=500)


@app.post("/api/projects/{project_id}/script/approve")
async def approve_script_api(project_id: str):
    """Approve script for production."""
    try:
        from app.application.use_cases.script_generation import ApproveScriptUseCase
        uc = ApproveScriptUseCase()
        result = uc.execute(project_id=project_id)
        
        if result["ok"]:
            return success_response({"script": result["data"].get("script")}, "Script approved")
        else:
            return error_response("APPROVE_FAILED", result["error"], status_code=500)
    except Exception as e:
        raise error_response("APPROVE_FAILED", str(e), status_code=500)


@app.get("/api/projects/{project_id}/script/current")
async def get_current_script(project_id: str):
    """Get current script."""
    try:
        from app.services.script_service import load_current_script
        result = load_current_script(project_id)
        return success_response({"script": result.get("script")}, "Current script loaded")
    except Exception as e:
        raise error_response("LOAD_SCRIPT_FAILED", str(e), status_code=500)


@app.get("/api/projects/{project_id}/script/versions")
async def get_script_versions(project_id: str):
    """Get all script versions."""
    try:
        from app.services.script_service import load_script_versions
        versions = load_script_versions(project_id)
        return success_response({"versions": versions}, "Script versions loaded")
    except Exception as e:
        raise error_response("LOAD_VERSIONS_FAILED", str(e), status_code=500)


# ========== Hardware ==========

@app.get("/api/hardware")
async def get_hardware_info():
    """Get hardware information."""
    try:
        from app.hardware import get_gpu_info
        return success_response(get_gpu_info(), "Hardware info retrieved")
    except Exception as e:
        logger.error("Hardware check failed: %s", e)
        return error_response("HARDWARE_CHECK_FAILED", str(e), status_code=500)


# ========== Jobs (Implemented with Use Cases) ==========

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status using use case."""
    try:
        from app.application.use_cases.job_use_cases import GetQueueStatusUseCase
        uc = GetQueueStatusUseCase()
        status = uc.execute()
        
        if status["ok"]:
            # Find specific job
            jobs = status["data"]["jobs"]
            job = next((j for j in jobs if j["job_id"] == job_id), None)
            if job:
                return success_response(job, "Job status retrieved")
            else:
                raise error_response("JOB_NOT_FOUND", "Job not found", status_code=404)
        else:
            raise error_response("QUEUE_STATUS_FAILED", status["error"], status_code=500)
    except Exception as e:
        logger.error("Job status check failed: %s", e)
        raise error_response("JOB_STATUS_FAILED", str(e), status_code=500)


@app.post("/api/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a job using use case."""
    try:
        from app.application.use_cases.job_use_cases import RemoveJobUseCase
        uc = RemoveJobUseCase()
        result = uc.execute(job_id=job_id)
        
        if result["ok"]:
            return success_response({"job_id": job_id}, "Job cancelled")
        else:
            raise error_response("CANCEL_FAILED", result["error"], status_code=500)
    except Exception as e:
        logger.error("Job cancellation failed: %s", e)
        raise error_response("CANCEL_FAILED", str(e), status_code=500)


@app.get("/api/jobs")
async def list_all_jobs():
    """List all jobs using use case."""
    try:
        from app.application.use_cases.job_use_cases import ListJobsUseCase
        uc = ListJobsUseCase()
        result = uc.execute()
        
        if result["ok"]:
            return success_response(result["data"], "Jobs listed")
        else:
            raise error_response("LIST_JOBS_FAILED", result["error"], status_code=500)
    except Exception as e:
        logger.error("Job listing failed: %s", e)
        raise error_response("LIST_JOBS_FAILED", str(e), status_code=500)


@app.post("/api/jobs")
async def create_job(request: JobCreateRequest):
    """Create new job using use case."""
    try:
        from app.application.use_cases.job_use_cases import AddJobUseCase
        uc = AddJobUseCase()
        result = uc.execute(
            project_id=request.project_id,
            job_type=request.job_type
        )
        
        if result["ok"]:
            return success_response(result["data"], "Job created")
        else:
            raise error_response("JOB_CREATE_FAILED", result["error"], status_code=500)
    except Exception as e:
        logger.error("Job creation failed: %s", e)
        raise error_response("JOB_CREATE_FAILED", str(e), status_code=500)

class JobCreateRequest(BaseModel):
    """Request model for job creation."""
    project_id: str
    job_type: str = "video_render"

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
        from app.application.use_cases.project_use_cases import CreateProjectUseCase
        from app.application.use_cases.script_generation import GenerateScriptUseCase
        from app.application.use_cases.pipeline_use_cases import SplitScenesUseCase, BuildPromptsUseCase, CreateStoryboardUseCase
        from datetime import datetime
        
        # 1. Create project (use case)
        project_name = request.product.replace(" ", "_")
        project_uc = CreateProjectUseCase()
        project_result = project_uc.execute(project_name=project_name)
        
        if not project_result["ok"]:
            return error_response("PROJECT_CREATION_FAILED", project_result["error"], status_code=500)
        
        project_id = project_result["project_id"]
        
        # 2. Generate script (use case)
        briefing = f"Comercial para {request.product}, público: {request.target_audience}, duração: {request.duration_seconds}s"
        script_uc = GenerateScriptUseCase()
        script_result = script_uc.execute(briefing=briefing, project_id=project_id)
        
        if not script_result["ok"]:
            return error_response("SCRIPT_GENERATION_FAILED", script_result["error"], status_code=500)
        
        script = script_result["data"]["script"]
        
        # 3. Split scenes (use case)
        scenes_uc = SplitScenesUseCase()
        scenes_result = scenes_uc.execute(script=script, project_id=project_id)
        
        if not scenes_result["ok"]:
            return error_response("SCENE_SPLIT_FAILED", scenes_result["error"], status_code=500)
        
        scenes = scenes_result["data"]["scenes"]
        
        # 4. Build prompts (use case)
        prompts_uc = BuildPromptsUseCase()
        prompts_result = prompts_uc.execute(scenes=scenes, style=request.style, project_id=project_id)
        
        if not prompts_result["ok"]:
            return error_response("PROMPT_BUILD_FAILED", prompts_result["error"], status_code=500)
        
        # 5. Create storyboard (use case)
        storyboard_uc = CreateStoryboardUseCase()
        storyboard_result = storyboard_uc.execute(project_id=project_id, scenes=scenes)
        
        return success_response({
            "project_id": project_id,
            "final_video": storyboard_result["data"].get("video_path") if storyboard_result["ok"] else None,
            "scenes_count": len(scenes),
            "provider_used": script_result["data"].get("provider_used")
        }, "Video generated successfully")
            
    except Exception as e:
        logger.error("Erro ao gerar video: %s", str(e))
        return error_response("VIDEO_GENERATION_ERROR", str(e), status_code=500)


@app.get("/api/video-status/{project_id}")
async def get_video_status(project_id: str):
    """Get status of video generation project."""
    from app.config import PROJECTS_DIR
    from pathlib import Path
    import json
    
    project_dir = Path(PROJECTS_DIR) / project_id
    
    if not project_dir.exists():
        raise error_response("PROJECT_NOT_FOUND", "Projeto nao encontrado", status_code=404)
    
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
        except Exception:
            pass
    
    return success_response(status, "Video status retrieved")


# ========== Pipeline Status ==========

@app.get("/api/pipeline/status")
async def get_pipeline_status():
    """Get status of all pipeline components."""
    try:
        from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
        
        pipeline = VideoGenerationPipeline()
        status = pipeline.get_pipeline_status()
        
        return success_response(status, "Pipeline status retrieved")
    except Exception as e:
        logger.error("Erro ao obter status do pipeline: %s", str(e))
        raise error_response("PIPELINE_STATUS_FAILED", str(e), status_code=500)


# ========== WebSocket for Progress ==========

@app.websocket("/ws/jobs/{job_id}")
async def websocket_progress(websocket: WebSocket, job_id: str):
    """WebSocket for real job progress updates."""
    await websocket.accept()
    try:
        import asyncio
        from app.jobs.queue import queue
        
        while True:
            job = queue.get_job(job_id)
            if job:
                # Calculate progress
                progress = 0
                if job.status == "completed":
                    progress = 100
                elif job.status == "running":
                    progress = 50
                elif job.status == "failed":
                    progress = 0
                
                await websocket.send_json({
                    "job_id": job_id,
                    "status": job.status,
                    "progress": progress,
                    "message": f"Job {job.job_type}: {job.status}",
                    "error": job.error if job.status == "failed" else None
                })
                
                if job.status in ["completed", "failed", "cancelled"]:
                    break
            else:
                await websocket.send_json({"error": "Job not found"})
                break
            
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    except Exception as e:
             try:
                 await websocket.send_json({"error": str(e)})
             except Exception:
                 pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=GRADIO_HOST, port=8000, reload=False)
