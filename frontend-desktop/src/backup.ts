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
