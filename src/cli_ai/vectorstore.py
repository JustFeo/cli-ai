from __future__ import annotations

from typing import Any, Dict, List

import chromadb


class VectorStore:
    def __init__(self, persist_dir: str, embedding_fn):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="memories")
        self.embedding_fn = embedding_fn

    def add(self, ids: List[str], texts: List[str], metadatas: List[Dict[str, Any]]):
        self.collection.add(
            ids=ids, documents=texts, metadatas=metadatas, embeddings=self.embedding_fn(texts)
        )

    def delete(self, ids: List[str]):
        self.collection.delete(ids=ids)

    def query(self, text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(query_embeddings=self.embedding_fn([text]), n_results=top_k)
        out = []
        for i, _id in enumerate(results["ids"][0]):
            out.append(
                {
                    "id": _id,
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None,
                }
            )
        return out
