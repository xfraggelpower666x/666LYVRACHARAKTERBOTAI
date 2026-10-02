"""Strictly read-only radio metadata bridge; never a radio controller.

Only explicit HTTPS GET /api/nowplaying to an exact operator configured DNS host.
Does NOT expose stream admin endpoints, tokens, cookies or listener identifiers.
"""
from __future__ import annotations
import ipaddress
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class RadioNowPlaying:
    title: str
    artist: str
    dj: str
    status: str

    def public_text(self) -> str:
        parts = [f"🎵 {self.title or 'Track nicht bekannt'}"]
        if self.artist:
            parts.append(f"Künstler: {self.artist}")
        if self.dj:
            parts.append(f"DJ: {self.dj}")
        parts.append(f"Stream: {self.status}")
        return "\n".join(parts)


def _public_text(value: object, max_len: int = 180) -> str:
    if not isinstance(value, (str, int, float)):
        return ""
    text = re.sub(r"[\x00-\x1f\x7f]+", " ", str(value))
    text = re.sub(r"<[^>]*>", "", text)
    return " ".join(text.split())[:max_len]


def parse_nowplaying(payload: object) -> RadioNowPlaying:
    if not isinstance(payload, dict):
        raise ValueError("Radio metadata must be an object")
    body = payload.get("now_playing")
    song = body.get("song") if isinstance(body, dict) else None
    title = _public_text(payload.get("display_title") or payload.get("title")
                         or (song.get("title") if isinstance(song, dict) else "")
                         or payload.get("songtitle"))
    artist = _public_text(payload.get("artist") or
                          (song.get("artist") if isinstance(song, dict) else ""))
    dj = _public_text(payload.get("dj_display") or payload.get("dj"))
    if not title and not dj:
        raise ValueError("No public now-playing fields")
    # Avoid rendering unverified operational health from a title-only response.
    is_online = payload.get("is_online")
    status = "online" if is_online is True else ("offline" if is_online is False else "unbestätigt")
    return RadioNowPlaying(title, artist, dj, status)


def validate_nowplaying_url(url: str, allowed_host: str) -> str:
    if not isinstance(url, str) or not allowed_host:
        raise ValueError("Missing URL or allowlisted host")
    allowed_host = allowed_host.lower().strip().rstrip(".")
    try:
        ipaddress.ip_address(allowed_host)
    except ValueError:
        pass
    else:
        raise ValueError("IP literals are not allowed")
    if ("." not in allowed_host or allowed_host == "localhost"
            or allowed_host.endswith((".localhost", ".local", ".internal", ".test"))
            or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789.-" for c in allowed_host)):
        raise ValueError("Unsafe radio hostname")
    p = urllib.parse.urlsplit(url)
    if (p.scheme != "https" or p.hostname != allowed_host
            or p.port not in (None, 443) or p.username or p.password
            or p.query or p.fragment or p.path != "/api/nowplaying"):
        raise ValueError("Radio metadata URL is not allowlisted")
    return url


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_nowplaying(url: str, *, allowed_host: str, timeout: float = 4.0,
                     opener=None) -> RadioNowPlaying:
    validate_nowplaying_url(url, allowed_host)
    if not 0.1 <= timeout <= 10.0:
        raise ValueError("Unsafe HTTP timeout")
    request = urllib.request.Request(url, headers={
        "User-Agent": "LYVRA-discord-radio-readonly/0.1",
        "Accept": "application/json",
    }, method="GET")
    # The optional opener is a test seam only: production uses no-redirect HTTP.
    sender = opener if opener is not None else urllib.request.build_opener(_NoRedirect())
    with sender.open(request, timeout=timeout) as response:
        if getattr(response, "status", 200) != 200:
            raise ValueError("Radio API status is not successful")
        blob = response.read(32769)
        if len(blob) > 32768:
            raise ValueError("Oversize metadata response")
    return parse_nowplaying(json.loads(blob.decode("utf-8")))
