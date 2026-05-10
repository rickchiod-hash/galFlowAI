"""Tests for Visual Bible schema (VIS-501)."""
import pytest
from app.domain.visual_bible import (
    ApprovedReference,
    BibleEntry,
    BibleEntryStatus,
    VisualBible,
)


class TestApprovedReference:
    """Test ApprovedReference model."""

    def test_create_minimal(self):
        """ApprovedReference can be created with minimal fields."""
        ref = ApprovedReference(
            file_path="/refs/product_01.jpg",
            description="Approved product image",
        )
        assert ref.file_path == "/refs/product_01.jpg"
        assert ref.description == "Approved product image"
        assert ref.angle is None
        assert ref.lighting_notes is None
        assert ref.is_primary is False

    def test_create_full(self):
        """ApprovedReference can be created with all fields."""
        ref = ApprovedReference(
            file_path="/refs/product_01.jpg",
            description="Frente do produto",
            angle="front",
            lighting_notes="Softbox a 45 graus",
            is_primary=True,
        )
        assert ref.angle == "front"
        assert ref.lighting_notes == "Softbox a 45 graus"
        assert ref.is_primary is True

    def test_multiple_references(self):
        """Multiple references can be created."""
        refs = [
            ApprovedReference(file_path="/refs/a.jpg", description="A"),
            ApprovedReference(file_path="/refs/b.jpg", description="B"),
        ]
        assert len(refs) == 2
        assert refs[0].file_path == "/refs/a.jpg"


class TestBibleEntry:
    """Test BibleEntry model creation and validation."""

    def test_create_minimal_entry(self):
        """BibleEntry can be created with minimal fields."""
        entry = BibleEntry(
            ingredient_id="ing_abc123",
            ingredient_name="Coca-Cola",
        )
        assert entry.ingredient_id == "ing_abc123"
        assert entry.ingredient_name == "Coca-Cola"
        assert entry.status == BibleEntryStatus.DRAFT
        assert entry.id.startswith("bbl_")
        assert entry.version == 1
        assert len(entry.references) == 0
        assert entry.notes == ""

    def test_create_with_references(self):
        """BibleEntry can contain approved references."""
        entry = BibleEntry(
            ingredient_id="ing_abc123",
            ingredient_name="Coca-Cola",
            references=[
                ApprovedReference(
                    file_path="/refs/coke_front.jpg",
                    description="Frente",
                    is_primary=True,
                ),
                ApprovedReference(
                    file_path="/refs/coke_side.jpg",
                    description="Lateral",
                    angle="side",
                ),
            ],
            status=BibleEntryStatus.APPROVED,
            notes="Usar iluminação quente",
        )
        assert entry.status == BibleEntryStatus.APPROVED
        assert len(entry.references) == 2
        assert entry.references[0].is_primary is True
        assert entry.notes == "Usar iluminação quente"

    def test_approved_status(self):
        """BibleEntry can be created as APPROVED."""
        entry = BibleEntry(
            ingredient_id="ing_abc",
            ingredient_name="Test",
            status=BibleEntryStatus.APPROVED,
        )
        assert entry.status == BibleEntryStatus.APPROVED

    def test_archived_status(self):
        """BibleEntry can be created as ARCHIVED."""
        entry = BibleEntry(
            ingredient_id="ing_abc",
            ingredient_name="Test",
            status=BibleEntryStatus.ARCHIVED,
        )
        assert entry.status == BibleEntryStatus.ARCHIVED

    def test_unique_ids(self):
        """Each BibleEntry gets a unique ID."""
        e1 = BibleEntry(ingredient_id="ing_a", ingredient_name="A")
        e2 = BibleEntry(ingredient_id="ing_b", ingredient_name="B")
        assert e1.id != e2.id

    def test_default_version(self):
        """BibleEntry starts at version 1."""
        e = BibleEntry(ingredient_id="ing_a", ingredient_name="A")
        assert e.version == 1

    def test_create_with_metadata(self):
        """BibleEntry can have arbitrary metadata."""
        entry = BibleEntry(
            ingredient_id="ing_abc",
            ingredient_name="Coca-Cola",
            metadata={"approved_by": "diretor", "session": "2026-05-09"},
        )
        assert entry.metadata["approved_by"] == "diretor"
        assert entry.metadata["session"] == "2026-05-09"


class TestVisualBible:
    """Test VisualBible service."""

    def test_add_entry(self):
        """Add a new entry to the bible."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)
        assert entry_id == entry.id
        assert bible.count() == 1

    def test_add_empty_ingredient_id_raises(self):
        """Adding with empty ingredient_id raises ValueError."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="", ingredient_name="Test")
        with pytest.raises(ValueError, match="ingredient_id cannot be empty"):
            bible.add(entry)

    def test_add_empty_name_raises(self):
        """Adding with empty ingredient_name raises ValueError."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="")
        with pytest.raises(ValueError, match="ingredient_name cannot be empty"):
            bible.add(entry)

    def test_get_existing(self):
        """Get returns the correct entry."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)
        retrieved = bible.get(entry_id)
        assert retrieved is not None
        assert retrieved.ingredient_name == "Coca-Cola"
        assert retrieved.id == entry_id

    def test_get_nonexistent(self):
        """Get returns None for nonexistent entry."""
        bible = VisualBible()
        result = bible.get("nonexistent_id")
        assert result is None

    def test_get_by_ingredient(self):
        """Get entries by ingredient ID."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        bible.add(BibleEntry(ingredient_id="ing_b", ingredient_name="Pepsi"))

        entries = bible.get_by_ingredient("ing_a")
        assert len(entries) == 2

        entries_b = bible.get_by_ingredient("ing_b")
        assert len(entries_b) == 1

    def test_get_by_ingredient_nonexistent(self):
        """Returns empty list for nonexistent ingredient."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="A"))
        result = bible.get_by_ingredient("nonexistent")
        assert len(result) == 0

    def test_update_status(self):
        """Update changes entry status and increments version."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)

        updated = bible.update(entry_id, status=BibleEntryStatus.APPROVED)
        assert updated.status == BibleEntryStatus.APPROVED
        assert updated.version == 2

    def test_update_notes(self):
        """Update changes entry notes."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)

        updated = bible.update(entry_id, notes="Approved by client")
        assert updated.notes == "Approved by client"

    def test_update_preserves_id(self):
        """Update cannot change entry ID."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)

        original_id = entry.id
        updated = bible.update(entry_id, id="new_id")
        assert updated.id == original_id

    def test_update_preserves_ingredient_id(self):
        """Update cannot change ingredient_id."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)

        updated = bible.update(entry_id, ingredient_id="ing_xyz")
        assert updated.ingredient_id == "ing_abc"

    def test_update_nonexistent_raises(self):
        """Updating nonexistent entry raises KeyError."""
        bible = VisualBible()
        with pytest.raises(KeyError, match="not found"):
            bible.update("nonexistent", status=BibleEntryStatus.APPROVED)

    def test_delete_existing(self):
        """Delete removes an entry."""
        bible = VisualBible()
        entry = BibleEntry(ingredient_id="ing_abc", ingredient_name="Coca-Cola")
        entry_id = bible.add(entry)
        assert bible.count() == 1

        result = bible.delete(entry_id)
        assert result is True
        assert bible.count() == 0
        assert bible.get(entry_id) is None

    def test_delete_nonexistent(self):
        """Delete returns False for nonexistent entry."""
        bible = VisualBible()
        result = bible.delete("nonexistent")
        assert result is False

    def test_list_all(self):
        """List returns all entries."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        bible.add(BibleEntry(ingredient_id="ing_b", ingredient_name="Pepsi"))
        bible.add(BibleEntry(ingredient_id="ing_c", ingredient_name="Fanta"))

        all_entries = bible.list()
        assert len(all_entries) == 3

    def test_list_by_status(self):
        """List filters by entry status."""
        bible = VisualBible()
        e1 = BibleEntry(ingredient_id="ing_a", ingredient_name="A")
        e1.status = BibleEntryStatus.APPROVED
        bible.add(e1)

        e2 = BibleEntry(ingredient_id="ing_b", ingredient_name="B")
        e2.status = BibleEntryStatus.DRAFT
        bible.add(e2)

        approved = bible.list(status=BibleEntryStatus.APPROVED)
        assert len(approved) == 1
        assert approved[0].ingredient_name == "A"

    def test_list_empty_by_status(self):
        """List returns empty list when no entries of that status."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="A"))
        archived = bible.list(status=BibleEntryStatus.ARCHIVED)
        assert len(archived) == 0

    def test_search_by_name(self):
        """Search finds entries by ingredient name (case-insensitive)."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        bible.add(BibleEntry(ingredient_id="ing_b", ingredient_name="Pepsi"))

        results = bible.search("coca")
        assert len(results) == 1
        assert results[0].ingredient_name == "Coca-Cola"

    def test_search_by_notes(self):
        """Search finds entries by notes."""
        bible = VisualBible()
        e1 = BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola", notes="Aprovado pelo cliente")
        bible.add(e1)
        e2 = BibleEntry(ingredient_id="ing_b", ingredient_name="Pepsi", notes="Revisar iluminação")
        bible.add(e2)

        results = bible.search("cliente")
        assert len(results) == 1
        assert results[0].ingredient_name == "Coca-Cola"

    def test_search_no_results(self):
        """Search returns empty list when no match."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        results = bible.search("nonexistent")
        assert len(results) == 0

    def test_count_by_ingredient(self):
        """Count entries for a specific ingredient."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="Coca-Cola"))
        bible.add(BibleEntry(ingredient_id="ing_b", ingredient_name="Pepsi"))

        assert bible.count_by_ingredient("ing_a") == 2
        assert bible.count_by_ingredient("ing_b") == 1
        assert bible.count_by_ingredient("nonexistent") == 0

    def test_register_multiple_increments_count(self):
        """Adding multiple entries increments count."""
        bible = VisualBible()
        count = 0
        for i in range(5):
            bible.add(
                BibleEntry(ingredient_id=f"ing_{i}", ingredient_name=f"Product {i}")
            )
            count += 1
        assert bible.count() == count

    def test_clear_removes_all(self):
        """Clear removes all entries."""
        bible = VisualBible()
        bible.add(BibleEntry(ingredient_id="ing_a", ingredient_name="A"))
        bible.add(BibleEntry(ingredient_id="ing_b", ingredient_name="B"))
        assert bible.count() == 2

        bible.clear()
        assert bible.count() == 0
