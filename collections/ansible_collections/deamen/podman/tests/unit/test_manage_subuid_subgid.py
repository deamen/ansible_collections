"""Unit tests for manage_subuid_subgid module."""

import sys
import os

# Add the module path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "modules")
)

from manage_subuid_subgid import get_next_range, user_has_entry


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
