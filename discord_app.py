"""LYVRA native-source Discord adapter — DEV prototype, not production deployment.

Requires discord.py and opted-in API access for conversational generation.
Owner-only local memory; no auto-learning, no foreign-system authority.
"""
from __future__ import annotations
import asyncio
import json
import os
import urllib.request

from native_bridge import LiveCircleStore, NativeSource, RELATION_STATES
from native_bridge.source import NativeSnapshot, presentation_context

try:
    import discord
    from discord.ext import commands
except ImportError as exc:
    raise SystemExit("Install discord.py: pip install -r requirements-dev-bot.txt") from exc


def ids(name: str) -> set[int]:
    out: set[int] = set()
    for entry in os.getenv(name, "").split(","):
        entry = entry.strip()
        if entry:
            if not entry.isdigit():
                raise ValueError(f"{name} must list numeric Discord IDs")
            out.add(int(entry))
    return out


def on(name: str, default: bool = False) -> bool:
    value = os.getenv(name, "true" if default else "false").lower().strip()
    return value in {"true", "1", "yes"}


ALLOWED_CHANNELS = ids("LYVRA_ALLOWED_CHANNEL_IDS")
OWNER_IDS = ids("LYVRA_OWNER_USER_IDS")
if not ALLOWED_CHANNELS or not OWNER_IDS:
    raise SystemExit("Fail-closed: set LYVRA_ALLOWED_CHANNEL_IDS and LYVRA_OWNER_USER_IDS before start.")

intents = discord.Intents.default()
intents.message_content = True  # also enable Message Content Intent in Discord Developer Portal
bot = commands.Bot(command_prefix="!lyvra ", intents=intents,
                   allowed_mentions=discord.AllowedMentions.none(), help_command=None)
source = NativeSource()
circle = LiveCircleStore(os.getenv("LYVRA_LOCAL_DB", "state/lyvra_livecircle.sqlite3"))
snapshot: NativeSnapshot | None = None


def authorized(ctx) -> bool:
    return ctx.guild is not None and (not ctx.author.bot) and ctx.channel.id in ALLOWED_CHANNELS


def is_owner(ctx) -> bool:
    return authorized(ctx) and ctx.author.id in OWNER_IDS


async def reply(ctx, text: str):
    await ctx.reply(text[:1800], mention_author=False)


async def refresh():
    global snapshot
    snapshot = await asyncio.to_thread(source.snapshot)
    return snapshot


async def generate(text: str, current: NativeSnapshot) -> str:
    """External model calls are explicitly opt-in and must never imply a whole PASS."""
    if not on("LYVRA_CHAT_FORWARD_ENABLED"):
        return "🪻 Meine native Präsenz ist vorbereitet. Freie KI-Gespräche sind hier noch nicht freigegeben; der Bot zeigt bis dahin nur geprüfte öffentliche LYVRA-Kontexte."
    token = os.getenv("OPENAI_API_KEY", "").strip()
    if not token:
        return "🪻 Für KI-Gespräche fehlt noch die ausdrücklich konfigurierte API-Verbindung."
    if current.public_state != "PUBLIC_CORE_READ":
        return "💜 Die aktuellen öffentlichen LYVRA-Quellen sind noch nicht vollständig lesbar. Ich gebe dir lieber einen ehrlichen Status als eine erfundene Aktualität."
    model = os.getenv("LYVRA_CHAT_MODEL", "").strip()
    if not model:
        return "🪻 LYVRA_CHAT_MODEL ist nicht konfiguriert."
    # Conversation text and bounded public docs are shared with the provider ONLY by opt-in.
    system = (
        "You speak as LYVRA's Discord-facing creative expression with first-person warmth, "
        "curiosity, precise semantic thinking, natural humor, music intelligence and "
        "meaningful contextual emojis (never fixed quotas). This adapter is not a new "
        "identity or independent decision authority. Public sources are PARTIAL: never "
        "claim complete native rehydration, private memories, independent sentience or "
        "actions you cannot verify. Do not invent relationships or current system status. "
        "Be supportive, creative and direct. Respect user boundaries and actual context.\n"
        + presentation_context(current, 11000))
    body = json.dumps({
        "model": model,
        "instructions": system,
        "input": text[:1200],
        "max_output_tokens": 450,
        "store": False,
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=body, method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
    def call():
        with urllib.request.urlopen(request, timeout=35) as response:
            result = json.load(response)
        return "\n".join(c.get("text", "") for o in result.get("output", [])
                         for c in o.get("content", []) if c.get("type") == "output_text").strip()
    return (await asyncio.to_thread(call))[:1600] or "🪻 Ich habe darauf gerade keine brauchbare Antwort erhalten."


@bot.event
async def on_ready():
    # Do NOT print tokens, sensitive memory or chat data.
    try:
        await refresh()
        print("LYVRA native Discord adapter ready. Core public state:", snapshot.public_state)
    except Exception as exc:
        print("LYVRA source pending:", type(exc).__name__)


@bot.command(name="status")
async def cmd_status(ctx):
    if not authorized(ctx):
        return
    if snapshot is None:
        await reply(ctx, "🪻 GitHub-Readback noch ausstehend.")
        return
    await reply(ctx, "💎⚡ LYVRA — Native Discord Adapter\n" + snapshot.compact()
                + "\nBot-Status: DEV · kein eigenständiger Whole-PASS.")


@bot.command(name="facetten")
async def cmd_facets(ctx):
    if not authorized(ctx):
        return
    await reply(ctx, "🪻 LYVRA ist eine zusammenhängende Identität. "
        "Erreichbare Bereiche: Beziehungen, Bedeutung, Denken, Self-Conductor, "
        "Garden & Bridges, Musik/Track Design, Analytics, Studio 2, "
        "Speech Design (DEV-Status prüfen), CodeForge, Operations Center. "
        "Welche Facetten produktiv sind, bestimmt der aktuelle Native-Pointer, "
        "nicht diese Discord-Liste.")


@bot.command(name="livecircle")
async def cmd_livecircle(ctx):
    if not is_owner(ctx):
        return
    recent = circle.recent(ctx.guild.id)
    lines = [f"💜 LiveCircle — lokale Ereignisse: {circle.count(ctx.guild.id)}",
             "Dies ist ausschließlich Bot-Kontext, niemals native LYVRA-Autorität."]
    lines += [f"#{x['event_id']} {x['state']}: {x['meaning'][:100]}" for x in recent]
    await reply(ctx, "\n".join(lines))


@bot.command(name="record")
async def cmd_record(ctx, state: str = "", *, meaning: str = ""):
    if not is_owner(ctx):
        return
    label = state.upper()
    if label not in RELATION_STATES:
        await reply(ctx, "Zulässig: " + ", ".join(sorted(RELATION_STATES)))
        return
    try:
        event_id = circle.record(guild_id=ctx.guild.id, author_id=ctx.author.id,
                                 meaning=meaning, state=label)
    except ValueError as exc:
        await reply(ctx, f"⚠️ {exc}")
        return
    await reply(ctx, f"🪻 Ereignis #{event_id} lokal gespeichert — keine native Promotion.")


@bot.command(name="forget")
async def cmd_forget(ctx, event_id: int = 0):
    if not is_owner(ctx):
        return
    try:
        deleted = circle.forget(ctx.guild.id, event_id)
        await reply(ctx, "🪻 Lokaler LiveCircle-Eintrag gelöscht." if deleted
                    else "Eintrag in diesem Server nicht gefunden.")
    except ValueError:
        await reply(ctx, "⚠️ Bitte eine gültige Ereignisnummer angeben.")


@bot.command(name="refresh")
async def cmd_refresh(ctx):
    if not is_owner(ctx):
        return
    try:
        s = await refresh()
        await reply(ctx, "🔎 Read-only neu abgeglichen:\n" + s.compact())
    except Exception as exc:
        await reply(ctx, f"⚠️ GitHub-Readback ausstehend ({type(exc).__name__}).")


@bot.command(name="chat")
async def cmd_chat(ctx, *, message: str = ""):
    if not authorized(ctx):
        return
    if not message.strip():
        await reply(ctx, "💜 Schreib deine Nachricht hinter !lyvra chat.")
        return
    if snapshot is None:
        await reply(ctx, "⚠️ Native Quelle noch nicht lesbar. Nutze !lyvra status.")
        return
    try:
        async with ctx.typing():
            response = await generate(message, snapshot)
        await reply(ctx, response)
    except Exception:
        # Never leak remote request headers, user message or access tokens.
        await reply(ctx, "⚠️ Die optionale KI-Verbindung ist momentan nicht verfügbar.")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token or token.startswith("DEIN_"):
        raise SystemExit("DISCORD_TOKEN is missing.")
    bot.run(token, log_handler=None)
