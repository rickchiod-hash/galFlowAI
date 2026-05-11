"""Tests for SEC-1100: MCP secure policy."""
from pathlib import Path
import pytest


class TestMCPDocs:
    def test_mcp_readme_exists(self):
        assert Path("mcp/README_MCP_OPTIONAL.md").exists()

    def test_mcp_readme_contains_policy(self):
        content = Path("mcp/README_MCP_OPTIONAL.md").read_text(encoding="utf-8")
        assert "desabilitado por padrao" in content
        assert "ADR-002" in content

    def test_mcp_references_adr(self):
        content = Path("mcp/README_MCP_OPTIONAL.md").read_text(encoding="utf-8")
        assert "11_DECISOES_TECNICAS_ADR.md" in content


class TestADRPresence:
    def test_adr_mentions_mcp_disabled(self):
        adr = Path("docs/project-control/11_DECISOES_TECNICAS_ADR.md")
        if adr.exists():
            content = adr.read_text(encoding="utf-8")
            assert "MCP desabilitado" in content


class TestMCPNotRequired:
    def test_no_mcp_dependency_in_pyproject(self):
        pyproject = Path("pyproject.toml")
        if pyproject.exists():
            content = pyproject.read_text(encoding="utf-8")
            # MCP-related deps should NOT be required
            mcp_deps = [l for l in content.split("\n") if "mcp" in l.lower()]
            # If any found, they should be optional
            for dep in mcp_deps:
                assert "optional" in dep.lower() or "extras" in dep.lower(), f"MCP dep found but not optional: {dep}"
