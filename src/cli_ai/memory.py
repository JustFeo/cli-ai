from __future__ import annotations

import os
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .vectorstore import VectorStore


@dataclass
class MemoryRecord:
    id: str
    text: str
    source: str
    created_at: str
    last_used_at: str
    tags: str | None = None
    summary: str | None = None


class MemoryStore:
    def __init__(self, base_dir: str, embedding_fn):
        os.makedirs(base_dir, exist_ok=True)
        self.db_path = os.path.join(base_dir, "memories.sqlite")
        self.vs = VectorStore(os.path.join(base_dir, "vector"), embedding_fn)
        self._init_db()

    def _init_db(self) -> None:
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_used_at TEXT NOT NULL,
                tags TEXT,
                summary TEXT
            )
            """
        )
        con.commit()
        con.close()

    def add(self, text: str, source: str, tags: Optional[str] = None) -> str:
        mem_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        rec = (mem_id, text, source, now, now, tags, None)
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("INSERT INTO memories VALUES (?,?,?,?,?,?,?)", rec)
        con.commit()
        con.close()
        self.vs.add([mem_id], [text], [{"source": source, "tags": tags or ""}])
        return mem_id

    def get(self, mem_id: str) -> Optional[MemoryRecord]:
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            "SELECT id, text, source, created_at, last_used_at, tags, summary FROM memories WHERE id=?",
            (mem_id,),
        )
        row = cur.fetchone()
        con.close()
        if not row:
            return None
        return MemoryRecord(*row)

    def search(self, query: str, top_k: int = 5) -> List[MemoryRecord]:
        hits = self.vs.query(query, top_k=top_k)
        out = []
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        for h in hits:
            cur.execute(
                "SELECT id, text, source, created_at, last_used_at, tags, summary FROM memories WHERE id=?",
                (h["id"],),
            )
            row = cur.fetchone()
            if row:
                out.append(MemoryRecord(*row))
        con.close()
        return out

    def delete(self, mem_id: str) -> None:
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("DELETE FROM memories WHERE id=?", (mem_id,))
        con.commit()
        con.close()
        self.vs.delete([mem_id])
