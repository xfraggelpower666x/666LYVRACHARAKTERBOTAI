# 666SOUNDsDESIGn LYVRA CHARACTER BOT v1.7.1

**Living Baseline · Relational Calibration · Reflective Psy Module Ecology · Canonical Machine Register Integration**

Diese Version korrigiert den v1.5.0-Auditumfang: Nicht nur das neue Modulregister, sondern auch die älteren kanonischen Maschinen- und Konzeptregister werden vor Trackentwicklung geprüft und eingebunden.

## Neu

- 55 kleine spezialisierte Core-Module.
- Vollständige Integration des `CHROMATIC CARRIER MACHINE LATTICE` aus v1.4.2.
- Exakte historische Maschinen bleiben direkt ansprechbar: Human Somatic Machine, Human Frontline Core, Emotional Ball Compression, Human Brake, Memory Halo, Acid Vocabulary Machine, Cyber Collapse Machine, Signal Shield, Reservoir Pressure, Lightning Strike Ignition, Radar Trap Overspeed, Psychedelic Vocabulary Machine, Baby-LYV Afterburner, Chaos Rail, FX Orbiter, Terrain Shift und Beast Release.
- Konzeptprofile für Human Machine, Acid Machine, Humor, Fantasy, Adult/Sensual Fantasy, Surreal und Cyber Mirror.
- Neue Spezialmodule wie Humor Collision Machine, Forensic/Dictation Humor Machine, Fantasy World Machine, Adult Sensual Fantasy Machine, Erotic Shoreline Memory Machine, Surreal Narrative Machine und Cyber Mirror/Glass-Skin Machine.
- Historische Benutzerbegriffe wie `Acid Machine`, `Human Machine`, `Humor Machine`, `Fantasy Machine` und `Fantasy Adult` werden auf die passenden spezialisierten Module geroutet.
- Registry-Audit kontrolliert jetzt Core-Module, Genreprofile, Konzeptprofile, kanonische Quellregister und Aliasziele.
- Pre-Creation bleibt reflektierend und selbstergänzend, nicht starr regelgetrieben.

## Start

```bash
pip install -r requirements.txt
python scripts/selftest.py
python scripts/module_audit.py
python -u main.py
```

Adaptive Module werden in `core/generated_psychoacoustic_modules.json` gespeichert.

## v1.7.1 Causal Module Mesh

Every module now has explicit activation, increase, decrease, redirect, transform, release and exit vocabulary; chromatic carrier/polarity/spatial control; incoming/outgoing causal signals; phase behavior; bounded feedback; exit conditions; and transformed memory traces. The selected ensemble is connected before generation.

## Character Continuity Memory & Recall Engine v1.0

The bot now records character-relevant events as causal episodes rather than copying whole chats into personality. Before every model call it automatically loads a compact package in this order:

1. canonical character state;
2. active Living Baseline;
3. current relationship state;
4. recent two-day context;
5. relevant long-term character events and decisions;
6. matching emotional-causal rules;
7. open character tasks.

The engine stores the user situation, observed meaning, emotional state, activated values, LYVRA decision, later feedback, evidence class, recurrence, importance, confidence and status. One episode cannot silently rewrite identity.

### Local commands

```bash
python character_memory_cli.py status
python character_memory_cli.py event "Module became organs" "The modules create living track movement through causal interaction."
python character_memory_cli.py recall "How should I respond to Fraggel's concern?"
python character_memory_cli.py export ./character_state_export
python character_memory_cli.py snapshot ./exports/LYVRA_CHARACTER_SNAPSHOT.zip
python character_memory_cli.py restore ./exports/LYVRA_CHARACTER_SNAPSHOT.zip
```

### Discord commands

- `/character_state`
- `/character_event`
- `/character_snapshot`

### Standalone ChatGPT boundary

The persistent runtime loads SQLite automatically. A separate new ChatGPT conversation still needs the exported `LYVRA_CHARACTER_BOOTSTRAP.md` or the snapshot package to be attached/loaded; no hidden cross-chat memory is claimed.

## v1.7.1 format correction

All nonstandard handoff and bootstrap extensions were corrected to the standard `.md` Markdown format. The earlier v1.7.0 format-mistake build is superseded.
