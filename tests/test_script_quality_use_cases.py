import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.application.use_cases.script_quality_use_cases import (
    ScoreScriptUseCase,
    GetScriptTemplateUseCase,
    EnrichBriefingUseCase,
)


class TestScoreScriptUseCase:
    def test_execute_full_score(self):
        uc = ScoreScriptUseCase()
        script = "Você já imaginou? Clique aqui e compre agora! " * 5
        result = uc.execute(script=script, project_id="proj_1")
        assert result["ok"] is True
        data = result["data"]
        assert data["score"] >= 60
        assert data["word_count"] > 10
        assert data["has_hook"] is True
        assert data["has_call_to_action"] is True

    def test_execute_short_script(self):
        uc = ScoreScriptUseCase()
        result = uc.execute(script="Hello", project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["word_count"] == 1
        assert "Aumente" in result["data"]["suggestions"][0]

    def test_execute_empty_script(self):
        uc = ScoreScriptUseCase()
        result = uc.execute(script="", project_id="proj_1")
        assert result["ok"] is False
        assert "Invalid" in result["error"]

    def test_execute_barely_minimal(self):
        uc = ScoreScriptUseCase()
        script = " ".join(["word"] * 50)
        result = uc.execute(script=script)
        assert result["ok"] is True
        assert result["data"]["word_count"] == 50

    def test_execute_no_hook_no_cta(self):
        uc = ScoreScriptUseCase()
        script = "this is a simple script without any hook or call to action words"
        result = uc.execute(script=script, project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["has_hook"] is False
        assert result["data"]["has_call_to_action"] is False
        assert result["data"]["score"] < 80

    def test_execute_exception(self):
        uc = ScoreScriptUseCase()
        result = uc.execute(script=None, project_id="proj_1")
        assert result["ok"] is False


class TestGetScriptTemplateUseCase:
    def test_get_produto(self):
        uc = GetScriptTemplateUseCase()
        result = uc.execute(commercial_type="produto")
        assert result["ok"] is True
        assert result["data"]["name"] == "Comercial de Produto"

    def test_get_servico(self):
        uc = GetScriptTemplateUseCase()
        result = uc.execute(commercial_type="servico")
        assert result["ok"] is True
        assert "solucao" in result["data"]["structure"]

    def test_get_marca(self):
        uc = GetScriptTemplateUseCase()
        result = uc.execute(commercial_type="marca")
        assert result["ok"] is True
        assert result["data"]["name"] == "Comercial de Marca"

    def test_get_invalid_type(self):
        uc = GetScriptTemplateUseCase()
        result = uc.execute(commercial_type="invalid")
        assert result["ok"] is False
        assert "Invalid commercial type" in result["error"]

    def test_get_default(self):
        uc = GetScriptTemplateUseCase()
        result = uc.execute()
        assert result["ok"] is True
        assert result["data"]["name"] == "Comercial de Produto"


class TestEnrichBriefingUseCase:
    def test_execute_short_briefing(self):
        uc = EnrichBriefingUseCase()
        result = uc.execute(briefing="Curto")
        assert result["ok"] is True
        suggestions = result["data"]["suggestions"]
        assert any("curto" in s.lower() for s in suggestions)

    def test_execute_full_briefing(self):
        uc = EnrichBriefingUseCase()
        text = "Nosso produto é incrível para o público jovem. Compre já!"
        result = uc.execute(briefing=text)
        assert result["ok"] is True
        assert "Briefing adequado" in result["data"]["suggestions"][0]

    def test_execute_empty_briefing(self):
        uc = EnrichBriefingUseCase()
        result = uc.execute(briefing="")
        assert result["ok"] is False
        assert "Invalid" in result["error"]

    def test_execute_with_project_id(self):
        uc = EnrichBriefingUseCase()
        result = uc.execute(briefing="Test briefing for produto", project_id="proj_1")
        assert result["ok"] is True
        assert result["data"]["original"] == "Test briefing for produto"
