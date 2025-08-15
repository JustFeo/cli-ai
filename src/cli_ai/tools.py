from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from duckduckgo_search import DDGS
from simpleeval import simple_eval


def calc(expression: str) -> str:
    # safe eval via simpleeval
    try:
        return str(simple_eval(expression))
    except Exception as e:
        return f"calc error: {e}"


def file_search(path: str, query: str) -> List[str]:
    results = []
    for p in Path(path).rglob("*"):
        if p.is_file() and p.suffix in {".txt", ".md", ".py", ".rst", ".json"}:
            try:
                text = p.read_text(errors="ignore")
            except Exception:
                continue
            if query.lower() in text.lower():
                results.append(str(p))
    return results


def web_search(query: str, max_results: int = 5) -> List[str]:
    with DDGS() as ddgs:
        return [r["href"] for r in ddgs.text(query, max_results=max_results)]


def execute_code(code: str, language: str = "python", timeout: int = 3) -> str:
    if language != "python":
        return "Only Python is supported in local sandbox"
    try:
        proc = subprocess.run(
            "python - <<'PY'\n" + code + "\nPY",
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return "Execution timed out"
