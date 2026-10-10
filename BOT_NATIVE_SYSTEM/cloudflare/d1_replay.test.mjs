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
    if(keys.has(id)) return {success:true,meta:{changes:0}};
    keys.add(id);
    return {success:true,meta:{changes:1}};
   }};
  }};
 }};
}
const key="1".repeat(128);
test("first insert succeeds, replay rejected",async()=>{const x=d1ReplayGuard(mockDb());assert.equal(await x.claim(key),true);assert.equal(await x.claim(key),false)});
test("missing binding rejects",()=>assert.throws(()=>d1ReplayGuard(),/D1_BINDING_MISSING/));
test("invalid key rejected",async()=>assert.equal(await d1ReplayGuard(mockDb()).claim("x"),false));
test("storage error propagates for fail closed upstream",async()=>{const x=d1ReplayGuard({prepare(){throw Error("quota")}});await assert.rejects(x.claim(key),/quota/)});

test("unconfirmed write must not accept request",async()=>{
 const db={prepare(){return {bind(){return {async run(){return {success:false,meta:{changes:1}}}}}}}};
 await assert.rejects(d1ReplayGuard(db).claim(key),/D1_UNCONFIRMED/);
});

test('missing changes rejects rather than assuming replay',async()=>{
 const db={prepare(){return {bind(){return {async run(){return {success:true,meta:{}}}}}}}};
 await assert.rejects(d1ReplayGuard(db).claim(key),/D1_CHANGE_COUNT_INVALID/);
});
test('invalid changes rejects',async()=>{
 const db={prepare(){return {bind(){return {async run(){return {success:true,meta:{changes:2}}}}}}}};
 await assert.rejects(d1ReplayGuard(db).claim(key),/D1_CHANGE_COUNT_INVALID/);
});
