"""Tests for StageLogger (OBS-900)."""
import pytest

from app.domain.stage_logger import StageEvent, StageLogger


class TestStageEvent:
    def test_default_fields(self):
        e = StageEvent(stage="test", event_type="start", message="hello")
        assert e.stage == "test"
        assert e.event_type == "start"
        assert e.message == "hello"
        assert e.cause == ""
        assert e.correction == ""
        assert e.project_id == ""

    def test_cause_and_correction(self):
        e = StageEvent(
            stage="render", event_type="failure", message="OOM",
            cause="VRAM insuficiente", correction="Reduza resolucao",
        )
        assert e.cause == "VRAM insuficiente"
        assert e.correction == "Reduza resolucao"


class TestStageLogger:
    def test_initial_state(self):
        logger = StageLogger("TestStage")
        assert logger.stage == "TestStage"
        assert logger.events == []

    def test_start_event(self):
        logger = StageLogger("TestStage")
        event = logger.start("Iniciando processo")
        assert event.event_type == "start"
        assert event.stage == "TestStage"
        assert len(logger.events) == 1

    def test_success_event(self):
        logger = StageLogger("TestStage")
        event = logger.success("Concluido com 10 cenas", duration_ms=1500.0)
        assert event.event_type == "success"
        assert event.duration_ms == 1500.0

    def test_failure_event_with_cause_correction(self):
        logger = StageLogger("RenderStage")
        event = logger.failure(
            "Falha ao renderizar",
            cause="GPU out of memory",
            correction="Use perfil GTX 1660 Super",
        )
        assert event.event_type == "failure"
        assert event.cause == "GPU out of memory"
        assert event.correction == "Use perfil GTX 1660 Super"

    def test_warning_event(self):
        logger = StageLogger("AudioStage")
        event = logger.warning(
            "TTS indisponivel",
            cause="Provider nao respondeu",
            correction="Fallback para audio vazio",
        )
        assert event.event_type == "warning"
        assert event.cause == "Provider nao respondeu"

    def test_multiple_events_accumulate(self):
        logger = StageLogger("MultiStage", project_id="proj_001")
        logger.start("Inicio")
        logger.success("Sucesso")
        logger.warning("Alerta")
        logger.failure("Falha", cause="erro")
        assert len(logger.events) == 4

    def test_project_id_propagation(self):
        logger = StageLogger("Test", project_id="proj_abc")
        event = logger.start("teste")
        assert event.project_id == "proj_abc"
        assert logger.project_id == "proj_abc"

    def test_get_summary(self):
        logger = StageLogger("SummaryStage")
        logger.start("Inicio")
        logger.success("Fim")
        logger.failure("Falhou", cause="x")
        summary = logger.get_summary()
        assert summary["stage"] == "SummaryStage"
        assert summary["total_events"] == 3
        assert summary["failures"] == 1
        assert summary["by_type"]["start"] == 1
        assert summary["by_type"]["success"] == 1
        assert summary["by_type"]["failure"] == 1

    def test_get_summary_no_failures(self):
        logger = StageLogger("CleanStage")
        logger.start("Inicio")
        logger.success("Fim")
        summary = logger.get_summary()
        assert summary["failures"] == 0
        assert summary["last_failure"] == ""

    def test_stage_immutable(self):
        logger = StageLogger("ImmutableStage")
        assert logger.stage == "ImmutableStage"
