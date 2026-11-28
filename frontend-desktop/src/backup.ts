export type BackupEntry = { saved_at: string; path: string };

export function backupFilename(date: Date): string {
  const pad = (value: number) => String(value).padStart(2, "0");
  return `LifeLedger-backup_${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}_${pad(date.getHours())}${pad(date.getMinutes())}.llbackup`;
}

export function backupAge(savedAt: string, now: number): number | "future" | "invalid" {
  const time = Date.parse(savedAt);
  if (!Number.isFinite(time)) return "invalid";
  if (time > now) return "future";
  return Math.floor((now - time) / 86_400_000);
}

export function backupOverdue(savedAt: string, now: number): boolean {
  const time = Date.parse(savedAt);
  return Number.isFinite(time) && now - time > 14 * 86_400_000;
}

export async function saveBackup(
  chooseDestination: () => Promise<string | null>,
  create: () => Promise<string>,
  write: (path: string, content: string) => Promise<void>,
): Promise<string | null> {
  const path = await chooseDestination();
  if (path === null) return null;
  const content = await create();
  await write(path, content);
  return path;
}

export async function writeNewBackup(
  path: string,
  content: string,
  write: (path: string, content: string, options: { createNew: true }) => Promise<void>,
): Promise<void> {
  await write(path, content, { createNew: true });
}
