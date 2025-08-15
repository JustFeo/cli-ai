# cli-ai

Terminal LLM Assistant using Gemini API with long-term memory, tools, and REPL.

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
- Never embed API keys in code or git history; use env vars or `~/.config/cli-ai/config.yaml` (chmod 600).
- Code execution tool is disabled by default and must be enabled explicitly in config.

## License
MIT 