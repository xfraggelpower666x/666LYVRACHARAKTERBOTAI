import test from "node:test";
import assert from "node:assert/strict";
import {webcrypto, generateKeyPairSync, sign} from "node:crypto";
import adapter, {verifyDiscordRequest} from "./discord_interactions.mjs";
if (!globalThis.crypto) globalThis.crypto = webcrypto;

const {privateKey, publicKey} = generateKeyPairSync("ed25519");
const pk = publicKey.export({format:"der",type:"spki"}).subarray(-32).toString("hex");
function signed(body, timestamp = String(Math.floor(Date.now()/1000))) {
  const sig=sign(null,Buffer.concat([Buffer.from(timestamp),Buffer.from(body)]),privateKey).toString("hex");
  return new Request("https://bot.invalid/interactions",{
    method:"POST",headers:{"x-signature-ed25519":sig,"x-signature-timestamp":timestamp},
    body
  });
}
test("valid signature and ping only", async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),{DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true'});
  assert.equal(r.status,200);assert.deepEqual(await r.json(),{type:1});
});
test("ordinary signed commands remain blocked",async()=>{
  const r=await adapter.fetch(signed('{"type":2}'),{DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true'});
  assert.equal((await r.json()).data.flags,64);
});
test("no configured public key denies",async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),{BOT_INTERACTIONS_TEST_ENABLED:'true'});
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
  const r=await adapter.fetch(new Request("https://bot.invalid/",{method:"POST",body:'{"type":1}'}),{DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true'});
  assert.equal(r.status,401);
  const get=await adapter.fetch(new Request("https://bot.invalid/"),{DISCORD_PUBLIC_KEY:pk,BOT_INTERACTIONS_TEST_ENABLED:'true'});
  assert.equal(get.status,405);
});

test("default disabled even for signed ping", async()=>{
  const r=await adapter.fetch(signed('{"type":1}'),{DISCORD_PUBLIC_KEY:pk});
  assert.equal(r.status,503);
  assert.equal((await r.json()).code,"BOT_DISABLED");
});
