"""Tests for book2notion.config module."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from book2notion.config import Config, ConfigError


class TestConfigLoad:
    """Tests for Config.load."""

    @patch.dict(os.environ, {"TOKEN": "test-token", "DATA_SOURCE_ID": "test-db"})
    def test_load_success(self) -> None:
        config = Config.load()
        assert config.token == "test-token"
        assert config.data_source_id == "test-db"

    @patch.dict(os.environ, {"TOKEN": "", "DATA_SOURCE_ID": ""}, clear=False)
    def test_missing_both_raises(self) -> None:
        with pytest.raises(ConfigError, match="TOKEN.*DATA_SOURCE_ID"):
            Config.load()

    @patch.dict(os.environ, {"TOKEN": "t", "DATA_SOURCE_ID": ""}, clear=False)
    def test_missing_data_source_id_raises(self) -> None:
        with pytest.raises(ConfigError, match="DATA_SOURCE_ID"):
            Config.load()

    @patch.dict(os.environ, {"TOKEN": "", "DATA_SOURCE_ID": "d"}, clear=False)
    def test_missing_token_raises(self) -> None:
        with pytest.raises(ConfigError, match="TOKEN"):
            Config.load()

    @patch.dict(
        os.environ, {"TOKEN": "'secret_abc'", "DATA_SOURCE_ID": '"db-123"'}, clear=False
    )
    def test_strips_surrounding_quotes(self) -> None:
        config = Config.load()
        assert config.token == "secret_abc"
        assert config.data_source_id == "db-123"
