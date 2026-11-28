import assert from "node:assert/strict";
import test from "node:test";
import { saveBackup } from "../src/backup.ts";

test("saves the encrypted backup at the selected path", async () => {
  const writes: Array<[string, string]> = [];
  const path = await saveBackup(
    async () => "C:\\Test\\backup.llbackup",
    async () => "encrypted-base64",
    async (destination, content) => { writes.push([destination, content]); },
  );
  assert.equal(path, "C:\\Test\\backup.llbackup");
  assert.deepEqual(writes, [["C:\\Test\\backup.llbackup", "encrypted-base64"]]);
});

test("cancelling the dialog does not create or write a backup", async () => {
  const path = await saveBackup(
    async () => null,
    async () => { throw new Error("should not create"); },
    async () => { throw new Error("should not write"); },
  );
  assert.equal(path, null);
});

test("creation and filesystem errors are propagated", async () => {
  await assert.rejects(saveBackup(
    async () => "backup.llbackup",
    async () => { throw new Error("API failed"); },
    async () => { throw new Error("should not write"); },
  ), /API failed/);
  await assert.rejects(saveBackup(
    async () => "backup.llbackup",
    async () => "encrypted-base64",
    async () => { throw new Error("disk full"); },
  ), /disk full/);
});
