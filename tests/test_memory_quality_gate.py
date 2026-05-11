# -*- coding: utf-8 -*-
"""Tests for MemoryQualityGate (VEC-801)."""

import pytest

from app.domain.ingredient_registry import Ingredient, IngredientType, VisualReference
from app.domain.visual_bible import BibleEntry, ApprovedReference
from app.domain.memory_quality_gate import MemoryQualityGate, QualityGateResult


class TestQualityGateResult:
    def test_approved_default(self):
        r = QualityGateResult(approved=True)
        assert r.approved is True
        assert r.errors == []
        assert r.warnings == []

    def test_with_errors(self):
        r = QualityGateResult(approved=False, errors=["err1"])
        assert r.approved is False
        assert r.errors == ["err1"]


class TestValidateIngredient:
    def test_valid_ingredient_passes(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="Produto X",
            type=IngredientType.PRODUCT,
            description="Um produto de teste com descricao longa o suficiente",
            visual_references=[
                VisualReference(file_path="ref.jpg", description="imagem"),
            ],
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is True
        assert result.errors == []

    def test_empty_name_fails(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="",
            type=IngredientType.PRODUCT,
            description="Descricao valida com mais de 10 caracteres",
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is False
        assert any("name cannot be empty" in e for e in result.errors)

    def test_short_name_fails(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="A",
            type=IngredientType.PRODUCT,
            description="Descricao valida com mais de 10 caracteres",
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is False

    def test_empty_description_fails(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="Produto",
            type=IngredientType.PRODUCT,
            description="",
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is False
        assert any("description cannot be empty" in e for e in result.errors)

    def test_short_description_warns(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="Produto",
            type=IngredientType.PRODUCT,
            description="Curto",
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is True
        assert any("short" in w for w in result.warnings)

    def test_no_visual_references_warns(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="Produto",
            type=IngredientType.PRODUCT,
            description="Descricao valida com mais de 10 caracteres",
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is True
        assert any("No visual references" in w for w in result.warnings)

    def test_valid_with_visual_references_no_warning(self):
        gate = MemoryQualityGate()
        ing = Ingredient(
            name="Produto",
            type=IngredientType.PRODUCT,
            description="Descricao longa o suficiente para passar no gate",
            visual_references=[
                VisualReference(file_path="img.jpg", description="foto"),
            ],
        )
        result = gate.validate_ingredient(ing)
        assert result.approved is True
        assert not any("No visual references" in w for w in result.warnings)


class TestValidateBibleEntry:
    def test_valid_entry_passes(self):
        gate = MemoryQualityGate()
        entry = BibleEntry(
            ingredient_id="ing_abc",
            ingredient_name="Produto X",
            references=[
                ApprovedReference(
                    file_path="ref.jpg", description="approved angle",
                ),
            ],
        )
        result = gate.validate_bible_entry(entry)
        assert result.approved is True
        assert result.errors == []

    def test_empty_ingredient_id_fails(self):
        gate = MemoryQualityGate()
        entry = BibleEntry(
            ingredient_id="",
            ingredient_name="Produto X",
        )
        result = gate.validate_bible_entry(entry)
        assert result.approved is False

    def test_empty_ingredient_name_fails(self):
        gate = MemoryQualityGate()
        entry = BibleEntry(
            ingredient_id="ing_abc",
            ingredient_name="",
        )
        result = gate.validate_bible_entry(entry)
        assert result.approved is False

    def test_no_approved_references_warns(self):
        gate = MemoryQualityGate()
        entry = BibleEntry(
            ingredient_id="ing_abc",
            ingredient_name="Produto X",
        )
        result = gate.validate_bible_entry(entry)
        assert result.approved is True
        assert any("No approved references" in w for w in result.warnings)
