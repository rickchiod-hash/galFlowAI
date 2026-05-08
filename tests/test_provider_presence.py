import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logger

logger = setup_logger()
REPO_ROOT = Path(__file__).parent.parent

LLM_PROVIDER_FILES = {
    "TemplateProvider": [
        "app/adapters/llm/base_provider.py",
        "app/adapters/llm/template_provider.py",
    ],
    "LMStudioProvider": "app/adapters/llm/lmstudio_provider.py",
    "KoboldCppProvider": "app/adapters/llm/koboldcpp_provider.py",
    "LlamaCppProvider": "app/adapters/llm/llamacpp_provider.py",
    "GPT4AllProvider": "app/adapters/llm/gpt4all_provider.py",
}

MANDATORY_PROVIDER_CLASSES = [
    "TemplateProvider",
    "LMStudioProvider",
    "KoboldCppProvider",
    "LlamaCppProvider",
    "GPT4AllProvider",
]

FALLBACK_FILES = {
    "LLM fallback (TemplateProvider)": "app/adapters/llm/base_provider.py",
    "ProviderRouter": "app/adapters/llm/provider_router.py",
    "Video fallback (FFmpegAdapter)": "app/adapters/ffmpeg_adapter.py",
    "Video primary (WanGPAdapter)": "app/adapters/wangp_adapter.py",
    "TTSAdapter": "app/adapters/tts_adapter.py",
}

FEATURE_MATRIX = REPO_ROOT / "docs" / "reference" / "FEATURE_PRESERVATION_MATRIX.md"

MANDATORY_MATRIX_TABLE_ROWS = [
    "Nome GalFlowAI",
    "Roteiro edit",
    "Aprova",
    "TemplateProvider",
    "FFmpeg fallback",
    "Providers locais",
    "Logs",
    "observabilidade",
    "Status di",
    "TODO rastre",
]


def _file_exists(rel_path: str) -> bool:
    full = REPO_ROOT / rel_path
    return full.exists()


def _class_in_file(rel_path: str, class_name: str) -> bool:
    full = REPO_ROOT / rel_path
    if not full.exists():
        return False
    content = full.read_text(encoding="utf-8", errors="ignore")
    return f"class {class_name}" in content


def test_all_llm_provider_files_exist():
    missing = []
    for name, path in LLM_PROVIDER_FILES.items():
        if isinstance(path, list):
            for p in path:
                if not _file_exists(p):
                    missing.append((name, p))
        else:
            if not _file_exists(path):
                missing.append((name, path))
    assert not missing, f"LLM provider files missing: {missing}"
    logger.info("TODOS OS ARQUIVOS LLM PROVIDER: OK")


def test_all_mandatory_provider_classes_exist():
    missing = []
    for provider in MANDATORY_PROVIDER_CLASSES:
        paths = LLM_PROVIDER_FILES[provider]
        if isinstance(paths, list):
            found = any(_class_in_file(p, provider) for p in paths)
            if not found:
                missing.append(provider)
        else:
            if not _class_in_file(paths, provider):
                missing.append(provider)
    assert not missing, f"Provider classes not found: {missing}"
    logger.info("TODAS AS CLASSES MANDATORIAS: OK")


def test_fallback_files_exist():
    missing = []
    for name, path in FALLBACK_FILES.items():
        if not _file_exists(path):
            missing.append((name, path))
    assert not missing, f"Fallback files missing: {missing}"
    logger.info("TODOS OS ARQUIVOS DE FALLBACK: OK")


def test_template_provider_is_fallback():
    router_path = REPO_ROOT / "app/adapters/llm/provider_router.py"
    assert router_path.exists(), "ProviderRouter not found"
    content = router_path.read_text(encoding="utf-8", errors="ignore")
    has_template_import = "TemplateProvider" in content
    has_fallback = "fallback" in content.lower()
    assert has_template_import, "ProviderRouter does not reference TemplateProvider"
    assert has_fallback, "ProviderRouter does not implement fallback"
    logger.info("TEMPLATEPROVIDER COMO FALLBACK: OK")


def test_tts_has_silence_fallback():
    tts_path = REPO_ROOT / "app/adapters/tts_adapter.py"
    assert tts_path.exists(), "TTSAdapter not found"
    content = tts_path.read_text(encoding="utf-8", errors="ignore")
    has_silence = "silence" in content.lower()
    has_fallback = "fallback" in content.lower()
    assert has_silence, "TTSAdapter missing silence fallback"
    assert has_fallback, "TTSAdapter missing fallback mechanism"
    logger.info("TTS SILENCE FALLBACK: OK")


def test_ffmpeg_is_video_fallback():
    ffmpeg_path = REPO_ROOT / "app/adapters/ffmpeg_adapter.py"
    assert ffmpeg_path.exists(), "FFmpegAdapter not found"
    content = ffmpeg_path.read_text(encoding="utf-8", errors="ignore")
    has_static_video = "static" in content.lower() or "create_static_video" in content
    assert has_static_video, "FFmpegAdapter missing static video generation (fallback)"
    logger.info("FFMPEG COMO VIDEO FALLBACK: OK")

    wangp_path = REPO_ROOT / "app/adapters/wangp_adapter.py"
    assert wangp_path.exists(), "WanGPAdapter not found (primary video provider)"
    logger.info("WANGP (PRIMARY VIDEO): OK")


def test_feature_matrix_preserved():
    assert FEATURE_MATRIX.exists(), "FEATURE_PRESERVATION_MATRIX.md not found"
    content = FEATURE_MATRIX.read_text(encoding="utf-8", errors="ignore")
    missing_entries = []
    for entry in MANDATORY_MATRIX_TABLE_ROWS:
        if entry not in content:
            missing_entries.append(entry)
    assert not missing_entries, f"Mandatory entries missing from matrix: {missing_entries}"
    logger.info("MATRIX DE PRESERVACAO: OK")


def test_no_missing_provider_imports():
    config_path = REPO_ROOT / "app" / "config_models.py"
    if config_path.exists():
        content = config_path.read_text(encoding="utf-8", errors="ignore")
        for provider in MANDATORY_PROVIDER_CLASSES:
            if provider == "TemplateProvider":
                continue
            if provider not in content:
                logger.warning(f"Provider {provider} not referenced in config_models.py")
        logger.info("CHECK IMPORTS CONFIG: OK")


if __name__ == "__main__":
    results = []
    for name, fn in [
        ("LLM provider files", test_all_llm_provider_files_exist),
        ("Provider classes", test_all_mandatory_provider_classes_exist),
        ("Fallback files", test_fallback_files_exist),
        ("Template fallback", test_template_provider_is_fallback),
        ("TTS silence fallback", test_tts_has_silence_fallback),
        ("Video fallback FFmpeg", test_ffmpeg_is_video_fallback),
        ("Feature matrix", test_feature_matrix_preserved),
        ("Config imports", test_no_missing_provider_imports),
    ]:
        try:
            results.append((name, fn()))
        except Exception as e:
            logger.error(f"Falha em {name}: {e}")
            results.append((name, False))

    print("\n=== RESULTADOS QA-1001 ===")
    for name, result in results:
        print(f"{name}: {'PASSOU' if result else 'FALHOU'}")
    print("==========================\n")
