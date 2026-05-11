# -*- coding: utf-8 -*-
"""Tests for SRT service (AUD-702)."""

import pytest
from pathlib import Path

from app.domain.audio_plan import AudioPlan, NarrationEntry
from app.services.srt_service import SRTService, _estimate_duration, _format_srt_timestamp


class TestEstimateDuration:
    def test_short_text_returns_minimum(self):
        assert _estimate_duration("Oi") == pytest.approx(2.0)

    def test_longer_text_scales_linearly(self):
        text = "A" * 150  # 150 chars
        expected = 150 / 15.0  # 10 seconds
        assert _estimate_duration(text) == pytest.approx(expected)

    def test_empty_string_returns_minimum(self):
        assert _estimate_duration("") == pytest.approx(2.0)

    def test_exact_boundary(self):
        text = "A" * 30  # 30 chars = 2 seconds exactly
        assert _estimate_duration(text) == pytest.approx(2.0)


class TestFormatSrtTimestamp:
    def test_zero_seconds(self):
        assert _format_srt_timestamp(0.0) == "00:00:00,000"

    def test_basic_seconds(self):
        assert _format_srt_timestamp(5.5) == "00:00:05,500"

    def test_minutes(self):
        assert _format_srt_timestamp(125.0) == "00:02:05,000"

    def test_hours(self):
        assert _format_srt_timestamp(3661.0) == "01:01:01,000"

    def test_milliseconds(self):
        assert _format_srt_timestamp(1.234) == "00:00:01,234"

    def test_fractional(self):
        assert _format_srt_timestamp(0.001) == "00:00:00,001"


class TestGenerateSrtContent:
    def test_single_scene(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_srt",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Abertura do video",
                    duration_seconds=3.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        assert "00:00:00,000 --> 00:00:03,000" in srt
        assert "Abertura do video" in srt

    def test_multiple_scenes_sequential_timing(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_seq",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="Cena 1", duration_seconds=2.0,
                ),
                NarrationEntry(
                    scene_number=2, narration_text="Cena 2", duration_seconds=3.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        assert "00:00:00,000 --> 00:00:02,000" in srt
        assert "00:00:02,000 --> 00:00:05,000" in srt

    def test_three_scenes(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_3",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="A", duration_seconds=1.0,
                ),
                NarrationEntry(
                    scene_number=2, narration_text="B", duration_seconds=1.5,
                ),
                NarrationEntry(
                    scene_number=3, narration_text="C", duration_seconds=2.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        assert "00:00:00,000 --> 00:00:01,000" in srt
        assert "00:00:01,000 --> 00:00:02,500" in srt
        assert "00:00:02,500 --> 00:00:04,500" in srt

    def test_estimated_duration_when_not_provided(self):
        service = SRTService()
        text_120_chars = "A" * 120  # 120/15 = 8 seconds
        plan = AudioPlan(
            project_id="proj_est",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text=text_120_chars,
                    duration_seconds=0.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        assert "00:00:08,000" in srt

    def test_minimum_duration_for_short_text(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_min",
            narrations=[
                NarrationEntry(
                    scene_number=1,
                    narration_text="Oi",
                    duration_seconds=0.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        # Minimo 2 segundos
        assert "00:00:02,000" in srt
        assert "--> 00:00:02,000" in srt

    def test_output_includes_sequence_numbers(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_seqnum",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="X", duration_seconds=1.0,
                ),
                NarrationEntry(
                    scene_number=2, narration_text="Y", duration_seconds=1.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        lines = [l for l in srt.split("\n") if l.strip().isdigit()]
        assert lines == ["1", "2"]

    def test_scenes_sorted_by_scene_number(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_sort",
            narrations=[
                NarrationEntry(
                    scene_number=3, narration_text="Cena 3", duration_seconds=1.0,
                ),
                NarrationEntry(
                    scene_number=1, narration_text="Cena 1", duration_seconds=1.0,
                ),
                NarrationEntry(
                    scene_number=2, narration_text="Cena 2", duration_seconds=1.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        idx_1 = srt.index("Cena 1")
        idx_2 = srt.index("Cena 2")
        idx_3 = srt.index("Cena 3")
        assert idx_1 < idx_2 < idx_3

    def test_empty_plan_returns_empty_string(self):
        service = SRTService()
        plan = AudioPlan(project_id="proj_empty")
        srt = service.generate_srt_content(plan)
        assert srt == ""

    def test_mixed_duration_sources(self):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_mix",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="Fix lasting 5s", duration_seconds=5.0,
                ),
                NarrationEntry(
                    scene_number=2, narration_text="AA", duration_seconds=0.0,
                ),
            ],
        )
        srt = service.generate_srt_content(plan)
        assert "00:00:00,000 --> 00:00:05,000" in srt
        assert "00:00:05,000 --> 00:00:07,000" in srt  # 5 + 2 (minimo)


class TestGenerateSrtFile:
    def test_writes_file(self, tmp_path):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_write",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="Teste", duration_seconds=2.0,
                ),
            ],
        )
        output = str(tmp_path / "legenda.srt")
        content = service.generate_srt_file(plan, output)
        assert Path(output).exists()
        content_read = Path(output).read_text(encoding="utf-8")
        assert content_read == content

    def test_creates_directory(self, tmp_path):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_dir",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="Teste", duration_seconds=1.0,
                ),
            ],
        )
        output = str(tmp_path / "subdir" / "nested" / "legenda.srt")
        service.generate_srt_file(plan, output)
        assert Path(output).exists()

    def test_srt_structure(self, tmp_path):
        service = SRTService()
        plan = AudioPlan(
            project_id="proj_struct",
            narrations=[
                NarrationEntry(
                    scene_number=1, narration_text="Texto", duration_seconds=2.0,
                ),
            ],
        )
        output = str(tmp_path / "out.srt")
        service.generate_srt_file(plan, output)
        content = Path(output).read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert lines[0] == "1"
        assert "-->" in lines[1]
        assert lines[2] == "Texto"
