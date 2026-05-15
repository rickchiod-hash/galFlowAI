import json
import shutil
from pathlib import Path

from app.repositories.script_repository import ScriptRepository
from app.config import PROJECTS_DIR


TEST_PROJECT = "test_repo_gal930"


def _clean():
    d = PROJECTS_DIR / TEST_PROJECT
    if d.exists():
        shutil.rmtree(d)


def _setup():
    _clean()
    d = PROJECTS_DIR / TEST_PROJECT
    d.mkdir(parents=True)
    (d / "script").mkdir()
    return d


class TestScriptRepositoryInit:
    def test_creates_repo_with_project_id(self):
        repo = ScriptRepository(TEST_PROJECT)
        assert repo.project_id == TEST_PROJECT
        assert str(TEST_PROJECT) in str(repo.script_dir)

    def test_script_dir_is_under_projects(self):
        repo = ScriptRepository(TEST_PROJECT)
        assert PROJECTS_DIR in repo.script_dir.parents

    def test_lazy_script_dir(self):
        repo = ScriptRepository(TEST_PROJECT)
        assert repo._script_dir is None
        _ = repo.script_dir
        assert repo._script_dir is not None


class TestScriptRepositoryVersionsList:
    def test_load_versions_returns_empty_when_no_file(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        assert repo.load_versions_list() == []

    def test_load_versions_returns_data_when_file_exists(self):
        proj_dir = _setup()
        versions = [{"version": "v001", "status": "Draft"}]
        (proj_dir / "script" / "script_versions.json").write_text(
            json.dumps(versions), encoding="utf-8"
        )
        repo = ScriptRepository(TEST_PROJECT)
        assert repo.load_versions_list() == versions

    def test_save_versions_list_creates_file(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        versions = [{"version": "v001", "status": "Draft"}]
        result = repo.save_versions_list(versions)
        assert result.ok is True
        saved = repo.load_versions_list()
        assert saved == versions

    def test_save_versions_list_failure_on_bad_path(self):
        repo = ScriptRepository(TEST_PROJECT)
        repo._script_dir = Path("Z:\\nonexistent_drive_path_gal930")
        result = repo.save_versions_list([{"v": "bad"}])
        assert result.ok is False


class TestScriptRepositoryNextVersion:
    def test_next_version_returns_v001_when_empty(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        result = repo.next_version()
        assert result.ok is True
        assert result.data == "v001"

    def test_next_version_increments(self):
        proj_dir = _setup()
        versions = [{"version": "v001"}, {"version": "v002"}]
        (proj_dir / "script" / "script_versions.json").write_text(
            json.dumps(versions), encoding="utf-8"
        )
        repo = ScriptRepository(TEST_PROJECT)
        result = repo.next_version()
        assert result.data == "v003"


class TestScriptRepositoryVersionFiles:
    def test_save_version_files_creates_md_and_json(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        result = repo.save_version_files("v001", "# Script content", note="Initial")
        assert result.ok is True
        assert result.data["version"] == "v001"

        md_file = repo.script_dir / "script_v001.md"
        assert md_file.exists()
        assert md_file.read_text(encoding="utf-8") == "# Script content"

        json_file = repo.script_dir / "script_v001.json"
        assert json_file.exists()
        meta = json.loads(json_file.read_text(encoding="utf-8"))
        assert meta["version"] == "v001"
        assert meta["note"] == "Initial"

    def test_save_version_files_updates_versions_list(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "first")
        repo.save_version_files("v002", "second")
        versions = repo.load_versions_list()
        assert len(versions) == 2
        assert versions[0]["version"] == "v001"
        assert versions[1]["version"] == "v002"

    def test_load_version_file_success(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "hello world")
        result = repo.load_version_file("v001")
        assert result.ok is True
        assert result.data == "hello world"

    def test_load_version_file_not_found(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        result = repo.load_version_file("v999")
        assert result.ok is False
        assert result.code == "VERSION_FILE_NOT_FOUND"


class TestScriptRepositoryCurrentScript:
    def test_load_current_script_returns_error_when_none(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        result = repo.load_current_script()
        assert result.ok is False
        assert result.code == "NO_SCRIPT"

    def test_load_current_script_returns_latest(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "version one")
        repo.save_version_files("v002", "version two")
        result = repo.load_current_script()
        assert result.ok is True
        assert result.data["script"] == "version two"
        assert result.data["version"] == "v002"

    def test_load_current_script_returns_approved_first(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "version one")
        repo.save_approved("approved script", "v001")
        result = repo.load_current_script()
        assert result.ok is True
        assert "approved" in result.data["script"]
        assert result.data["version"] == "approved"


class TestScriptRepositoryApproved:
    def test_save_approved_creates_files_and_updates_status(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "draft script")
        result = repo.save_approved("approved script", "v001")
        assert result.ok is True
        assert result.data["status"] == "Approved"

        approved_md = repo.script_dir / "script_approved.md"
        assert approved_md.exists()
        assert "approved script" in approved_md.read_text(encoding="utf-8")

        versions = repo.load_versions_list()
        assert versions[0]["status"] == "Approved"

    def test_load_approved_script_success(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_approved("my approved", "v001")
        result = repo.load_approved_script()
        assert result.ok is True
        assert result.data["script"] == "my approved"
        assert result.data["version"] == "approved"

    def test_load_approved_script_not_found(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        result = repo.load_approved_script()
        assert result.ok is False
        assert result.code == "NOT_APPROVED"


class TestScriptRepositoryVersionsSummary:
    def test_load_versions_summary_empty(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        assert repo.load_versions_summary() == []

    def test_load_versions_summary_returns_fields(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "content", note="first")
        repo.save_version_files("v002", "more", note="second")
        summary = repo.load_versions_summary()
        assert len(summary) == 2
        assert summary[0] == {"version": "v001", "note": "first", "status": "Draft"}
        assert summary[1] == {"version": "v002", "note": "second", "status": "Draft"}


class TestScriptRepositoryPreviousVersion:
    def test_find_previous_returns_error_when_single(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "only one")
        result = repo.find_previous_version()
        assert result.ok is False
        assert result.code == "NO_PREVIOUS_VERSION"

    def test_find_previous_returns_second_to_last(self):
        _clean()
        repo = ScriptRepository(TEST_PROJECT)
        repo.save_version_files("v001", "first")
        repo.save_version_files("v002", "second")
        result = repo.find_previous_version()
        assert result.ok is True
        assert result.data["script"] == "first"
        assert result.data["version"] == "v001"
