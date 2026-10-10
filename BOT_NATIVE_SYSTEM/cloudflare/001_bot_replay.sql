-- Bot-local Cloudflare D1 migration (proposal only; not executed).
-- Never apply to LYVRA, PET, CLIC, STREAM or radio databases.
CREATE TABLE IF NOT EXISTS bot_replay_claims (
  id TEXT PRIMARY KEY NOT NULL,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_bot_replay_expires ON bot_replay_claims(expires_at);
-- Planned optional periodic cleanup, only with an explicitly approved zero-cost quota:
-- DELETE FROM bot_replay_claims WHERE expires_at < unixepoch();
