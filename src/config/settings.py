from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from environment variables."""

    model_path: Path
    host: str
    port: int
    max_new_tokens: int
    temperature: float
    sandbox_timeout_sec: int

    @classmethod
    def from_env(cls) -> "Settings":
        project_root = Path(__file__).resolve().parents[1]
        default_model = project_root / "models" / "base_qwen_7b"
        return cls(
            model_path=Path(os.getenv("MODEL_PATH", str(default_model))),
            host=os.getenv("API_HOST", "127.0.0.1"),
            port=int(os.getenv("API_PORT", "8000")),
            max_new_tokens=int(os.getenv("MAX_NEW_TOKENS", "512")),
            temperature=float(os.getenv("TEMPERATURE", "0.2")),
            sandbox_timeout_sec=int(os.getenv("SANDBOX_TIMEOUT_SEC", "30")),
        )


settings = Settings.from_env()
