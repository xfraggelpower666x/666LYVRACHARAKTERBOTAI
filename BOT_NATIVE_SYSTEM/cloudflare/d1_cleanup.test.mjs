import test from "node:test";
import assert from "node:assert/strict";
import {cleanupExpiredClaims} from "./d1_cleanup.mjs";
const db=(result)=>({prepare(sql){assert.match(sql,/DELETE FROM bot_replay_claims/);return {bind(now,limit){assert.equal(limit,25);return {async run(){return result}}}}}});
test("bounded cleanup reports confirmed count",async()=>assert.equal(await cleanupExpiredClaims(db({success:true,meta:{changes:3}}),{now:1000}),3));
test("cleanup missing DB fails",async()=>await assert.rejects(cleanupExpiredClaims(null),/D1_BINDING_MISSING/));
test("cleanup cannot exceed hard limit",async()=>await assert.rejects(cleanupExpiredClaims(db({success:true,meta:{changes:0}}),{limit:26}),/CLEANUP_LIMIT_INVALID/));
test("cleanup rejects DB uncertainty",async()=>await assert.rejects(cleanupExpiredClaims(db({success:false,meta:{changes:1}})),/D1_CLEANUP_UNCONFIRMED/));
test("cleanup rejects invalid affected rows",async()=>await assert.rejects(cleanupExpiredClaims(db({success:true,meta:{changes:26}})),/D1_CLEANUP_COUNT_INVALID/));
