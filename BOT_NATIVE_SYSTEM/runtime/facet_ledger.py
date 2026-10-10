"""Bot-local append-only event ledger; not LYVRA native memory."""
import json
import os
from pathlib import Path
from bot_runtime import validate_event

def append_event(path, event, allowed_facets):
    failures = validate_event(event)
    if event.get('facet') not in allowed_facets:
        failures.append('UNKNOWN_FACET')
    if failures:
        raise ValueError(','.join(failures))
    target = Path(path)
    if target.is_symlink():
        raise ValueError('SYMLINK_REJECTED')
    target.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
    if hasattr(os, 'O_NOFOLLOW'):
        flags |= os.O_NOFOLLOW
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, 'a', encoding='utf-8') as stream:
        stream.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())

def load_events(path, allowed_facets):
    target = Path(path)
    if target.is_symlink():
        raise ValueError('SYMLINK_REJECTED')
    if not target.exists():
        return []
    seen = set()
    entries = []
    for number, line in enumerate(target.read_text(encoding='utf-8').splitlines(), 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError('CORRUPT_EVENT_LINE_' + str(number)) from exc
        if not isinstance(event, dict) or validate_event(event) or event.get('facet') not in allowed_facets:
            raise ValueError('INVALID_EVENT_LINE_' + str(number))
        if event['event_id'] in seen:
            raise ValueError('DUPLICATE_EVENT_ID_' + str(number))
        seen.add(event['event_id'])
        entries.append(event)
    return entries
