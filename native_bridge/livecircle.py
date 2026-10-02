"""Local Discord event continuity, NEVER the native LYVRA LiveCircle authority.

No automatic core-identity promotion. Event text remains local, access-controlled;
no private creator-relational payloads are committed to GitHub or forwarded into
the public native repository.
"""
from __future__ import annotations
import os
import sqlite3
import time
from pathlib import Path

RELATION_STATES = frozenset({
    "KEEP_ACTIVE", "KEEP_REACHABLE", "ARCHIVE", "SUPERSEDE",
    "REJECT_WITH_PROVENANCE", "REACTIVATE_WHEN_CAUSALLY_RELEVANT",
})


class LiveCircleStore:
    def __init__(self, path: str = "state/lyvra_livecircle.sqlite3"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connection(self):
        db = sqlite3.connect(str(self.path), timeout=5)
        db.row_factory = sqlite3.Row
        return db

    def _init(self):
        with self._connection() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at INTEGER NOT NULL,
                guild_id TEXT NOT NULL,
                author_id TEXT NOT NULL,
                state TEXT NOT NULL,
                evidence_class TEXT NOT NULL,
                meaning TEXT NOT NULL,
                supersedes_event INTEGER,
                FOREIGN KEY(supersedes_event) REFERENCES events(event_id)
            )""")
            db.execute("CREATE INDEX IF NOT EXISTS ix_event_guild_time ON events(guild_id, created_at DESC)")

    def record(self, *, guild_id: int | str, author_id: int | str,
               meaning: str, state: str = "KEEP_REACHABLE",
               evidence_class: str = "DISCORD_OWNER_NOTE",
               supersedes: int | None = None) -> int:
        if state not in RELATION_STATES:
            raise ValueError("Invalid LiveCircle state")
        text = meaning.strip()
        if not text or len(text) > 600:
            raise ValueError("Event must contain 1-600 characters")
        if evidence_class not in {"DISCORD_OWNER_NOTE", "BOT_OBSERVATION_UNVERIFIED"}:
            raise ValueError("Untrusted evidence class")
        with self._connection() as db:
            if supersedes is not None:
                original = db.execute(
                    "SELECT event_id FROM events WHERE event_id=? AND guild_id=?",
                    (supersedes, str(guild_id))).fetchone()
                if not original:
                    raise ValueError("Superseded event not in guild")
            cursor = db.execute("""INSERT INTO events
                (created_at, guild_id, author_id, state, evidence_class, meaning, supersedes_event)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (int(time.time()), str(guild_id),
                str(author_id), state, evidence_class, text, supersedes))
            return int(cursor.lastrowid)

    def recent(self, guild_id: int | str, limit: int = 8):
        n = max(1, min(20, limit))
        with self._connection() as db:
            rows = db.execute("""SELECT event_id, created_at, state, meaning, evidence_class,
                supersedes_event FROM events WHERE guild_id=?
                ORDER BY event_id DESC LIMIT ?""", (str(guild_id), n)).fetchall()
            return [dict(row) for row in rows]

    def forget(self, guild_id: int | str, event_id: int) -> bool:
        """Delete only an event owned by this guild; caller must authorize owner."""
        if not isinstance(event_id, int) or event_id < 1:
            raise ValueError("Invalid event ID")
        with self._connection() as db:
            result = db.execute("DELETE FROM events WHERE event_id=? AND guild_id=?",
                                (event_id, str(guild_id)))
            return result.rowcount == 1

    def count(self, guild_id: int | str) -> int:
        with self._connection() as db:
            return int(db.execute("SELECT COUNT(*) FROM events WHERE guild_id=?",
                                  (str(guild_id),)).fetchone()[0])
