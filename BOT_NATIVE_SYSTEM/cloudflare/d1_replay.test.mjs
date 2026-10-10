import {test} from "node:test";
import assert from "node:assert/strict";
import {webcrypto} from "node:crypto";
import {d1ReplayGuard} from "./d1_replay.mjs";
if (!globalThis.crypto) globalThis.crypto=webcrypto;
function mockDb() {
 const keys=new Set();
 return {prepare(sql) {
  assert.match(sql,/INSERT OR IGNORE/);
  return {bind(id,expires) {
   return {async run() {
    if(keys.has(id)) return {meta:{changes:0}};
    keys.add(id);
    return {meta:{changes:1}};
   }};
  }};
 }};
}
const key="1".repeat(128);
test("first insert succeeds, replay rejected",async()=>{const x=d1ReplayGuard(mockDb());assert.equal(await x.claim(key),true);assert.equal(await x.claim(key),false)});
test("missing binding rejects",()=>assert.throws(()=>d1ReplayGuard(),/D1_BINDING_MISSING/));
test("invalid key rejected",async()=>assert.equal(await d1ReplayGuard(mockDb()).claim("x"),false));
test("storage error propagates for fail closed upstream",async()=>{const x=d1ReplayGuard({prepare(){throw Error("quota")}});await assert.rejects(x.claim(key),/quota/)});
