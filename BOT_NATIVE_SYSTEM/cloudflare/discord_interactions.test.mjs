import test from "node:test";
import assert from "node:assert/strict";
import {webcrypto, generateKeyPairSync, sign} from "node:crypto";
import adapter, {verifyDiscordRequest} from "./discord_interactions.mjs";
if (!globalThis.crypto) globalThis.crypto = webcrypto;

const {privateKey, publicKey} = generateKeyPairSync("ed25519");
const pk = publicKey.export({format:"der",type:"spki"}).subarray(-32).toString("hex");
const claimOnce = () => {
  const seen = new Set();
  return {claim: async (key) => {
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }};
};
const ready = () => ({DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true',BOT_ALLOW_MOCK_REPLAY:'true',REPLAY_GUARD:claimOnce()});
function signed(body, timestamp = String(Math.floor(Date.now()/1000))) {
  const sig=sign(null,Buffer.concat([Buffer.from(timestamp),Buffer.from(body)]),privateKey).toString("hex");
  return new Request("https://bot.invalid/interactions",{
    method:"POST",headers:{"x-signature-ed25519":sig,"x-signature-timestamp":timestamp},
    body
  });
}
test("valid signature and ping only", async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),ready());
  assert.equal(r.status,200);assert.deepEqual(await r.json(),{type:1});
});
test("ordinary signed commands remain blocked",async()=>{
  const r=await adapter.fetch(signed('{"type":2}'),ready());
  assert.equal((await r.json()).data.flags,64);
});
test("no configured public key denies",async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),{BOT_INTERACTIONS_TEST_ENABLED:'true',BOT_ALLOW_MOCK_REPLAY:'true',REPLAY_GUARD:claimOnce()});
  assert.equal(r.status,401);
});
test("tampered payload denies",async()=>{
  const r=signed('{"type":1}');
  const headers=new Headers(r.headers);
  const altered=new Request(r.url,{method:"POST",headers,body:'{"type":2}'});
  assert.equal(await verifyDiscordRequest(altered,pk),false);
});
test("expired signature denies",async()=>{
  const r=signed('{"type":1}',String(Math.floor(Date.now()/1000)-400));
  assert.equal(await verifyDiscordRequest(r,pk),false);
});
test("unsigned and GET deny",async()=>{
  const r=await adapter.fetch(new Request("https://bot.invalid/",{method:"POST",body:'{"type":1}'}),ready());
  assert.equal(r.status,401);
  const get=await adapter.fetch(new Request("https://bot.invalid/"),ready());
  assert.equal(get.status,405);
});

test("default disabled even for signed ping", async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),{DISCORD_PUBLIC_KEY:pk});
  assert.equal(r.status,503);
  assert.equal((await r.json()).code,"BOT_DISABLED");
});

test("missing atomic replay guard fails closed", async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),{DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true'});
  assert.equal(r.status,503);
  assert.equal((await r.json()).code,"REPLAY_GUARD_REQUIRED");
});
test("same signed request rejected on second claim", async()=>{
  const env=ready(), req=signed('{"type":1}');
  assert.equal((await adapter.fetch(req.clone(),env)).status,200);
  const r=await adapter.fetch(req.clone(),env);
  assert.equal(r.status,409);
  assert.equal((await r.json()).code,"REPLAY_REJECTED");
});
test("replay service outage fails closed", async()=>{
  const env={...ready(),REPLAY_GUARD:{claim:async()=>{throw Error("offline")}}};
  const r=await adapter.fetch(signed('{"type":1}'),env);
  assert.equal(r.status,503);
  assert.equal((await r.json()).code,"REPLAY_GUARD_UNAVAILABLE");
});

test("invalid D1 binding fails closed without crash", async()=>{
  const env={DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true',BOT_REPLAY_DB:{}};
  const result=await adapter.fetch(signed('{"type":1}'),env);
  assert.equal(result.status,503);
  assert.equal((await result.json()).code,"REPLAY_GUARD_UNAVAILABLE");
});
test("mock flag without test activation remains disabled", async()=>{
  const env={DISCORD_PUBLIC_KEY:pk,BOT_ALLOW_MOCK_REPLAY:'true',REPLAY_GUARD:claimOnce()};
  const result=await adapter.fetch(signed('{"type":1}'),env);
  assert.equal(result.status,503);
  assert.equal((await result.json()).code,"BOT_DISABLED");
});
test("test activation without mock flag cannot use local replay", async()=>{
  const env={DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true',REPLAY_GUARD:claimOnce()};
  const result=await adapter.fetch(signed('{"type":1}'),env);
  assert.equal(result.status,503);
  assert.equal((await result.json()).code,"REPLAY_GUARD_REQUIRED");
});

test("oversized signed body is rejected before replay claim", async()=>{
  let called=false;
  const env={...ready(),REPLAY_GUARD:{claim:async()=>{called=true;return true;}}};
  const result=await adapter.fetch(signed("x".repeat(65537)),env);
  assert.equal(result.status,401);
  assert.equal(called,false);
});
test("exactly 64KiB signed body passes signature gate then rejects invalid JSON",async()=>{
  const data=" ".repeat(65536);
  const result=await adapter.fetch(signed(data),ready());
  assert.equal(result.status,400);
  assert.equal((await result.json()).code,"BAD_BODY");
});

test('declared oversized request denied',async()=>{
 const req=signed('{"type":1}');
 req.headers.set('content-length','65537');
 assert.equal((await adapter.fetch(req,ready())).status,401);
});
