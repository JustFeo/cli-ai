# cli-ai

Terminal LLM Assistant using Gemini API with longterm memory, tools, and repl, created as a cli ai that knows stuff about you.

## Install (dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Export GEMINI_API_KEY in your shell (do NOT commit keys):
```bash
export GEMINI_API_KEY=...  # keep secret
```

## Usage
```bash
cli-ai                 # interactive REPL
cli-ai -q "Explain eigenvalues like I'm 12"  # one-shot
cli-ai remember "Met Anna at conference; likes ML" --tags personal,network
cli-ai mem-search "Anna conference" --top 5
cli-ai ingest ./notes
```

## Security
- Never embed API keys in code or git history (i have to say ts).
- Code execution tool is disabled by default and must be enabled.

## License
MIT standard
