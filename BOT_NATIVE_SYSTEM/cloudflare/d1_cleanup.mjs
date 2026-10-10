// Bot-only proposed bounded replay garbage collection. No cron or DB provisioned.
// Explicit invocation only; verify actual D1 free budget before activation.
export async function cleanupExpiredClaims(db, {limit=25, now=Math.floor(Date.now()/1000)}={}) {
  if (!db || typeof db.prepare !== "function") throw Error("D1_BINDING_MISSING");
  if (!Number.isInteger(limit) || limit < 1 || limit > 25) throw Error("CLEANUP_LIMIT_INVALID");
  if (!Number.isSafeInteger(now) || now < 0) throw Error("CLEANUP_TIME_INVALID");
  const result = await db.prepare(
    "DELETE FROM bot_replay_claims WHERE id IN (SELECT id FROM bot_replay_claims WHERE expires_at < ? ORDER BY expires_at LIMIT ?)"
  ).bind(now, limit).run();
  if (result?.success !== true) throw Error("D1_CLEANUP_UNCONFIRMED");
  const count = result?.meta?.changes;
  if (!Number.isInteger(count) || count < 0 || count > limit) throw Error("D1_CLEANUP_COUNT_INVALID");
  return count;
}
