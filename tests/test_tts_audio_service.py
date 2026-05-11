# -*- coding: utf-8 -*-
"""Tests for TTSAudioService (AUD-701)."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.domain.audio_plan import AudioPlan, NarrationEntry
from app.services.tts_audio_service import TTSAudioService


class TestTTSAudioServiceInit:
    def test_create_with_adapter(self):
        adapter = MagicMock()
        service = TTSAudioService(adapter)
        assert service.tts_adapter is adapter

    def test_create_with_minimal_mock(self):
        service = TTSAudioService(MagicMock())
        assert service.tts_adapter is not None


class TestGenerateSceneAudio:
    def test_returns_list_of_results(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert isinstance(results, list)
        assert len(results) == 1

    def test_calls_adapter_per_narration(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
                NarrationEntry(scene_number=2, narration_text="Cena 2"),
                NarrationEntry(scene_number=3, narration_text="Cena 3"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert len(results) == 3
        assert adapter.generate_audio.call_count == 3

    def test_returns_scene_numbers(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=5, narration_text="Cena 5"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert results[0]["scene_number"] == 5

    def test_returns_audio_path_on_success(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert results[0]["success"] is True
        assert results[0]["audio_path"] is not None
        assert "scene_001.wav" in results[0]["audio_path"]

    def test_passes_text_to_adapter(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="Texto personalizado"
                ),
            ],
        )
        service.generate_scene_audio(plan, str(tmp_path))
        call_kwargs = adapter.generate_audio.call_args[1]
        assert call_kwargs["text"] == "Texto personalizado"

    def test_passes_voice_from_entry(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Cena 1",
                    tts_voice="brazil-pt-medium",
                ),
            ],
        )
        service.generate_scene_audio(plan, str(tmp_path))
        call_kwargs = adapter.generate_audio.call_args[1]
        assert call_kwargs["voice"] == "brazil-pt-medium"

    def test_passes_none_voice_for_default(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Cena 1",
                    tts_voice="default",
                ),
            ],
        )
        service.generate_scene_audio(plan, str(tmp_path))
        call_kwargs = adapter.generate_audio.call_args[1]
        assert call_kwargs["voice"] is None

    def test_passes_language_from_entry(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Cena 1",
                    language="en-US",
                ),
            ],
        )
        service.generate_scene_audio(plan, str(tmp_path))
        call_kwargs = adapter.generate_audio.call_args[1]
        assert call_kwargs["language"] == "en-US"

    def test_creates_output_directory(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": True, "engine": "silence"
        }
        service = TTSAudioService(adapter)
        nested_dir = tmp_path / "audio" / "scenes"
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
            ],
        )
        service.generate_scene_audio(plan, str(nested_dir))
        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_empty_plan_returns_empty_list(self, tmp_path):
        adapter = MagicMock()
        service = TTSAudioService(adapter)
        plan = AudioPlan(project_id="proj_empty")
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert results == []


class TestGenerateSceneAudioFallback:
    def test_adapter_failure_returns_false_success(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": False, "error": "TTS engine failed"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert results[0]["success"] is False
        assert results[0]["audio_path"] is None

    def test_adapter_exception_does_not_crash(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.side_effect = RuntimeError("TTS crash")
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena 1"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert len(results) == 1
        assert results[0]["success"] is False
        assert results[0]["scene_number"] == 1

    def test_mixed_success_and_failure(self, tmp_path):
        adapter = MagicMock()
        def side_effect(text, output_path, voice=None, speed=1.0, language="pt"):
            if "falha" in text:
                return {"success": False, "error": "simulated fail"}
            return {"success": True, "engine": "silence"}
        adapter.generate_audio.side_effect = side_effect
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="Cena normal"),
                NarrationEntry(scene_number=2, narration_text="Cena falha"),
                NarrationEntry(scene_number=3, narration_text="Outra normal"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert results[0]["success"] is True
        assert results[1]["success"] is False
        assert results[2]["success"] is True
        assert results[0]["audio_path"] is not None
        assert results[1]["audio_path"] is None
        assert results[2]["audio_path"] is not None

    def test_all_failures_returns_all_false(self, tmp_path):
        adapter = MagicMock()
        adapter.generate_audio.return_value = {
            "success": False, "error": "all fail"
        }
        service = TTSAudioService(adapter)
        plan = AudioPlan(
            project_id="proj_test",
            narrations=[
                NarrationEntry(scene_number=1, narration_text="A"),
                NarrationEntry(scene_number=2, narration_text="B"),
            ],
        )
        results = service.generate_scene_audio(plan, str(tmp_path))
        assert all(r["success"] is False for r in results)
        assert all(r["audio_path"] is None for r in results)


class TestGetAudioMap:
    def test_returns_dict_mapping_scene_to_path(self):
        service = TTSAudioService(MagicMock())
        results = [
            {"scene_number": 1, "audio_path": "/a/scene_001.wav", "success": True},
            {"scene_number": 2, "audio_path": "/a/scene_002.wav", "success": True},
        ]
        audio_map = service.get_audio_map(results)
        assert audio_map == {
            1: "/a/scene_001.wav",
            2: "/a/scene_002.wav",
        }

    def test_includes_none_for_failed_scenes(self):
        service = TTSAudioService(MagicMock())
        results = [
            {"scene_number": 1, "audio_path": "/a/scene_001.wav", "success": True},
            {"scene_number": 2, "audio_path": None, "success": False},
        ]
        audio_map = service.get_audio_map(results)
        assert audio_map[1] == "/a/scene_001.wav"
        assert audio_map[2] is None

    def test_empty_results_returns_empty_dict(self):
        service = TTSAudioService(MagicMock())
        audio_map = service.get_audio_map([])
        assert audio_map == {}
