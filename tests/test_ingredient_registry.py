"""Tests for Ingredient Registry schema (VIS-500)."""
import pytest
from app.domain.ingredient_registry import (
    Ingredient,
    IngredientRegistry,
    IngredientType,
    VisualReference,
)


class TestIngredientSchema:
    """Test Ingredient model creation and validation."""

    def test_create_minimal_ingredient(self):
        """Ingredient can be created with minimal fields."""
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante clássico")
        assert ing.name == "Coca-Cola"
        assert ing.type == IngredientType.PRODUCT
        assert ing.description == "Refrigerante clássico"
        assert ing.id.startswith("ing_")
        assert ing.version == 1
        assert len(ing.visual_references) == 0
        assert ing.metadata == {}

    def test_create_character(self):
        """Ingredient can be a character type."""
        ing = Ingredient(
            name="João Silva",
            type=IngredientType.CHARACTER,
            description="Protagonista, 30 anos"
        )
        assert ing.type == IngredientType.CHARACTER

    def test_create_scenario(self):
        """Ingredient can be a scenario type."""
        ing = Ingredient(
            name="Praia ao entardecer",
            type=IngredientType.SCENARIO,
            description="Cena de praia com pôr do sol"
        )
        assert ing.type == IngredientType.SCENARIO

    def test_create_object(self):
        """Ingredient can be an object type."""
        ing = Ingredient(
            name="Garrafa azul",
            type=IngredientType.OBJECT,
            description="Garrafa de vidro azul 500ml"
        )
        assert ing.type == IngredientType.OBJECT

    def test_create_with_visual_references(self):
        """Ingredient can have visual references."""
        ing = Ingredient(
            name="Coca-Cola",
            type=IngredientType.PRODUCT,
            description="Refrigerante clássico",
            visual_references=[
                VisualReference(file_path="/refs/coca_cola_01.jpg", description="Frente do produto"),
                VisualReference(file_path="/refs/coca_cola_02.jpg", description="Lateral do produto", is_canonical=True),
            ]
        )
        assert len(ing.visual_references) == 2
        assert ing.visual_references[0].file_path == "/refs/coca_cola_01.jpg"
        assert ing.visual_references[1].is_canonical is True

    def test_create_with_metadata(self):
        """Ingredient can have arbitrary metadata."""
        ing = Ingredient(
            name="Coca-Cola",
            type=IngredientType.PRODUCT,
            description="Refrigerante clássico",
            metadata={"brand": "Coca-Cola Company", "volume_ml": 350, "color": "#8B0000"}
        )
        assert ing.metadata["brand"] == "Coca-Cola Company"
        assert ing.metadata["volume_ml"] == 350

    def test_unique_ids(self):
        """Each ingredient gets a unique ID."""
        ing1 = Ingredient(name="Produto A", type=IngredientType.PRODUCT, description="Desc A")
        ing2 = Ingredient(name="Produto B", type=IngredientType.PRODUCT, description="Desc B")
        assert ing1.id != ing2.id

    def test_default_version(self):
        """Ingredient starts at version 1."""
        ing = Ingredient(name="Teste", type=IngredientType.PRODUCT, description="Teste")
        assert ing.version == 1


class TestIngredientRegistry:
    """Test IngredientRegistry service."""

    def test_register(self):
        """Register a new ingredient."""
        registry = IngredientRegistry()
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante")
        ing_id = registry.register(ing)
        assert ing_id == ing.id
        assert registry.count() == 1

    def test_register_empty_name_raises(self):
        """Registering with empty name raises ValueError."""
        registry = IngredientRegistry()
        ing = Ingredient(name="", type=IngredientType.PRODUCT, description="Vazio")
        with pytest.raises(ValueError, match="name cannot be empty"):
            registry.register(ing)

    def test_get_existing(self):
        """Get returns the correct ingredient."""
        registry = IngredientRegistry()
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante")
        ing_id = registry.register(ing)
        retrieved = registry.get(ing_id)
        assert retrieved is not None
        assert retrieved.name == "Coca-Cola"
        assert retrieved.id == ing_id

    def test_get_nonexistent(self):
        """Get returns None for nonexistent ingredient."""
        registry = IngredientRegistry()
        result = registry.get("nonexistent_id")
        assert result is None

    def test_update_name(self):
        """Update changes ingredient name and increments version."""
        registry = IngredientRegistry()
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante")
        ing_id = registry.register(ing)

        updated = registry.update(ing_id, name="Coca-Cola Zero")
        assert updated.name == "Coca-Cola Zero"
        assert updated.version == 2

    def test_update_description(self):
        """Update changes ingredient description."""
        registry = IngredientRegistry()
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante")
        ing_id = registry.register(ing)

        updated = registry.update(ing_id, description="Refrigerante zero açúcar")
        assert updated.description == "Refrigerante zero açúcar"

    def test_update_preserves_id(self):
        """Update cannot change ingredient ID."""
        registry = IngredientRegistry()
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante")
        ing_id = registry.register(ing)

        original_id = ing.id
        updated = registry.update(ing_id, id="new_id")
        assert updated.id == original_id  # id is protected

    def test_update_nonexistent_raises(self):
        """Updating nonexistent ingredient raises KeyError."""
        registry = IngredientRegistry()
        with pytest.raises(KeyError, match="not found"):
            registry.update("nonexistent", name="New Name")

    def test_delete_existing(self):
        """Delete removes an ingredient."""
        registry = IngredientRegistry()
        ing = Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante")
        ing_id = registry.register(ing)
        assert registry.count() == 1

        result = registry.delete(ing_id)
        assert result is True
        assert registry.count() == 0
        assert registry.get(ing_id) is None

    def test_delete_nonexistent(self):
        """Delete returns False for nonexistent ingredient."""
        registry = IngredientRegistry()
        result = registry.delete("nonexistent")
        assert result is False

    def test_list_all(self):
        """List returns all registered ingredients."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="Prod A", type=IngredientType.PRODUCT, description="A"))
        registry.register(Ingredient(name="Pers B", type=IngredientType.CHARACTER, description="B"))
        registry.register(Ingredient(name="Cen C", type=IngredientType.SCENARIO, description="C"))

        all_ingredients = registry.list()
        assert len(all_ingredients) == 3

    def test_list_by_type(self):
        """List filters by ingredient type."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="Prod A", type=IngredientType.PRODUCT, description="A"))
        registry.register(Ingredient(name="Pers B", type=IngredientType.CHARACTER, description="B"))

        products = registry.list(ingredient_type=IngredientType.PRODUCT)
        assert len(products) == 1
        assert products[0].name == "Prod A"

    def test_list_empty_by_type(self):
        """List returns empty list when no ingredients of that type."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="Prod A", type=IngredientType.PRODUCT, description="A"))

        objects = registry.list(ingredient_type=IngredientType.OBJECT)
        assert len(objects) == 0

    def test_search_by_name(self):
        """Search finds ingredients by name (case-insensitive)."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante"))
        registry.register(Ingredient(name="Pepsi", type=IngredientType.PRODUCT, description="Refrigerante"))

        results = registry.search("coca")
        assert len(results) == 1
        assert results[0].name == "Coca-Cola"

    def test_search_by_description(self):
        """Search finds ingredients by description."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante clássico"))
        registry.register(Ingredient(name="Fanta", type=IngredientType.PRODUCT, description="Refrigerante de laranja"))

        results = registry.search("clássico")
        assert len(results) == 1
        assert results[0].name == "Coca-Cola"

    def test_search_no_results(self):
        """Search returns empty list when no match."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="Coca-Cola", type=IngredientType.PRODUCT, description="Refrigerante"))

        results = registry.search("nonexistent")
        assert len(results) == 0

    def test_register_multiple_increments_count(self):
        count = 0
        registry = IngredientRegistry()
        for i in range(5):
            registry.register(
                Ingredient(name=f"Product {i}", type=IngredientType.PRODUCT, description=f"Desc {i}")
            )
            count += 1
        assert registry.count() == count

    def test_clear_removes_all(self):
        """Clear removes all ingredients."""
        registry = IngredientRegistry()
        registry.register(Ingredient(name="A", type=IngredientType.PRODUCT, description="A"))
        registry.register(Ingredient(name="B", type=IngredientType.CHARACTER, description="B"))
        assert registry.count() == 2

        registry.clear()
        assert registry.count() == 0

    def test_visual_reference_defaults(self):
        """VisualReference has correct defaults."""
        ref = VisualReference(file_path="/path/to/ref.jpg", description="Reference image")
        assert ref.file_path == "/path/to/ref.jpg"
        assert ref.description == "Reference image"
        assert ref.is_canonical is False
