"""Read-only radio bridge offline HTTP fake and security regression tests."""
import io
import json
import unittest

from native_bridge.radio_readonly import (
    fetch_nowplaying, parse_nowplaying, validate_nowplaying_url,
)


HOST = "radio.example.com"
URL = "https://radio.example.com/api/nowplaying"


class FakeResponse:
    def __init__(self, data):
        self.body = io.BytesIO(data)
        self.status = 200

    def __enter__(self):
        return self

    def __exit__(self, typ, exc, tb):
        self.body.close()

    def read(self, size):
        return self.body.read(size)


class FakeOpener:
    def __init__(self, data):
        self.data = data
        self.methods = []

    def open(self, request, timeout):
        self.methods.append((request.get_method(), request.full_url, timeout))
        return FakeResponse(self.data)


class RadioBridgeTests(unittest.TestCase):
    def test_known_safe_url(self):
        self.assertEqual(validate_nowplaying_url(URL, HOST), URL)

    def test_reject_unsafe_host_and_paths(self):
        bad_urls = [
            "http://radio.example.com/api/nowplaying",
            "https://example.org/api/nowplaying",
            "https://radio.example.com/radio/autodj/skip",
            "https://radio.example.com/api/nowplaying?token=secret",
            "https://login:pass@radio.example.com/api/nowplaying",
            "https://radio.example.com:8443/api/nowplaying",
            "https://radio.example.com/api/nowplaying#fragment",
        ]
        for url in bad_urls:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_nowplaying_url(url, HOST)

    def test_refuse_private_ip_hosts(self):
        for host in ["127.0.0.1", "192.168.0.1", "::1", "localhost",
                     "private.local", "machine.internal", "invalid"]:
            with self.subTest(host=host), self.assertRaises(ValueError):
                validate_nowplaying_url(URL, host)

    def test_public_flat_metadata(self):
        row = parse_nowplaying({"title": "Acid Fields", "artist": "Fraggle",
                                "dj_display": "LYVRA DJ", "is_online": True,
                                "listeners": 2, "admin_token": "secret"})
        text = row.public_text()
        self.assertIn("Acid Fields", text)
        self.assertEqual(row.status, "online")
        self.assertNotIn("listeners", text)
        self.assertNotIn("secret", text)

    def test_nested_song(self):
        row = parse_nowplaying({"now_playing": {"song": {
            "title": "Track", "artist": "Artist"}}})
        self.assertEqual(row.title, "Track")
        self.assertEqual(row.artist, "Artist")
        self.assertEqual(row.status, "unbestätigt")

    def test_sanitize_control_and_markup(self):
        row = parse_nowplaying({"title": "Test\n<script>bad</script>"})
        self.assertNotIn("<script>", row.public_text())
        self.assertNotIn("\n", row.title)

    def test_reject_missing_metadata(self):
        with self.assertRaises(ValueError):
            parse_nowplaying({"listeners": 10})

    def test_http_reads_only_get(self):
        opener = FakeOpener(json.dumps({"title": "Now playing"}).encode())
        row = fetch_nowplaying(URL, allowed_host=HOST, opener=opener)
        self.assertEqual(row.title, "Now playing")
        self.assertEqual(opener.methods, [("GET", URL, 4.0)])

    def test_overlarge_data_rejected(self):
        opener = FakeOpener(b"{" + b"x" * 33000)
        with self.assertRaises(ValueError):
            fetch_nowplaying(URL, allowed_host=HOST, opener=opener)

    def test_timeout_limit(self):
        with self.assertRaises(ValueError):
            fetch_nowplaying(URL, allowed_host=HOST, timeout=100, opener=FakeOpener(b"{}"))


if __name__ == "__main__":
    unittest.main()
