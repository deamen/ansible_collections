"""Unit tests for manage_subuid_subgid module."""

import sys
import os

# Add the module path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "modules")
)

import manage_subuid_subgid as ms

from manage_subuid_subgid import get_next_range, user_has_entry


class DummyModule:
    def __init__(self, check_mode=False, run_commands=None):
        self.check_mode = check_mode
        self._calls = []
        # queue of (rc, stdout, stderr) tuples to return for run_command
        self._results = list(run_commands) if run_commands else []

    def run_command(self, cmd, check_rc=False):
        self._calls.append(cmd)
        if self._results:
            return self._results.pop(0)
        return (0, "", "")

    def fail_json(self, **kwargs):
        # emulate AnsibleModule.fail_json by raising an exception with the payload
        raise RuntimeError(kwargs)


class TestGetNextRange:
    """Test the get_next_range function."""

    def test_nonexistent_file(self, tmp_path):
        """Test with a file that doesn't exist."""
        filepath = tmp_path / "nonexistent"
        start, end = get_next_range(str(filepath), 65536)
        assert start == 100000
        assert end == 165535

    def test_empty_file(self, tmp_path):
        """Test with an empty file."""
        filepath = tmp_path / "empty"
        filepath.write_text("")
        start, end = get_next_range(str(filepath), 65536)
        assert start == 100000
        assert end == 165535

    def test_single_entry(self, tmp_path):
        """Test with a single existing entry."""
        filepath = tmp_path / "subuid"
        filepath.write_text("user1:100000:65536\n")
        start, end = get_next_range(str(filepath), 65536)
        assert start == 165536
        assert end == 231071

    def test_multiple_entries(self, tmp_path):
        """Test with multiple existing entries."""
        filepath = tmp_path / "subuid"
        content = """user1:100000:65536
user2:165536:65536
user3:231072:100000
"""
        filepath.write_text(content)
        start, end = get_next_range(str(filepath), 65536)
        assert start == 331072
        assert end == 396607

    def test_custom_range_size(self, tmp_path):
        """Test with a custom range size."""
        filepath = tmp_path / "subuid"
        filepath.write_text("user1:100000:65536\n")
        start, end = get_next_range(str(filepath), 100000)
        assert start == 165536
        assert end == 265535


class TestUserHasEntry:
    """Test the user_has_entry function."""

    def test_nonexistent_file(self, tmp_path):
        """Test with a file that doesn't exist."""
        filepath = tmp_path / "nonexistent"
        has_entry, info = user_has_entry(str(filepath), "testuser")
        assert has_entry is False
        assert info is None

    def test_user_not_found(self, tmp_path):
        """Test when user is not in the file."""
        filepath = tmp_path / "subuid"
        filepath.write_text("user1:100000:65536\nuser2:165536:65536\n")
        has_entry, info = user_has_entry(str(filepath), "testuser")
        assert has_entry is False
        assert info is None

    def test_user_found(self, tmp_path):
        """Test when user is found in the file."""
        filepath = tmp_path / "subuid"
        filepath.write_text(
            "user1:100000:65536\ntestuser:165536:65536\nuser2:231072:100000\n"
        )
        has_entry, info = user_has_entry(str(filepath), "testuser")
        assert has_entry is True
        assert info is not None
        assert info["start"] == 165536
        assert info["end"] == 231071

    def test_user_at_beginning(self, tmp_path):
        """Test when user entry is at the beginning."""
        filepath = tmp_path / "subuid"
        filepath.write_text("testuser:100000:65536\nuser1:165536:65536\n")
        has_entry, info = user_has_entry(str(filepath), "testuser")
        assert has_entry is True
        assert info["start"] == 100000
        assert info["end"] == 165535

    def test_partial_username_match(self, tmp_path):
        """Test that partial username matches are not detected."""
        filepath = tmp_path / "subuid"
        filepath.write_text("testuser1:100000:65536\n")
        has_entry, info = user_has_entry(str(filepath), "testuser")
        assert has_entry is False
        assert info is None


def test_basic():
    """Dummy test that always passes."""
    assert bool(1) is True


def test_noop_when_both_entries_exist(tmp_path):
    """No-op when both subuid and subgid entries already exist for user."""
    uid_file = tmp_path / "subuid"
    gid_file = tmp_path / "subgid"
    uid_file.write_text("testuser:100000:65536\n")
    gid_file.write_text("testuser:100000:65536\n")

    ms.SUBUID_FILE = str(uid_file)
    ms.SUBGID_FILE = str(gid_file)

    module = DummyModule(check_mode=False)
    res = ms.add_subuid_subgid_ranges(module, "testuser", 65536)

    assert res["changed"] is False
    assert res["subuid_range"]["start"] == 100000
    assert res["subgid_range"]["start"] == 100000
    # ensure no run_command calls were made
    assert module._calls == []


def test_adds_only_missing_subgid(tmp_path):
    """When subuid exists but subgid missing, only add subgid."""
    uid_file = tmp_path / "subuid"
    gid_file = tmp_path / "subgid"
    uid_file.write_text("testuser:200000:65536\n")
    # gid_file does not exist

    ms.SUBUID_FILE = str(uid_file)
    ms.SUBGID_FILE = str(gid_file)

    # Simulate successful usermod call for adding subgids
    module = DummyModule(check_mode=False, run_commands=[(0, "", "")])
    res = ms.add_subuid_subgid_ranges(module, "testuser", 65536)

    assert res["changed"] is True
    # one run_command call for subgid addition
    assert len(module._calls) == 1
    called = module._calls[0]
    # should call usermod --add-subgids=...
    assert any("--add-subgids=" in str(x) for x in called)
    # existing subuid preserved
    assert res["subuid_range"]["start"] == 200000


def test_check_mode_reports_change_without_run_command(tmp_path):
    """In check mode, report changed=True and do not invoke run_command."""
    uid_file = tmp_path / "subuid"
    gid_file = tmp_path / "subgid"
    # neither file exists

    ms.SUBUID_FILE = str(uid_file)
    ms.SUBGID_FILE = str(gid_file)

    module = DummyModule(check_mode=True)
    res = ms.add_subuid_subgid_ranges(module, "checkuser", 65536)

    assert res["changed"] is True
    assert "Would add" in res.get("msg", "")
    assert module._calls == []


def test_failure_returns_fail_json_on_usermod_error(tmp_path):
    """If usermod returns non-zero rc, module.fail_json is invoked with details."""
    uid_file = tmp_path / "subuid"
    gid_file = tmp_path / "subgid"
    # neither file exists -> will try to add subuid first

    ms.SUBUID_FILE = str(uid_file)
    ms.SUBGID_FILE = str(gid_file)

    # Simulate failing usermod for subuid addition
    module = DummyModule(check_mode=False, run_commands=[(2, "out", "err")])

    try:
        ms.add_subuid_subgid_ranges(module, "baduser", 65536)
        assert False, "Expected fail_json to raise"
    except RuntimeError as exc:
        payload = exc.args[0]
        assert "rc" in payload
        assert payload["rc"] == 2
        assert "stdout" in payload
        assert payload["stdout"] == "out"
        assert "stderr" in payload
        assert payload["stderr"] == "err"
