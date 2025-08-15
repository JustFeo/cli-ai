from __future__ import annotations

import typer

from .repl import repl as start_repl

app = typer.Typer(add_completion=False)


@app.callback()
def main():
    """cli-ai: Terminal LLM Assistant"""
    # Delegate to REPL by default
    start_repl()


if __name__ == "__main__":
    app()
