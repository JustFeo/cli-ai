from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Any, Dict
import yaml

CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "cli-ai"
CONFIG_PATH = CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG: Dict[str, Any] = {
    "api_key": None,
    "model": "gemini-1.5-pro",
    "embedding_model": "text-embedding-004",
    "session_memory_n": 12,
    "retrieval_top_k": 4,
    "similarity_threshold": 0.3,
    "allow_execute_code": False,
}


def ensure_secure(path: Path) -> None:
    if path.exists():
        mode = path.stat().st_mode
        # chmod 600 equivalent
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def load_config() -> Dict[str, Any]:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(yaml.safe_dump(DEFAULT_CONFIG, sort_keys=True))
        ensure_secure(CONFIG_PATH)
        return DEFAULT_CONFIG.copy()
    ensure_secure(CONFIG_PATH)
    data = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(data)
    return cfg 