// Cloudflare-only Discord HTTP Interactions adapter, nonproduction.
// Ed25519 signature validation occurs before all parsing. No outbound API,
// model inference, KV/D1 writes, native LYVRA Worker calls, or paid features.
const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: {"content-type": "application/json; charset=utf-8", "cache-control": "no-store"}
});
const validHex = (s, length) => typeof s === "string" &&
  s.length === length && /^[0-9a-f]+$/i.test(s);
const bytes = (s) => new Uint8Array(s.match(/../g).map(x => parseInt(x, 16)));
export async function verifyDiscordRequest(request, publicKey) {
  const signature = request.headers.get("x-signature-ed25519");
  const timestamp = request.headers.get("x-signature-timestamp");
  if (!validHex(signature, 128) || !validHex(publicKey, 64) ||
      !timestamp || !/^\d{10}$/.test(timestamp)) return false;
  const t = Number(timestamp);
  if (!Number.isSafeInteger(t) || Math.abs(Math.floor(Date.now()/1000) - t) > 300) return false;
  try {
    const body = await request.clone().arrayBuffer();
    if (body.byteLength > 65536) return false;
    const signed = new Uint8Array(new TextEncoder().encode(timestamp).length + body.byteLength);
    signed.set(new TextEncoder().encode(timestamp));
    signed.set(new Uint8Array(body), timestamp.length);
    const key = await crypto.subtle.importKey("raw", bytes(publicKey), {name: "Ed25519"}, false, ["verify"]);
    return await crypto.subtle.verify("Ed25519", key, bytes(signature), signed);
  } catch { return false; }
}
export default {
  async fetch(request, env) {
    if (request.method !== "POST") return json({ok:false,code:"METHOD_DENIED"}, 405);
    if (!env?.DISCORD_PUBLIC_KEY || !await verifyDiscordRequest(request, env.DISCORD_PUBLIC_KEY)) {
      return json({ok:false,code:"BAD_SIGNATURE"}, 401);
    }
    let interaction;
    try { interaction = await request.json(); } catch { return json({ok:false,code:"BAD_BODY"},400); }
    if (interaction?.type === 1) return json({type:1});
    // Publicly signed requests do not grant permission to operate the character bot.
    // All other commands stay disabled until identity/replay/cost/handoff gates are implemented.
    return json({type:4,data:{content:"LYVRA Character Bot: deployment not authorized.",flags:64}});
  }
};
