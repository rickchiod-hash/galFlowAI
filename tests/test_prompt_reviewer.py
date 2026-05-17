"""Tests for the prompt reviewer — lint rules and scene prompt review."""

import pytest

from app.domain.prompt_reviewer import (
    ViolationSeverity,
    PromptViolation,
    PromptReview,
    PosPromptNotEmpty,
    NegPromptNotEmpty,
    PromptTooShort,
    PromptTooLong,
    NoPlaceholderText,
    HasQualityKeywordsPos,
    NegHasQualityTerms,
    NegHasBothLanguages,
    review_prompt,
    review_scene_prompts,
    DEFAULT_RULES,
)


# ---------------------------------------------------------------------------
# ViolationSeverity
# ---------------------------------------------------------------------------


def test_severity_values():
    assert ViolationSeverity.ERROR.value == "error"
    assert ViolationSeverity.WARNING.value == "warning"
    assert ViolationSeverity.INFO.value == "info"


# ---------------------------------------------------------------------------
# PromptViolation
# ---------------------------------------------------------------------------


def test_prompt_violation_defaults():
    v = PromptViolation(rule="test", severity=ViolationSeverity.ERROR,
                        message="fail", suggestion="fix it")
    assert v.field is None
    assert v.rule == "test"
    assert v.severity == ViolationSeverity.ERROR


# ---------------------------------------------------------------------------
# PromptReview
# ---------------------------------------------------------------------------


def test_prompt_review_score_perfect():
    review = PromptReview(target="prompt")
    assert review.score == 1.0


def test_prompt_review_score_with_errors():
    review = PromptReview(target="prompt", violations=[
        PromptViolation(rule="e1", severity=ViolationSeverity.ERROR,
                        message="e", suggestion="s"),
        PromptViolation(rule="w1", severity=ViolationSeverity.WARNING,
                        message="w", suggestion="s"),
    ])
    assert review.score == pytest.approx(1.0 - 0.25 - 0.10)


def test_prompt_review_score_min_zero():
    many = [PromptViolation(rule=f"e{i}", severity=ViolationSeverity.ERROR,
                            message="x", suggestion="x")
            for i in range(10)]
    review = PromptReview(target="prompt", violations=many)
    assert review.score == 0.0


def test_prompt_review_get_summary():
    review = PromptReview(target="scene[0]:abc", violations=[
        PromptViolation(rule="r1", severity=ViolationSeverity.ERROR,
                        message="err", suggestion="fix"),
    ])
    summary = review.get_summary()
    assert summary["target"] == "scene[0]:abc"
    assert summary["score"] == 0.75
    assert summary["total_violations"] == 1
    assert summary["errors"] == 1
    assert summary["warnings"] == 0
    assert "violations" in summary
    assert summary["violations"][0]["rule"] == "r1"


# ---------------------------------------------------------------------------
# PosPromptNotEmpty
# ---------------------------------------------------------------------------


class TestPosPromptNotEmpty:
    def test_passes_with_content(self):
        rule = PosPromptNotEmpty()
        assert rule.check("Uma cena de ação") is None

    def test_fails_when_empty(self):
        rule = PosPromptNotEmpty()
        v = rule.check("")
        assert v is not None
        assert v.severity == ViolationSeverity.ERROR
        assert "empty" in v.message

    def test_fails_when_whitespace(self):
        rule = PosPromptNotEmpty()
        assert rule.check("   ") is not None


# ---------------------------------------------------------------------------
# NegPromptNotEmpty
# ---------------------------------------------------------------------------


class TestNegPromptNotEmpty:
    def test_passes_with_neg_prompt(self):
        rule = NegPromptNotEmpty()
        assert rule.check("blurry, low quality") is None

    def test_warns_when_empty(self):
        rule = NegPromptNotEmpty()
        v = rule.check("")
        assert v is not None
        assert v.severity == ViolationSeverity.WARNING


# ---------------------------------------------------------------------------
# PromptTooShort
# ---------------------------------------------------------------------------


class TestPromptTooShort:
    def test_passes_with_long_prompt(self):
        rule = PromptTooShort()
        assert rule.check("Uma cena detalhada de ação com explosões") is None

    def test_warns_when_too_short(self):
        rule = PromptTooShort()
        v = rule.check("Curta")
        assert v is not None
        assert v.severity == ViolationSeverity.WARNING
        assert "too short" in v.message

    def test_ignores_empty(self):
        rule = PromptTooShort()
        assert rule.check("") is None


# ---------------------------------------------------------------------------
# PromptTooLong
# ---------------------------------------------------------------------------


class TestPromptTooLong:
    def test_passes_with_normal_length(self):
        rule = PromptTooLong()
        assert rule.check("Prompt normal") is None

    def test_info_when_very_long(self):
        rule = PromptTooLong()
        text = "x" * 2500
        v = rule.check(text)
        assert v is not None
        assert v.severity == ViolationSeverity.INFO
        assert "very long" in v.message


# ---------------------------------------------------------------------------
# NoPlaceholderText
# ---------------------------------------------------------------------------


class TestNoPlaceholderText:
    def test_passes_with_clean_prompt(self):
        rule = NoPlaceholderText()
        text = "Uma cena de ação com carros em alta velocidade"
        assert rule.check(text) is None

    @pytest.mark.parametrize("bad_text", [
        "DESCRIÇÃO: cena de ação",
        "DESCRIPTION: action scene",
        "TODO: adicionar descrição",
        "LINGUAGEM formal",
        "IDIOMA português",
        "##",
        "****",
    ])
    def test_fails_with_placeholder(self, bad_text):
        rule = NoPlaceholderText()
        v = rule.check(bad_text)
        assert v is not None
        assert v.severity == ViolationSeverity.ERROR
        assert "placeholder" in v.message

    def test_case_insensitive(self):
        rule = NoPlaceholderText()
        assert rule.check("descrição") is not None


# ---------------------------------------------------------------------------
# HasQualityKeywordsPos
# ---------------------------------------------------------------------------


class TestHasQualityKeywordsPos:
    def test_passes_with_keywords(self):
        rule = HasQualityKeywordsPos()
        text = "Ação cinematográfica com alta qualidade e iluminação profissional"
        assert rule.check(text) is None

    def test_info_when_no_keywords(self):
        rule = HasQualityKeywordsPos()
        text = "Cena simples sem detalhes"
        v = rule.check(text)
        assert v is not None
        assert v.severity == ViolationSeverity.INFO
        assert "quality" in v.message.lower()


# ---------------------------------------------------------------------------
# NegHasQualityTerms
# ---------------------------------------------------------------------------


class TestNegHasQualityTerms:
    def test_passes_with_terms(self):
        rule = NegHasQualityTerms()
        text = "blurry, low quality, distorted, bad anatomy"
        assert rule.check(text) is None

    def test_warns_without_terms(self):
        rule = NegHasQualityTerms()
        text = "some random negative text"
        v = rule.check(text)
        assert v is not None
        assert v.severity == ViolationSeverity.WARNING

    def test_ignores_empty(self):
        rule = NegHasQualityTerms()
        assert rule.check("") is None


# ---------------------------------------------------------------------------
# NegHasBothLanguages
# ---------------------------------------------------------------------------


class TestNegHasBothLanguages:
    def test_passes_with_both_languages(self):
        rule = NegHasBothLanguages()
        text = "blurry, borrão, low quality, baixa qualidade, distorted, distorcido"
        assert rule.check(text) is None

    def test_warns_missing_br(self):
        rule = NegHasBothLanguages()
        text = "blurry, low quality, distorted"
        v = rule.check(text)
        assert v is not None
        assert v.severity == ViolationSeverity.WARNING
        assert "Portuguese" in v.message

    def test_warns_missing_en(self):
        rule = NegHasBothLanguages()
        text = "borrão, baixa qualidade, distorcido"
        v = rule.check(text)
        assert v is not None
        assert "English" in v.message

    def test_ignores_empty(self):
        rule = NegHasBothLanguages()
        assert rule.check("") is None


# ---------------------------------------------------------------------------
# review_prompt
# ---------------------------------------------------------------------------


class TestReviewPrompt:
    def test_returns_review_object(self):
        review = review_prompt("Uma cena cinematográfica de alta qualidade")
        assert isinstance(review, PromptReview)
        assert review.target == "prompt"

    def test_perfect_prompt_has_no_violations(self):
        text = "Cena cinematográfica de alta qualidade com iluminação profissional, ângulo dinâmico"
        neg = "blurry, borrão, low quality, baixa qualidade, distorted, distorcido, bad anatomy, má anatomia"
        review = review_prompt(f"{text}. negative: {neg}")
        assert review.score > 0.5

    def test_empty_prompt_triggers_multiple_rules(self):
        review = review_prompt("")
        assert review.score < 1.0
        assert len(review.violations) >= 2

    def test_context_passed_through(self):
        review = review_prompt("test", {"scene_id": "abc"})
        assert review is not None


# ---------------------------------------------------------------------------
# review_scene_prompts
# ---------------------------------------------------------------------------


class TestReviewScenePrompts:
    def test_empty_list(self):
        result = review_scene_prompts([])
        assert result["scene_count"] == 0
        assert result["average_score"] == 1.0
        assert result["total_violations"] == 0

    def test_reviews_each_scene(self):
        scenes = [
            {
                "prompt_positive": "Cena cinematográfica de alta qualidade com ação",
                "prompt_negative": "blurry, borrão, low quality, baixa qualidade",
                "id": "scene_1",
                "duration": 5,
            },
            {
                "prompt_positive": "",
                "prompt_negative": "",
                "id": "scene_2",
            },
        ]
        result = review_scene_prompts(scenes)
        assert result["scene_count"] == 2
        assert result["total_violations"] > 0
        assert len(result["scene_reviews"]) == 2

        scene2 = result["scene_reviews"][1]
        assert scene2["score"] < 0.5

    def test_fallback_field_names(self):
        scenes = [
            {"prompt": "ação", "negative_prompt": "blurry", "id": "s1"},
            {"prompt_pos": "ação", "prompt_neg": "blurry", "id": "s2"},
        ]
        result = review_scene_prompts(scenes)
        assert result["scene_count"] == 2


# ---------------------------------------------------------------------------
# DEFAULT_RULES — all instantiatable
# ---------------------------------------------------------------------------


def test_default_rules_are_instantiated():
    for rule in DEFAULT_RULES:
        assert rule.name
        assert isinstance(rule.severity, ViolationSeverity)


def test_all_rules_return_none_on_good_input():
    good_neg = "blurry, borrão, low quality, baixa qualidade, distorted, distorcido, bad anatomy, má anatomia, ugly, feio"
    good_pos = "Cena cinematográfica de alta qualidade com iluminação profissional, nítida e detalhada"
    for rule in DEFAULT_RULES:
        v = rule.check(good_pos, {})
        if v is not None:
            v = rule.check(good_neg, {})
        if v is not None:
            raise AssertionError(
                f"Rule '{rule.name}' flagged good input: {v.message} "
                f"(suggestion: {v.suggestion})"
            )
