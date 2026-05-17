"""Prompt reviewer — lint rules for scene prompt quality validation."""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import re


class ViolationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class PromptViolation:
    rule: str
    severity: ViolationSeverity
    message: str
    suggestion: str
    field: Optional[str] = None


@dataclass
class PromptReview:
    target: str
    violations: List[PromptViolation] = field(default_factory=list)

    @property
    def score(self) -> float:
        if not self.violations:
            return 1.0
        penalties = {
            ViolationSeverity.ERROR: 0.25,
            ViolationSeverity.WARNING: 0.10,
            ViolationSeverity.INFO: 0.03,
        }
        total = sum(penalties.get(v.severity, 0) for v in self.violations)
        return max(0.0, 1.0 - total)

    def get_summary(self) -> Dict[str, Any]:
        errors = [v for v in self.violations if v.severity == ViolationSeverity.ERROR]
        warnings = [v for v in self.violations if v.severity == ViolationSeverity.WARNING]
        infos = [v for v in self.violations if v.severity == ViolationSeverity.INFO]
        return {
            "target": self.target,
            "score": self.score,
            "total_violations": len(self.violations),
            "errors": len(errors),
            "warnings": len(warnings),
            "info": len(infos),
            "violations": [
                {"rule": v.rule, "severity": v.severity.value, "message": v.message, "suggestion": v.suggestion}
                for v in self.violations
            ],
        }


PLACEHOLDER_PATTERNS = [
    r"\bDESCRIÇÃO\b", r"\bDESCRIPTION\b", r"\bTODO\b",
    r"\bLINGUAGEM\b", r"\bIDIOMA\b", r"\bLANGUAGE\b",
    r"\bINSERT\b", r"\bPLACEHOLDER\b",
    r"^#+$", r"^\*+$",
]

QUALITY_KEYWORDS_POS = [
    "high quality", "alta qualidade", "detalhado", "detalhada", "detailed",
    "4k", "hd", "well-lit", "iluminação", "sharp", "nítido", "nítida",
    "cinematic", "cinematográfico", "cinematográfica", "professional",
    "profissional",
]

QUALITY_KEYWORDS_NEG = [
    "blurry", "low quality", "distorted", "bad anatomy",
    "borrão", "baixa qualidade", "distorcido", "má anatomia",
]

NEGATIVE_TERMS_BR = ["borrão", "baixa qualidade", "estático", "má anatomia", "distorcido"]
NEGATIVE_TERMS_EN = ["blurry", "low quality", "static", "bad anatomy", "distorted", "ugly"]


class PromptRule:
    def __init__(self, name: str, severity: ViolationSeverity):
        self.name = name
        self.severity = severity

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        return None


class PosPromptNotEmpty(PromptRule):
    def __init__(self):
        super().__init__("prompt_pos_not_empty", ViolationSeverity.ERROR)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        if not prompt_text or not prompt_text.strip():
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message="Positive prompt is empty",
                suggestion="Provide a descriptive positive prompt for the scene",
                field="prompt_positive",
            )
        return None


class NegPromptNotEmpty(PromptRule):
    def __init__(self):
        super().__init__("prompt_neg_not_empty", ViolationSeverity.WARNING)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        if not prompt_text or not prompt_text.strip():
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message="Negative prompt is empty",
                suggestion="Add quality negative prompt terms: blurry, low quality, distorted, bad anatomy",
                field="prompt_negative",
            )
        return None


class PromptTooShort(PromptRule):
    MIN_LENGTH = 20

    def __init__(self):
        super().__init__("prompt_too_short", ViolationSeverity.WARNING)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        text = prompt_text.strip()
        if 0 < len(text) < self.MIN_LENGTH:
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message=f"Positive prompt is too short ({len(text)} chars, min {self.MIN_LENGTH})",
                suggestion="Add more descriptive details: scene context, visual style, lighting, camera angle",
                field="prompt_positive",
            )
        return None


class PromptTooLong(PromptRule):
    MAX_LENGTH = 2000

    def __init__(self):
        super().__init__("prompt_too_long", ViolationSeverity.INFO)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        if len(prompt_text) > self.MAX_LENGTH:
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message=f"Positive prompt is very long ({len(prompt_text)} chars, max {self.MAX_LENGTH})",
                suggestion="Consider splitting into multiple prompts or simplifying description",
                field="prompt_positive",
            )
        return None


class NoPlaceholderText(PromptRule):
    def __init__(self):
        super().__init__("no_placeholder_text", ViolationSeverity.ERROR)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, prompt_text, re.IGNORECASE):
                return PromptViolation(
                    rule=self.name, severity=self.severity,
                    message=f"Prompt contains placeholder text matching '{pattern}'",
                    suggestion="Replace placeholders with actual scene description content",
                    field="prompt_positive",
                )
        return None


class HasQualityKeywordsPos(PromptRule):
    def __init__(self):
        super().__init__("has_quality_keywords_pos", ViolationSeverity.INFO)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        text = prompt_text.lower()
        found = [kw for kw in QUALITY_KEYWORDS_POS if kw.lower() in text]
        if not found:
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message="Positive prompt lacks quality keywords (e.g., cinematic, detailed, high quality)",
                suggestion="Add quality descriptors: 'cinematic', 'high quality', 'detalhado', 'well-lit'",
                field="prompt_positive",
            )
        return None


class NegHasQualityTerms(PromptRule):
    def __init__(self):
        super().__init__("neg_has_quality_terms", ViolationSeverity.WARNING)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        if not prompt_text:
            return None
        text = prompt_text.lower()
        found = [kw for kw in QUALITY_KEYWORDS_NEG if kw.lower() in text]
        if not found:
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message="Negative prompt lacks quality terms (e.g., blurry, low quality, distorted)",
                suggestion="Add common quality negative terms: 'blurry, low quality, distorted, bad anatomy'",
                field="prompt_negative",
            )
        return None


class NegHasBothLanguages(PromptRule):
    def __init__(self):
        super().__init__("neg_has_both_languages", ViolationSeverity.WARNING)

    def check(self, prompt_text: str, context: Optional[Dict[str, Any]] = None) -> Optional[PromptViolation]:
        if not prompt_text:
            return None
        text = prompt_text.lower()
        has_br = any(term in text for term in NEGATIVE_TERMS_BR)
        has_en = any(term in text for term in NEGATIVE_TERMS_EN)
        if not (has_br and has_en):
            missing_lang = []
            if not has_br:
                missing_lang.append("Portuguese")
            if not has_en:
                missing_lang.append("English")
            return PromptViolation(
                rule=self.name, severity=self.severity,
                message=f"Negative prompt missing quality terms in {', '.join(missing_lang)}",
                suggestion=f"Add negative terms in both PT and EN: 'borrão, blurry, baixa qualidade, low quality'",
                field="prompt_negative",
            )
        return None


DEFAULT_RULES: List[PromptRule] = [
    PosPromptNotEmpty(),
    NegPromptNotEmpty(),
    PromptTooShort(),
    PromptTooLong(),
    NoPlaceholderText(),
    HasQualityKeywordsPos(),
    NegHasQualityTerms(),
    NegHasBothLanguages(),
]


def review_prompt(prompt_text: str, context: Optional[Dict[str, Any]] = None, rules: Optional[List[PromptRule]] = None) -> PromptReview:
    """Review a single prompt string against lint rules."""
    review = PromptReview(target="prompt")
    for rule in (rules or DEFAULT_RULES):
        try:
            violation = rule.check(prompt_text, context)
            if violation:
                review.violations.append(violation)
        except Exception as e:
            review.violations.append(PromptViolation(
                rule=rule.name, severity=ViolationSeverity.ERROR,
                message=f"Rule check error: {e}",
                suggestion="Internal error — check rule implementation",
            ))
    return review


def review_scene_prompts(scene_prompts: List[Dict[str, Any]], rules: Optional[List[PromptRule]] = None) -> Dict[str, Any]:
    """Review all prompts in a scene_prompts list."""
    results = []
    total_score = 0.0
    for i, scene in enumerate(scene_prompts):
        pos = scene.get("prompt_positive") or scene.get("prompt") or scene.get("prompt_pos", "")
        neg = scene.get("prompt_negative") or scene.get("negative_prompt") or scene.get("prompt_neg", "")

        context = {
            "scene_id": scene.get("scene_id") or scene.get("id"),
            "duration": scene.get("duration"),
            "style": scene.get("style"),
        }

        pos_review = review_prompt(str(pos), {**context, "field": "prompt_positive"}, rules)
        neg_review = review_prompt(str(neg), {**context, "field": "prompt_negative"}, rules)

        combined_violations = pos_review.violations + neg_review.violations
        combined_review = PromptReview(
            target=f"scene[{i}]:{context.get('scene_id', '?')}",
            violations=combined_violations,
        )
        total_score += combined_review.score
        results.append(combined_review.get_summary())

    count = len(scene_prompts)
    return {
        "scene_count": count,
        "average_score": round(total_score / count, 2) if count > 0 else 1.0,
        "total_violations": sum(r["total_violations"] for r in results),
        "scene_reviews": results,
    }
