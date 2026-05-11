"""Tests for SEC-1101: Secrets and sensitive files policy."""
from pathlib import Path

import pytest


class TestSecretsPolicyDoc:
    def test_policy_document_exists(self):
        assert Path("docs/project-control/SECRETS_POLICY.md").exists()

    def test_policy_contains_rules(self):
        content = Path("docs/project-control/SECRETS_POLICY.md").read_text(encoding="utf-8")
        assert ".env" in content
        assert "paths pessoais" in content
        assert "Nunca commitar" in content


class TestGitignoreSecurity:
    def test_gitignore_exists(self):
        assert Path(".gitignore").exists()

    def test_gitignore_has_env_entry(self):
        content = Path(".gitignore").read_text(encoding="utf-8")
        assert any(x in content for x in [".env", "*.env"]), ".gitignore should cover .env files"

    def test_gitignore_has_pyc_entry(self):
        content = Path(".gitignore").read_text(encoding="utf-8")
        assert any(x in content for x in ["*.pyc", "__pycache__"]), ".gitignore should cover pycache"

    def test_gitignore_has_credentials_entry(self):
        content = Path(".gitignore").read_text(encoding="utf-8")
        assert "credentials" in content, ".gitignore should cover credential files"


