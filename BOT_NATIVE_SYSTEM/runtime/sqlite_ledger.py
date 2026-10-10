"""Cross-platform transactional facet ledger for bot-local evidence.

SQLite BEGIN IMMEDIATE serializes cooperating writers. No native LYVRA
identity or private conversation storage is authorized by this module.
"""
import json
import sqlite3
from pathlib import Path
from bot_runtime import validate_event

def _check(event, facets):
    errors = validate_event(event)
    if event.get("facet") not in facets:
        errors.append("UNKNOWN_FACET")
    if errors:
        raise ValueError(",".join(errors))

def connect(path):
    file = Path(path)
    if file.is_symlink():
        raise ValueError("SYMLINK_REJECTED")
    file.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(file), timeout=10.0, isolation_level=None)
    db.execute("PRAGMA busy_timeout=10000")
    db.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, facet TEXT NOT NULL, source_sha TEXT NOT NULL, payload TEXT NOT NULL)")
    return db

def append(path, event, facets):
    _check(event, facets)
    with connect(path) as db:
        try:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO events (event_id, facet, source_sha, payload) VALUES (?, ?, ?, ?)",
                       (event["event_id"], event["facet"], event["source_sha"], json.dumps(event, sort_keys=True)))
            db.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            db.execute("ROLLBACK")
            raise ValueError("DUPLICATE_EVENT_ID") from exc
        except Exception:
            db.execute("ROLLBACK")
            raise
        finally:
            db.close()

def read(path, facets):
    file = Path(path)
    if not file.exists():
        return []
    with connect(path) as db:
        try:
            items = [json.loads(payload) for (payload,) in db.execute("SELECT payload FROM events ORDER BY rowid")]
            for item in items:
                _check(item, facets)
            return items
        finally:
            db.close()
