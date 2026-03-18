"""Configuration and environment variable management."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Config:
    """Application configuration loaded from environment variables."""

    token: str
    data_source_id: str

    @classmethod
    def load(cls) -> Config:
        """Load configuration from .env file and environment variables.

        Raises:
            ConfigError: If required environment variables are missing.
        """
        load_dotenv(verbose=True)

        token = os.environ.get("TOKEN", "").strip("'\"")
        data_source_id = os.environ.get("DATA_SOURCE_ID", "").strip("'\"")

        missing: list[str] = []
        if not token:
            missing.append("TOKEN")
        if not data_source_id:
            missing.append("DATA_SOURCE_ID")

        if missing:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                "Please copy .env.example to .env and fill in your Notion credentials."
            )

        return cls(token=token, data_source_id=data_source_id)
