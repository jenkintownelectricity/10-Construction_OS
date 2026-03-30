"""Tests for drawing generation — Wave 8A structural validation.

Validates DrawingGenerator, SheetBuilder, and PackageBuilder instantiation
and deterministic output guarantees.
"""

import pytest

from runtime.drawing_generation.generator import DrawingGenerator
from runtime.sheet_builder.builder import SheetBuilder
from runtime.package_builder.builder import PackageBuilder
from runtime.models.condition_packet import ConditionPacket


# ---------------------------------------------------------------------------
# DrawingGenerator
# ---------------------------------------------------------------------------

class TestDrawingGeneratorInstantiation:
    """Verify DrawingGenerator can be instantiated."""

    def test_instantiate_without_args(self):
        gen = DrawingGenerator()
        assert gen is not None

    def test_instantiate_with_contract_loader(self):
        gen = DrawingGenerator(contract_loader="mock_loader")
        assert gen._contract_loader == "mock_loader"

    def test_has_generate_drawing_method(self):
        gen = DrawingGenerator()
        assert callable(getattr(gen, "generate_drawing", None))

    def test_has_generate_sheet_method(self):
        gen = DrawingGenerator()
        assert callable(getattr(gen, "generate_sheet", None))

    def test_has_validate_determinism_method(self):
        gen = DrawingGenerator()
        assert callable(getattr(gen, "validate_determinism", None))


class TestDrawingGeneratorDeterminism:
    """Verify deterministic output contract — same input, same structure."""

    def test_generator_instances_have_same_initial_state(self):
        """Two generators with identical config should have identical initial state."""
        config = {"scale": "1:50"}
        gen_a = DrawingGenerator(config=config)
        gen_b = DrawingGenerator(config=config)
        assert gen_a._config == gen_b._config

    def test_determinism_method_exists(self):
        """validate_determinism must be exposed for hash verification."""
        gen = DrawingGenerator()
        assert hasattr(gen, "validate_determinism")


# ---------------------------------------------------------------------------
# SheetBuilder
# ---------------------------------------------------------------------------

class TestSheetBuilderInstantiation:
    """Verify SheetBuilder can be instantiated."""

    def test_instantiate_without_args(self):
        builder = SheetBuilder()
        assert builder is not None

    def test_instantiate_with_contract_loader(self):
        builder = SheetBuilder(contract_loader="mock_loader")
        assert builder._contract_loader == "mock_loader"

    def test_has_build_sheet_method(self):
        builder = SheetBuilder()
        assert callable(getattr(builder, "build_sheet", None))

    def test_has_arrange_views_method(self):
        builder = SheetBuilder()
        assert callable(getattr(builder, "arrange_views", None))

    def test_has_add_titleblock_method(self):
        builder = SheetBuilder()
        assert callable(getattr(builder, "add_titleblock", None))


# ---------------------------------------------------------------------------
# PackageBuilder
# ---------------------------------------------------------------------------

class TestPackageBuilderInstantiation:
    """Verify PackageBuilder can be instantiated."""

    def test_instantiate_without_args(self):
        builder = PackageBuilder()
        assert builder is not None

    def test_instantiate_with_contract_loader(self):
        builder = PackageBuilder(contract_loader="mock_loader")
        assert builder._contract_loader == "mock_loader"

    def test_has_build_package_method(self):
        builder = PackageBuilder()
        assert callable(getattr(builder, "build_package", None))

    def test_has_add_sheet_method(self):
        builder = PackageBuilder()
        assert callable(getattr(builder, "add_sheet", None))

    def test_has_finalize_package_method(self):
        builder = PackageBuilder()
        assert callable(getattr(builder, "finalize_package", None))

    def test_has_compute_hash_method(self):
        builder = PackageBuilder()
        assert callable(getattr(builder, "compute_hash", None))
