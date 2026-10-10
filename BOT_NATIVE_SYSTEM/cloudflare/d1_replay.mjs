// Proposed D1 replay storage, not provisioned. Schema must be applied explicitly.
// Atomic one-statement insert with a unique primary key; errors fail closed.
export function d1ReplayGuard(db) {
  if (!db || typeof db.prepare !== "function") throw Error("D1_BINDING_MISSING");
  return {
    async claim(key) {
      if (typeof key !== "string" || key.length < 50 || key.length > 200) return false;
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(key));
      const id = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
      const until = Math.floor(Date.now() / 1000) + 600;
      const result = await db.prepare(
        "INSERT OR IGNORE INTO bot_replay_claims (id, expires_at) VALUES (?, ?)"
      ).bind(id, until).run();
      if (result?.success !== true) throw Error('D1_UNCONFIRMED');
      const changes = result?.meta?.changes;
      if (changes !== 0 && changes !== 1) throw Error('D1_CHANGE_COUNT_INVALID');
      return changes === 1;
    }
  };
}
