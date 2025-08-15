from __future__ import annotations

import typer
from rich.console import Console
from rich.prompt import Prompt

from .api_client import ApiClient
from .config import CONFIG_DIR, load_config
from .memory import MemoryStore

app = typer.Typer(add_completion=False)
console = Console()


def build_prompt(
    system: str, persona: str, memories: list[str], recent: list[str], user: str
) -> str:
    parts = [
        "SYSTEM:\n" + system,
        "PERSONA:\n" + persona,
    ]
    if memories:
        parts.append("MEMORIES:\n- " + "\n- ".join(memories))
    if recent:
        parts.append("RECENT:\n" + "\n".join(recent))
    parts.append("USER QUERY:\n" + user)
    parts.append("INSTRUCTIONS:\n- Be concise. Limit to 600 tokens.")
    return "\n\n".join(parts)


@app.command()
def repl(q: str = typer.Option(None, "-q", help="One-shot query")):
    cfg = load_config()
    client = ApiClient(model=cfg["model"], embedding_model=cfg["embedding_model"])
    mem = MemoryStore(str(CONFIG_DIR / "memory"), embedding_fn=lambda texts: client.embed(texts))

    if q:
        prompt = build_prompt(
            "You are a helpful terminal assistant.", "Professional tone.", [], [], q
        )
        console.print(client.generate(prompt, stream=False))
        raise typer.Exit(0)

    console.print("[bold]cli-ai REPL[/bold] — Ctrl+C to exit")
    recent: list[str] = []
    while True:
        try:
            user = Prompt.ask("cli-ai>")
        except (EOFError, KeyboardInterrupt):
            console.print("\nbye")
            break
        if not user.strip():
            continue
        # simplistic retrieval
        retrieved = [r.text for r in mem.search(user, top_k=cfg["retrieval_top_k"])]
        prompt = build_prompt(
            "You are a helpful terminal assistant.",
            "Professional tone.",
            retrieved,
            recent[-cfg["session_memory_n"] :],
            user,
        )
        resp = client.generate(prompt, stream=False)
        console.print(f"[green]AI>[/green] {resp}")
        recent.append(f"User: {user}")
        recent.append(f"Assistant: {resp}")


app = typer.Typer(callback=repl)
