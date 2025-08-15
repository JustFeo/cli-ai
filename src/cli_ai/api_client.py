from __future__ import annotations

from typing import Iterable, List, Optional
import os
import google.generativeai as genai
from .config import load_config


class ApiClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-pro", embedding_model: str = "text-embedding-004"):
        cfg = load_config()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or cfg.get("api_key")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not set (env) and api_key missing in ~/.config/cli-ai/config.yaml")
        genai.configure(api_key=self.api_key)
        self.model_name = model
        self.embedding_model = embedding_model
        self._model = genai.GenerativeModel(model)

    def generate(self, prompt: str, max_tokens: int = 800, temperature: float = 0.3, stream: bool = False) -> str:
        if stream:
            out = []
            for chunk in self._model.generate_content(prompt, generation_config={"max_output_tokens": max_tokens, "temperature": temperature}, stream=True):
                text = getattr(chunk, "text", None)
                if text:
                    out.append(text)
            return "".join(out)
        resp = self._model.generate_content(prompt, generation_config={"max_output_tokens": max_tokens, "temperature": temperature})
        return resp.text or ""

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = genai.embed_content(model=self.embedding_model, content=texts)
        # SDK returns {'embedding': [...]} if single; list if batch
        if isinstance(texts, list) and len(texts) == 1 and isinstance(embeddings, dict):
            return [embeddings["embedding"]]
        return embeddings["embeddings"]

    def health_check(self) -> bool:
        try:
            _ = self.embed(["ping"])
            return True
        except Exception:
            return False 