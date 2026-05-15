from unittest.mock import patch, MagicMock

from app.core.result import Result
from app.services.script_service import (
    _condense_template,
    _build_enhanced_prompt,
    _call_template,
    generate_script_with_provider,
    get_provider_diagnostics,
    get_provider_status,
    generate_script_with_llm,
    save_manual_edit,
    create_new_version,
    restore_previous_version,
    approve_script,
    load_current_script,
    load_script_versions,
    improve_script,
    complement_script,
    make_script_more_viral,
    make_script_more_premium,
    make_script_more_direct,
    validate_script_quality,
    generate_script_fast,
    generate_script_quality as async_generate_script_quality,
)


# ========== _condense_template ==========

class TestCondenseTemplate:
    def test_condenses_scene_headers(self):
        tpl = "[Cena 1 - 10s]\nTexto: Hello\nNarracao: Test\nPrompt visual: img\n[Other]\nskip"
        result = _condense_template(tpl)
        assert "[Cena 1 - 10s]" in result
        assert "Texto: Hello" in result
        assert "Narracao: Test" in result
        assert "Prompt visual: img" in result
        assert "skip" not in result

    def test_returns_truncated_when_less_than_3_matches(self):
        result = _condense_template("short text")
        assert len(result) == 10

    def test_empty_template_returns_empty(self):
        result = _condense_template("")
        assert result == ""


# ========== _build_enhanced_prompt ==========

class TestBuildEnhancedPrompt:
    def test_includes_briefing_and_pt_br_instruction(self):
        result = _build_enhanced_prompt("briefing here", "[Cena 1]\nTexto: x\nNarracao: y\nPrompt: z")
        assert "briefing here" in result
        assert "pt-BR" in result
        assert "Estrutura de referencia" in result

    def test_condensed_template_included(self):
        result = _build_enhanced_prompt("b", "[Cena 1]\nTexto: a\nNarracao: b\nPrompt: c")
        assert "Texto: a" in result


# ========== _call_template ==========

class TestCallTemplate:
    def test_returns_dict_with_expected_keys(self):
        result = _call_template("briefing")
        assert result["ok"] is True
        assert "script" in result
        assert result["provider"] == "TemplateProvider"
        assert "quality" in result

    def test_script_is_non_empty_string(self):
        result = _call_template("test product")
        assert isinstance(result["script"], str)
        assert len(result["script"]) > 0


# ========== generate_script_with_provider ==========

class TestGenerateScriptWithProvider:
    @patch("app.services.script_service.generate_script_with_llm")
    def test_auto_delegates_to_generate_script_with_llm(self, mock_gs):
        mock_gs.return_value = {"ok": True, "script": "auto script"}
        result = generate_script_with_provider("brief", "auto")
        assert result["ok"] is True
        mock_gs.assert_called_once_with("brief", mode="auto")

    def test_unknown_provider_returns_error(self):
        result = generate_script_with_provider("brief", "nonexistent")
        assert result["ok"] is False
        assert "desconhecido" in result["error"].lower()

    @patch("app.services.script_service._call_template")
    def test_template_provider_calls_template(self, mock_ct):
        mock_ct.return_value = {"ok": True, "script": "template"}
        result = generate_script_with_provider("brief", "template")
        assert result["ok"] is True
        mock_ct.assert_called_once_with("brief")

    @patch("app.services.script_service._call_template")
    def test_provider_fallback_on_empty_result(self, mock_ct):
        mock_ct.return_value = {"ok": True, "script": "fallback script content here xyz"}
        result = generate_script_with_provider("brief", "template")
        assert result["ok"] is True

    @patch("app.services.script_service._call_template")
    def test_provider_import_error_returns_error(self, mock_ct):
        mock_ct.return_value = {"ok": True, "script": "fallback content"}
        with patch.dict("app.services.script_service._PROVIDER_CLASSES", {"badprov": ("nonexistent.module", "BadProvider")}):
            result = generate_script_with_provider("brief", "badprov")
        assert result["ok"] is False


# ========== get_provider_diagnostics ==========

class TestGetProviderDiagnostics:
    @patch("app.services.script_service.get_provider_status")
    @patch("app.services.script_service.ProviderRouter")
    def test_returns_status_and_router(self, mock_router_cls, mock_status):
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True}
        mock_router_cls.return_value = mock_router
        mock_status.return_value = {"template": True}
        result = get_provider_diagnostics()
        assert "status" in result
        assert "router_available" in result
        assert result["status"] == {"template": True}


# ========== get_provider_status ==========

class TestGetProviderStatus:
    @patch("app.services.script_service._PROVIDER_CLASSES", {"template": ("os", "path")})
    def test_returns_dict(self):
        result = get_provider_status()
        assert isinstance(result, dict)
        assert "template" in result


# ========== generate_script_with_llm ==========

class TestGenerateScriptWithLLM:
    @patch("app.services.script_service.ProviderRouter")
    def test_auto_with_available_llm_uses_safe(self, mock_router_cls):
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True, "gpt4all": True}
        mock_router.generate_script_safe.return_value = {"provider": "GPT4All", "script": "ok", "time": 0, "quality": "high"}
        mock_router_cls.return_value = mock_router

        result = generate_script_with_llm("brief", mode="auto")
        assert result["ok"] is True

    @patch("app.services.script_service.ProviderRouter")
    @patch("app.services.script_service.asyncio.get_running_loop")
    def test_auto_with_only_template_uses_fast(self, mock_loop, mock_router_cls):
        mock_loop.side_effect = RuntimeError
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True}
        mock_router.generate_script_fast = MagicMock(return_value={"provider": "TemplateProvider", "script": "ok", "time": 0, "quality": "template"})
        mock_router_cls.return_value = mock_router

        with patch("app.services.script_service.asyncio.run") as mock_run:
            mock_run.return_value = {"provider": "TemplateProvider", "script": "ok", "time": 0, "quality": "template"}
            result = generate_script_with_llm("brief", mode="auto")
            assert result["ok"] is True
            assert result["provider"] == "TemplateProvider"

    @patch("app.services.script_service.ProviderRouter")
    def test_safe_mode(self, mock_router_cls):
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True}
        mock_router.generate_script_safe.return_value = {"provider": "Safe", "script": "ok", "time": 0, "quality": "safe"}
        mock_router_cls.return_value = mock_router

        result = generate_script_with_llm("brief", mode="safe")
        assert result["ok"] is True

    @patch("app.services.script_service.ProviderRouter")
    def test_fast_mode(self, mock_router_cls):
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True, "gpt4all": True}
        mock_router.generate_script_fast = MagicMock(return_value={"provider": "Fast", "script": "fast", "time": 0, "quality": "high"})
        mock_router.generate_script_safe = MagicMock()
        mock_router_cls.return_value = mock_router

        with patch("app.services.script_service.asyncio.get_running_loop", side_effect=RuntimeError):
            with patch("app.services.script_service.asyncio.run") as mock_run:
                mock_run.return_value = {"provider": "Fast", "script": "fast", "time": 0, "quality": "high"}
                result = generate_script_with_llm("brief", mode="fast")
                assert result["ok"] is True

    @patch("app.services.script_service.ProviderRouter")
    @patch("app.services.script_service.asyncio.get_running_loop")
    def test_fast_mode_with_running_loop(self, mock_loop, mock_router_cls):
        mock_loop.return_value = "loop"
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True, "gpt4all": True}
        mock_router.generate_script_safe.return_value = {"provider": "Safe", "script": "ok", "time": 0, "quality": "safe"}
        mock_router_cls.return_value = mock_router

        result = generate_script_with_llm("brief", mode="fast")
        assert result["ok"] is True

    @patch("app.services.script_service.ProviderRouter")
    @patch("app.services.script_service.asyncio.get_running_loop")
    def test_quality_mode_with_running_loop(self, mock_loop, mock_router_cls):
        mock_loop.return_value = "loop"
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True, "gpt4all": True}
        mock_router.generate_script_safe.return_value = {"provider": "Safe", "script": "ok", "time": 0, "quality": "safe"}
        mock_router_cls.return_value = mock_router

        result = generate_script_with_llm("brief", mode="quality")
        assert result["ok"] is True

    @patch("app.services.script_service.ProviderRouter")
    @patch("app.services.script_service.asyncio.get_running_loop")
    def test_quality_mode_without_running_loop(self, mock_loop, mock_router_cls):
        mock_loop.side_effect = RuntimeError
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True, "gpt4all": True}
        mock_router.generate_script_quality = MagicMock(return_value={"provider": "Quality", "script": "ok", "time": 0, "quality": "high"})
        mock_router_cls.return_value = mock_router

        with patch("app.services.script_service.asyncio.run") as mock_run:
            mock_run.return_value = {"provider": "Quality", "script": "ok", "time": 0, "quality": "high"}
            result = generate_script_with_llm("brief", mode="quality")
            assert result["ok"] is True

    @patch("app.services.script_service.ProviderRouter")
    def test_exception_in_generation_returns_error(self, mock_router_cls):
        mock_router = MagicMock()
        mock_router.detect_available.return_value = {"template": True}
        mock_router.generate_script_safe.side_effect = Exception("generation failed")
        mock_router_cls.return_value = mock_router

        result = generate_script_with_llm("brief", mode="safe")
        assert result["ok"] is False
        assert "generation failed" in result["error"]


# ========== save_manual_edit ==========

class TestSaveManualEdit:
    @patch("app.services.script_service._get_repo")
    def test_success(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.next_version.return_value = Result.success("v001")
        mock_repo.save_version_files.return_value = Result.success({"version": "v001"})
        mock_get_repo.return_value = mock_repo

        result = save_manual_edit("p1", "# script", "manual note")
        assert result["ok"] is True
        assert result["version"] == "v001"

    @patch("app.services.script_service._get_repo")
    def test_fails_when_next_version_fails(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.next_version.return_value = Result.failure("no versions", "NO_VERSIONS")
        mock_get_repo.return_value = mock_repo

        result = save_manual_edit("p1", "# script")
        assert result["ok"] is False

    @patch("app.services.script_service._get_repo")
    def test_fails_when_save_fails(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.next_version.return_value = Result.success("v001")
        mock_repo.save_version_files.return_value = Result.failure("disk full", "SAVE_FAILED")
        mock_get_repo.return_value = mock_repo

        result = save_manual_edit("p1", "# script")
        assert result["ok"] is False

    @patch("app.services.script_service._get_repo")
    def test_exception_returns_error(self, mock_get_repo):
        mock_get_repo.side_effect = Exception("unexpected")
        result = save_manual_edit("p1", "# script")
        assert result["ok"] is False


# ========== create_new_version ==========

class TestCreateNewVersion:
    @patch("app.services.script_service._get_repo")
    def test_success(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.next_version.return_value = Result.success("v001")
        mock_repo.save_version_files.return_value = Result.success({"version": "v001"})
        mock_get_repo.return_value = mock_repo

        result = create_new_version("p1")
        assert result["ok"] is True
        assert result["version"] == "v001"

    @patch("app.services.script_service._get_repo")
    def test_fails_when_next_version_fails(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.next_version.return_value = Result.failure("err")
        mock_get_repo.return_value = mock_repo

        result = create_new_version("p1")
        assert result["ok"] is False

    @patch("app.services.script_service._get_repo")
    def test_fails_when_save_fails(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.next_version.return_value = Result.success("v001")
        mock_repo.save_version_files.return_value = Result.failure("err")
        mock_get_repo.return_value = mock_repo

        result = create_new_version("p1")
        assert result["ok"] is False

    @patch("app.services.script_service._get_repo")
    def test_exception_returns_error(self, mock_get_repo):
        mock_get_repo.side_effect = Exception("unexpected")
        result = create_new_version("p1")
        assert result["ok"] is False


# ========== restore_previous_version ==========

class TestRestorePreviousVersion:
    @patch("app.services.script_service._get_repo")
    def test_success(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.find_previous_version.return_value = Result.success({"script": "prev", "version": "v001"})
        mock_get_repo.return_value = mock_repo

        result = restore_previous_version("p1")
        assert result["ok"] is True
        assert result["script"] == "prev"

    @patch("app.services.script_service._get_repo")
    def test_no_previous_version(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.find_previous_version.return_value = Result.failure("no previous")
        mock_get_repo.return_value = mock_repo

        result = restore_previous_version("p1")
        assert result["ok"] is False

    @patch("app.services.script_service._get_repo")
    def test_exception_returns_error(self, mock_get_repo):
        mock_get_repo.side_effect = Exception("unexpected")
        result = restore_previous_version("p1")
        assert result["ok"] is False


# ========== approve_script ==========

class TestApproveScript:
    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service._get_repo")
    def test_success(self, mock_get_repo, mock_load):
        mock_load.return_value = {"ok": True, "script": "my script", "version": "v002"}
        mock_repo = MagicMock()
        mock_repo.save_approved.return_value = Result.success({"script": "my script", "status": "Approved"})
        mock_get_repo.return_value = mock_repo

        result = approve_script("p1")
        assert result["ok"] is True
        assert result["status"] == "Approved"

    @patch("app.services.script_service.load_current_script")
    def test_no_current_script(self, mock_load):
        mock_load.return_value = {"ok": False, "error": "no script"}
        result = approve_script("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service._get_repo")
    def test_save_fails(self, mock_get_repo, mock_load):
        mock_load.return_value = {"ok": True, "script": "s", "version": "v1"}
        mock_repo = MagicMock()
        mock_repo.save_approved.return_value = Result.failure("save error")
        mock_get_repo.return_value = mock_repo

        result = approve_script("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service._get_repo")
    def test_exception_returns_error(self, mock_get_repo, mock_load):
        mock_load.return_value = {"ok": True, "script": "s", "version": "v1"}
        mock_repo = MagicMock()
        mock_repo.save_approved.side_effect = Exception("unexpected")
        mock_get_repo.return_value = mock_repo

        result = approve_script("p1")
        assert result["ok"] is False


# ========== load_current_script ==========

class TestLoadCurrentScript:
    @patch("app.services.script_service._get_repo")
    def test_success(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.load_current_script.return_value = Result.success({"script": "s", "version": "v1"})
        mock_get_repo.return_value = mock_repo

        result = load_current_script("p1")
        assert result["ok"] is True
        assert result["script"] == "s"

    @patch("app.services.script_service._get_repo")
    def test_no_script(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.load_current_script.return_value = Result.failure("no script")
        mock_get_repo.return_value = mock_repo

        result = load_current_script("p1")
        assert result["ok"] is False

    @patch("app.services.script_service._get_repo")
    def test_exception_returns_error(self, mock_get_repo):
        mock_get_repo.side_effect = Exception("unexpected")
        result = load_current_script("p1")
        assert result["ok"] is False


# ========== load_script_versions ==========

class TestLoadScriptVersions:
    @patch("app.services.script_service._get_repo")
    def test_success(self, mock_get_repo):
        mock_repo = MagicMock()
        mock_repo.load_versions_summary.return_value = [{"version": "v001", "note": "first", "status": "Draft"}]
        mock_get_repo.return_value = mock_repo

        result = load_script_versions("p1")
        assert len(result) == 1
        assert result[0]["version"] == "v001"

    @patch("app.services.script_service._get_repo")
    def test_exception_returns_empty_list(self, mock_get_repo):
        mock_get_repo.side_effect = Exception("unexpected")
        result = load_script_versions("p1")
        assert result == []


# ========== improve_script ==========

class TestImproveScript:
    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_success(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "existing script"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "improved script"}

        with patch("app.pipeline.script_generator.generate_script", return_value="improved script"):
            result = improve_script("p1", "make it better")

        assert result["ok"] is True
        assert result["script"] == "improved script"

    @patch("app.services.script_service.load_current_script")
    def test_no_current_script(self, mock_load):
        mock_load.return_value = {"ok": False, "error": "no script"}
        result = improve_script("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_uses_current_script_as_fallback_briefing(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "current script text"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "improved"}

        with patch("app.pipeline.script_generator.generate_script", return_value="improved") as mock_gen:
            result = improve_script("p1")

        mock_gen.assert_called_once()
        assert result["ok"] is True

    @patch("app.services.script_service.load_current_script")
    def test_exception_returns_error(self, mock_load):
        mock_load.side_effect = Exception("unexpected")
        result = improve_script("p1")
        assert result["ok"] is False


# ========== complement_script ==========

class TestComplementScript:
    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_adds_complement_section(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "existing script"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "complemented"}

        result = complement_script("p1")
        assert result["ok"] is True
        assert "[Complemento" in result["script"]

    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_does_not_duplicate_complement(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "[Complemento]\nExisting complement"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "[Complemento]\nExisting complement"}

        result = complement_script("p1")
        assert result["ok"] is True
        assert result["script"].count("[Complemento]") == 1

    @patch("app.services.script_service.load_current_script")
    def test_no_current_script(self, mock_load):
        mock_load.return_value = {"ok": False}
        result = complement_script("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    def test_exception_returns_error(self, mock_load):
        mock_load.side_effect = Exception("unexpected")
        result = complement_script("p1")
        assert result["ok"] is False


# ========== make_script_more_viral ==========

class TestMakeScriptMoreViral:
    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_adds_hook(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "existing script"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "with hook"}

        result = make_script_more_viral("p1")
        assert result["ok"] is True
        assert "Hook" in result["script"]

    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_does_not_duplicate_hook(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "[Hook - 3s]\nExisting hook"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "[Hook - 3s]\nExisting hook"}

        result = make_script_more_viral("p1")
        assert result["ok"] is True
        assert result["script"].count("Hook") == 1

    @patch("app.services.script_service.load_current_script")
    def test_no_current_script(self, mock_load):
        mock_load.return_value = {"ok": False}
        result = make_script_more_viral("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    def test_exception_returns_error(self, mock_load):
        mock_load.side_effect = Exception("viral error")
        result = make_script_more_viral("p1")
        assert result["ok"] is False


# ========== make_script_more_premium ==========

class TestMakeScriptMorePremium:
    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_replaces_text_and_narracao(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "Texto: hello\nNarracao: world"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "Texto premium: hello\nNarracao premium: world"}

        result = make_script_more_premium("p1")
        assert result["ok"] is True
        assert "Texto premium:" in result["script"]
        assert "Narracao premium:" in result["script"]

    @patch("app.services.script_service.load_current_script")
    def test_no_current_script(self, mock_load):
        mock_load.return_value = {"ok": False}
        result = make_script_more_premium("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    def test_exception_returns_error(self, mock_load):
        mock_load.side_effect = Exception("premium error")
        result = make_script_more_premium("p1")
        assert result["ok"] is False


# ========== make_script_more_direct ==========

class TestMakeScriptMoreDirect:
    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_adds_cta(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "existing script"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "with cta"}

        result = make_script_more_direct("p1")
        assert result["ok"] is True
        assert "CTA" in result["script"]

    @patch("app.services.script_service.load_current_script")
    @patch("app.services.script_service.save_manual_edit")
    def test_does_not_duplicate_cta(self, mock_save, mock_load):
        mock_load.return_value = {"ok": True, "script": "existing script with CTA already"}
        mock_save.return_value = {"ok": True, "version": "v002", "script": "existing script with CTA already"}

        result = make_script_more_direct("p1")
        assert result["ok"] is True
        assert result["script"].count("CTA") == 1

    @patch("app.services.script_service.load_current_script")
    def test_no_current_script(self, mock_load):
        mock_load.return_value = {"ok": False}
        result = make_script_more_direct("p1")
        assert result["ok"] is False

    @patch("app.services.script_service.load_current_script")
    def test_exception_returns_error(self, mock_load):
        mock_load.side_effect = Exception("direct error")
        result = make_script_more_direct("p1")
        assert result["ok"] is False


# ========== validate_script_quality ==========

class TestValidateScriptQuality:
    def test_valid_script(self):
        script = "[Cena 1 - 10s]\nTexto: Hello\nNarracao: World\nCTA: Buy now\n" * 5
        result = validate_script_quality(script)
        assert result["valid"] is True
        assert result["score"] >= 50

    def test_too_short_script(self):
        result = validate_script_quality("short")
        assert result["valid"] is False
        assert result["score"] >= 0

    def test_empty_script(self):
        result = validate_script_quality("")
        assert result["valid"] is False

    def test_robotic_phrase_detected(self):
        long_prefix = "[Cena 1]\nCTA: agora\n" + "x" * 150
        script = long_prefix + "produto de qualidade"
        result = validate_script_quality(script)
        assert any("robotic" in issue for issue in result["issues"])

    def test_no_scenes_found(self):
        result = validate_script_quality("some text without scene markers that is more than one hundred chars long but has not scenes at all")
        assert result["valid"] is False
        assert result["score"] >= 0

    def test_no_call_to_action(self):
        script = "[Cena 1]\nTexto: Hello\nNarracao: World\n" * 5
        result = validate_script_quality(script)
        assert result["score"] <= 60

    def test_multiple_issues_accumulate(self):
        result = validate_script_quality("Apresentamos nosso produto")
        assert result["valid"] is False


# ========== Async Wrappers ==========

class TestAsyncWrappers:
    @patch("app.services.script_service.generate_script_with_llm")
    def test_generate_script_fast(self, mock_gs):
        mock_gs.return_value = {"ok": True}
        import asyncio
        result = asyncio.run(generate_script_fast("brief"))
        mock_gs.assert_called_once_with("brief", mode="fast")
        assert result["ok"] is True

    @patch("app.services.script_service.generate_script_with_llm")
    def test_generate_script_quality(self, mock_gs):
        mock_gs.return_value = {"ok": True}
        import asyncio
        result = asyncio.run(async_generate_script_quality("brief"))
        mock_gs.assert_called_once_with("brief", mode="quality")
        assert result["ok"] is True
