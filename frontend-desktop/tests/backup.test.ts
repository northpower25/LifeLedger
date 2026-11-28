import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, readFile, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { saveBackup, writeNewBackup } from "../src/backup.ts";

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

test("backup creation never replaces an existing backup or symlink", async () => {
  const dir = await mkdtemp(join(tmpdir(), "lifeledger-backup-"));
  const original = join(dir, "original.llbackup");
  const link = join(dir, "link.llbackup");
  const writer = (path: string, content: string, options: { createNew: true }) =>
    writeFile(path, content, { flag: options.createNew ? "wx" : "w" });
  try {
    await writeFile(original, "original-backup");
    await assert.rejects(writeNewBackup(original, "other-backup", writer));
    if (process.platform !== "win32") {
      await symlink(original, link);
      await assert.rejects(writeNewBackup(link, "other-backup", writer));
    }
    assert.equal(await readFile(original, "utf8"), "original-backup");
    await writeNewBackup(join(dir, "new.llbackup"), "new-backup", writer);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
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
