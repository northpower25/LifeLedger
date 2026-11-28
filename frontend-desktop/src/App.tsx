import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { isTauri } from "@tauri-apps/api/core";
import { save } from "@tauri-apps/plugin-dialog";
import { writeTextFile } from "@tauri-apps/plugin-fs";
import { QRCodeSVG } from "qrcode.react";
import { api, FhirResource } from "./api";
import { backupAge, backupFilename, backupOverdue, BackupEntry, saveBackup, writeNewBackup } from "./backup";
import { Locale, message } from "./i18n";

type OwnerStatus = { owner_exists: boolean; owner_confirmed: boolean };
type TimelineEntry = {
  occurred_at: string;
  resource_type: string;
  resource: FhirResource;
};

function base64(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

export default function App() {
  const [locale, setLocale] = useState<Locale>("de");
  const [ownerStatus, setOwnerStatus] = useState<OwnerStatus>();
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [totp, setTotp] = useState("");
  const [totpSecret, setTotpSecret] = useState("");
  const [totpUri, setTotpUri] = useState("");
  const [token, setToken] = useState("");
  const [patientName, setPatientName] = useState("");
  const [medicationName, setMedicationName] = useState("");
  const [documentTitle, setDocumentTitle] = useState("");
  const [documentFile, setDocumentFile] = useState<File>();
  const [backupPassword, setBackupPassword] = useState("");
  const [restorePassword, setRestorePassword] = useState("");
  const [patients, setPatients] = useState<FhirResource[]>([]);
  const [selectedPatient, setSelectedPatient] = useState("");
  const [timeline, setTimeline] = useState<TimelineEntry[]>([]);
  const [error, setError] = useState("");
  const [backupStatus, setBackupStatus] = useState("");
  const [backupError, setBackupError] = useState("");
  const [savingBackup, setSavingBackup] = useState(false);
  const [backupHistory, setBackupHistory] = useState<BackupEntry[] | null>(null);
  const [historyError, setHistoryError] = useState(false);
  const [now, setNow] = useState(Date.now());
  const historyVersion = useRef(0);
  const [recovering, setRecovering] = useState(false);
  const [recoveryStatus, setRecoveryStatus] = useState("");
  const [replacementBackup, setReplacementBackup] = useState("");
  const [replacementPassword, setReplacementPassword] = useState("");
  const [replacementCode, setReplacementCode] = useState("");
  const [replacementConfirmed, setReplacementConfirmed] = useState(false);
  const [replacementBusy, setReplacementBusy] = useState(false);
  const text = useMemo(() => (key: Parameters<typeof message>[1]) => message(locale, key), [locale]);

  useEffect(() => {
    api<OwnerStatus>("/owner/status")
      .then(setOwnerStatus)
      .catch(() => setError(text("error")));
  }, [text]);

  useEffect(() => {
    let active = true;
    const version = ++historyVersion.current;
    setBackupHistory(null);
    setHistoryError(false);
    if (token) {
      api<BackupEntry[]>("/backup/history", {}, token)
        .then((entries) => { if (active && historyVersion.current === version) setBackupHistory(entries); })
        .catch(() => { if (active && historyVersion.current === version) setHistoryError(true); });
    }
    return () => { active = false; };
  }, [token]);

  useEffect(() => {
    if (!token) return;
    setNow(Date.now());
    const timer = window.setInterval(() => setNow(Date.now()), 60_000);
    return () => window.clearInterval(timer);
  }, [token]);

  async function submit(event: FormEvent, operation: () => Promise<void>) {
    event.preventDefault();
    setError("");
    try {
      await operation();
    } catch {
      setError(text("error"));
    }
  }

  async function refreshPatients(session = token) {
    const records = await api<FhirResource[]>("/patients", {}, session);
    setPatients(records);
    if (!selectedPatient && records[0]) setSelectedPatient(records[0].id);
  }

  async function setup(event: FormEvent) {
    await submit(event, async () => {
      const result = await api<{ totp_secret: string; totp_uri: string }>("/owner/setup", {
        method: "POST",
        body: JSON.stringify({ display_name: displayName, password }),
      });
      setTotpSecret(result.totp_secret);
      setTotpUri(result.totp_uri);
      setOwnerStatus({ owner_exists: true, owner_confirmed: false });
    });
  }

  async function confirmSetup(event: FormEvent) {
    await submit(event, async () => {
      const session = await api<{ access_token: string }>("/owner/setup/confirm", {
        method: "POST",
        body: JSON.stringify({ password, code: totp }),
      });
      setToken(session.access_token);
      setTotpSecret("");
      setTotpUri("");
      setOwnerStatus({ owner_exists: true, owner_confirmed: true });
      await refreshPatients(session.access_token);
    });
  }

  async function resumeSetup(event: FormEvent) {
    await submit(event, async () => {
      const result = await api<{ totp_secret: string; totp_uri: string }>("/owner/setup/resume", {
        method: "POST",
        body: JSON.stringify({ password }),
      });
      setTotpSecret(result.totp_secret);
      setTotpUri(result.totp_uri);
    });
  }

  async function unlock(event: FormEvent) {
    await submit(event, async () => {
      const session = await api<{ access_token: string }>("/owner/unlock", {
        method: "POST",
        body: JSON.stringify({ password, code: totp }),
      });
      setToken(session.access_token);
      await refreshPatients(session.access_token);
    });
  }

  async function addPatient(event: FormEvent) {
    await submit(event, async () => {
      const patient = await api<FhirResource>("/patients", {
        method: "POST",
        body: JSON.stringify({ name: patientName, synthetic: true }),
      }, token);
      setPatientName("");
      await refreshPatients();
      setSelectedPatient(patient.id);
      await refreshTimeline(patient.id);
    });
  }

  async function refreshTimeline(patientId = selectedPatient) {
    if (!patientId) return;
    const entries = await api<TimelineEntry[]>(
      `/patients/${patientId}/timeline`,
      {},
      token,
    );
    setTimeline(entries);
  }

  async function addMedication(event: FormEvent) {
    await submit(event, async () => {
      await api(`/patients/${selectedPatient}/medication-statements`, {
        method: "POST",
        body: JSON.stringify({
          patient_id: selectedPatient,
          medication_text: medicationName,
          effective_datetime: new Date().toISOString(),
          synthetic: true,
        }),
      }, token);
      setMedicationName("");
      await refreshTimeline();
    });
  }

  async function addDocument(event: FormEvent) {
    await submit(event, async () => {
      if (!documentFile) return;
      const types = ["application/pdf", "image/png", "text/plain"];
      if (!types.includes(documentFile.type)) throw new Error("unsupported_file");
      const content = base64(new Uint8Array(await documentFile.arrayBuffer()));
      await api(`/patients/${selectedPatient}/documents`, {
        method: "POST",
        body: JSON.stringify({
          patient_id: selectedPatient,
          title: documentTitle,
          content_type: documentFile.type,
          content_base64: content,
          synthetic: true,
        }),
      }, token);
      setDocumentTitle("");
      setDocumentFile(undefined);
      await refreshTimeline();
    });
  }

  async function createBackup(event: FormEvent) {
    event.preventDefault();
    setError("");
    setBackupError("");
    setBackupStatus("");
    if (backupPassword.length < 12) {
      setBackupError(text("backupPasswordInvalid"));
      return;
    }
    if (replacementBackup && !isTauri()) {
      setBackupError(text("replacementDesktopOnly"));
      return;
    }
    setSavingBackup(true);
    try {
      const create = async () => {
        const result = await api<{ backup_base64: string }>("/backup", {
          method: "POST",
          body: JSON.stringify({ passphrase: backupPassword }),
        }, token);
        return result.backup_base64;
      };
      if (isTauri()) {
        const path = await saveBackup(
          () => save({
            defaultPath: backupFilename(new Date()),
            filters: [{ name: "LifeLedger Backup", extensions: ["llbackup"] }],
          }),
          create,
          (path, content) => writeNewBackup(path, content, writeTextFile),
        );
        setBackupStatus(path === null ? text("backupCancelled") : `${text("backupSaved")} ${path}`);
        if (path !== null) {
          ++historyVersion.current;
          try {
            await api<BackupEntry>("/backup/saved", {
              method: "POST",
              body: JSON.stringify({ path }),
            }, token);
          } catch {
            setHistoryError(true);
            setBackupError(text("backupRecordFailed"));
            return;
          }
          try {
            const entries = await api<BackupEntry[]>("/backup/history", {}, token);
            setBackupHistory(entries);
            setHistoryError(false);
            setNow(Date.now());
          } catch {
            setHistoryError(true);
          }
        }
      } else {
        const content = await create();
        const link = document.createElement("a");
        link.href = URL.createObjectURL(new Blob([content], { type: "text/plain" }));
        link.download = backupFilename(new Date());
        link.click();
        window.setTimeout(() => URL.revokeObjectURL(link.href), 60_000);
        setBackupStatus(text("backupDownloadStarted"));
      }
    } catch {
      setBackupError(text("backupSaveFailed"));
    } finally {
      setSavingBackup(false);
    }
  }

  async function restoreBackup(event: FormEvent, file?: File) {
    event.preventDefault();
    setBackupStatus("");
    setBackupError("");
    setReplacementBusy(true);
    try {
      if (!file || restorePassword.length < 12) throw new Error("invalid_backup_input");
      const backupBase64 = (await file.text()).trim();
      await api("/backup/validate", {
        method: "POST",
        body: JSON.stringify({
          passphrase: restorePassword,
          backup_base64: backupBase64,
        }),
      }, token);
      setReplacementBackup(backupBase64);
      setReplacementConfirmed(false);
    } catch {
      setBackupError(text("recoveryFailed"));
    } finally {
      setReplacementBusy(false);
    }
  }

  async function replaceBackup(event: FormEvent) {
    event.preventDefault();
    setBackupError("");
    setReplacementBusy(true);
    try {
      await api("/backup/replace", {
        method: "POST",
        body: JSON.stringify({
          passphrase: restorePassword,
          backup_base64: replacementBackup,
          password: replacementPassword,
          code: replacementCode,
        }),
      }, token);
      setToken("");
      setPatients([]);
      setSelectedPatient("");
      setTimeline([]);
      setBackupPassword("");
      setRestorePassword("");
      setReplacementBackup("");
      setReplacementPassword("");
      setReplacementCode("");
      setOwnerStatus({ owner_exists: true, owner_confirmed: true });
      setRecoveryStatus(text("recoverySucceeded"));
    } catch {
      setBackupError(text("replacementFailed"));
    } finally {
      setReplacementBusy(false);
    }
  }

  async function recoverBackup(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const fileInput = form.elements.namedItem("recoveryFile");
    const file = fileInput instanceof HTMLInputElement ? fileInput.files?.[0] : undefined;
    setError("");
    setRecoveryStatus("");
    if (!file || backupPassword.length < 12) {
      setError(text("recoveryInputInvalid"));
      return;
    }
    setRecovering(true);
    try {
      await api("/backup/recover", {
        method: "POST",
        body: JSON.stringify({
          passphrase: backupPassword,
          backup_base64: (await file.text()).trim(),
        }),
      });
      setBackupPassword("");
      setRestorePassword("");
      setReplacementBackup("");
      setReplacementPassword("");
      setReplacementCode("");
      form.reset();
      setOwnerStatus({ owner_exists: true, owner_confirmed: true });
      setRecoveryStatus(text("recoverySucceeded"));
    } catch (error) {
      setError(error instanceof Error && error.message === "recovery_database_not_empty"
        ? text("recoveryNotEmpty") : text("recoveryFailed"));
    } finally {
      setRecovering(false);
    }
  }

  async function lock() {
    try {
      await api("/owner/lock", { method: "POST" }, token);
    } finally {
      setToken("");
      setPatients([]);
      setSelectedPatient("");
      setTimeline([]);
      setBackupStatus("");
      setBackupError("");
      setBackupPassword("");
      setRestorePassword("");
      setReplacementBackup("");
      setReplacementPassword("");
      setReplacementCode("");
    }
  }

  useEffect(() => {
    if (token && selectedPatient) {
      refreshTimeline().catch(() => setError(text("error")));
    }
  }, [token, selectedPatient]);

  const latestBackup = backupHistory?.[0];
  const age = latestBackup ? backupAge(latestBackup.saved_at, now) : null;

  return (
    <main>
      <header className="topbar">
        <div>
          <h1>{text("title")}</h1>
          <p>{text("subtitle")}</p>
        </div>
        <div className="top-actions">
          <label className="visually-hidden" htmlFor="locale">Language</label>
          <select id="locale" value={locale} onChange={(event) => setLocale(event.target.value as Locale)}>
            <option value="de">Deutsch</option>
            <option value="en">English</option>
          </select>
          {token && <button className="secondary" disabled={savingBackup || replacementBusy} onClick={lock}>{text("lock")}</button>}
        </div>
      </header>

      <p className="warning" role="note">{text("syntheticWarning")}</p>
      {error && <p className="error" role="alert">{error}</p>}
      {recoveryStatus && <p role="status">{recoveryStatus}</p>}
      {token && historyError && <p className="error" role="alert">{text("backupHistoryFailed")}</p>}
      {token && backupHistory && !historyError && (
        !latestBackup ? <p className="warning" role="note">{text("backupNever")}</p>
          : age === "future" || age === "invalid" ? <p className="warning" role="note">{text("backupClockWarning")}</p>
            : backupOverdue(latestBackup.saved_at, now) && <p className="warning" role="note">{text("backupReminder").replace("{days}", String(age))}</p>
      )}

      {!token && !totpSecret && ownerStatus?.owner_exists === false && (
        <>
          <form className="card narrow" onSubmit={setup}>
            <h2>{text("setup")}</h2>
            <label>{text("displayName")}<input required value={displayName} onChange={(event) => setDisplayName(event.target.value)} /></label>
            <label>{text("password")}<input required minLength={12} type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
            <button disabled={recovering}>{text("setup")}</button>
          </form>
          <form className="card narrow" onSubmit={recoverBackup}>
            <h2>{text("recover")}</h2>
            <p>{text("recoveryHint")}</p>
            <label>{text("backupFile")}<input required name="recoveryFile" type="file" accept=".llbackup,text/plain" /></label>
            <label>{text("backupPassword")}<input required minLength={12} type="password" value={backupPassword} onChange={(event) => setBackupPassword(event.target.value)} /></label>
            <button disabled={recovering}>{text("recover")}</button>
          </form>
        </>
      )}

      {!token && !totpSecret && ownerStatus?.owner_exists && !ownerStatus.owner_confirmed && (
        <form className="card narrow" onSubmit={resumeSetup}>
          <h2>{text("resumeSetup")}</h2>
          <label>{text("password")}<input required type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
          <button>{text("resumeSetup")}</button>
        </form>
      )}

      {!token && totpSecret && (
        <form className="card narrow" onSubmit={confirmSetup}>
          <h2>{text("confirm")}</h2>
          <p>{text("totpSetup")}</p>
          {totpUri && <QRCodeSVG value={totpUri} size={200} title={text("totpQr")} />}
          <code className="secret">{totpSecret}</code>
          <label>{text("totp")}<input required inputMode="numeric" pattern="[0-9]{6}" value={totp} onChange={(event) => setTotp(event.target.value)} /></label>
          <button>{text("confirm")}</button>
        </form>
      )}

      {!token && !totpSecret && ownerStatus?.owner_confirmed && (
        <form className="card narrow" onSubmit={unlock}>
          <h2>{text("unlock")}</h2>
          <label>{text("password")}<input required type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
          <label>{text("totp")}<input required inputMode="numeric" pattern="[0-9]{6}" value={totp} onChange={(event) => setTotp(event.target.value)} /></label>
          <button>{text("unlock")}</button>
        </form>
      )}

      {token && (
        <>
          <section className="card">
            <h2>{text("patient")}</h2>
            <form className="inline-form" onSubmit={addPatient}>
              <label>{text("patientName")}<input required value={patientName} onChange={(event) => setPatientName(event.target.value)} /></label>
              <button>{text("addPatient")}</button>
            </form>
            <label>{text("patient")}
              <select value={selectedPatient} onChange={(event) => setSelectedPatient(event.target.value)}>
                <option value="" />
                {patients.map((patient) => (
                  <option key={patient.id} value={patient.id}>
                    {String((patient.name as Array<{ text?: string }> | undefined)?.[0]?.text ?? patient.id)}
                  </option>
                ))}
              </select>
            </label>
          </section>

          {selectedPatient && (
            <div className="columns">
              <section className="card">
                <h2>{text("document")}</h2>
                <form onSubmit={addDocument}>
                  <label>{text("documentTitle")}<input required value={documentTitle} onChange={(event) => setDocumentTitle(event.target.value)} /></label>
                  <label>{text("document")}<input required type="file" accept=".pdf,.png,.txt,application/pdf,image/png,text/plain" onChange={(event) => setDocumentFile(event.target.files?.[0])} /></label>
                  <small>{text("unsupportedFile")}</small>
                  <button>{text("addDocument")}</button>
                </form>
              </section>
              <section className="card">
                <h2>{text("medication")}</h2>
                <form onSubmit={addMedication}>
                  <label>{text("medicationName")}<input required value={medicationName} onChange={(event) => setMedicationName(event.target.value)} /></label>
                  <button>{text("addMedication")}</button>
                </form>
              </section>
            </div>
          )}

          <section className="card">
            <h2>{text("timeline")}</h2>
            {timeline.length === 0 && <p>{text("empty")}</p>}
            <ol className="timeline">
              {timeline.map((entry) => (
                <li key={entry.resource.id}>
                  <time>{new Date(entry.occurred_at).toLocaleString(locale)}</time>
                  <strong>{entry.resource_type}</strong>
                  <span>{entry.resource_type === "Patient"
                    ? String((entry.resource.name as Array<{ text?: string }> | undefined)?.[0]?.text ?? "")
                    : entry.resource_type === "MedicationStatement"
                      ? String((entry.resource.medicationCodeableConcept as { text?: string }).text ?? "")
                      : String((entry.resource.content as Array<{ attachment: { title: string } }>)[0]?.attachment.title ?? "")}
                  </span>
                </li>
              ))}
            </ol>
          </section>

          <section className="card">
            <h2>Backup</h2>
            {backupHistory && backupHistory.length > 0 && !historyError && (
              <>
                <h3>{text("backupHistory")}</h3>
                <p>{text("backupHistoryHint")}</p>
                <ol>
                  {backupHistory.map((entry, index) => (
                    <li key={`${entry.saved_at}-${index}`}>
                      <time>{new Date(entry.saved_at).toLocaleString(locale)}</time>{" — "}{entry.path}
                    </li>
                  ))}
                </ol>
              </>
            )}
            <div className="actions">
              <form onSubmit={createBackup}>
                <label>{text("backupPassword")}<input required minLength={12} type="password" value={backupPassword} onChange={(event) => setBackupPassword(event.target.value)} /></label>
                <button disabled={savingBackup || replacementBusy}>{text("backup")}</button>
              </form>
              {!replacementBackup && <form onSubmit={(event) => restoreBackup(event, (event.currentTarget.elements.namedItem("backup") as HTMLInputElement).files?.[0])}>
                <label>{text("backupFile")}<input required name="backup" type="file" accept=".llbackup,text/plain" /></label>
                <label>{text("backupPassword")}<input required minLength={12} type="password" value={restorePassword} onChange={(event) => setRestorePassword(event.target.value)} /></label>
                <button disabled={replacementBusy || savingBackup}>{text("restore")}</button>
              </form>}
            </div>
            {backupStatus && <p role="status">{backupStatus}</p>}
            {backupError && <p className="error" role="alert">{backupError}</p>}
            {replacementBackup && <form onSubmit={replaceBackup}>
              <p className="warning" role="note">{text("replacementWarning")}</p>
              <p>{text("replacementBackupHint")}</p>
              <label>{text("currentPassword")}<input required type="password" value={replacementPassword} onChange={(event) => setReplacementPassword(event.target.value)} /></label>
              <label>{text("freshTotp")}<input required inputMode="numeric" pattern="[0-9]{6}" value={replacementCode} onChange={(event) => setReplacementCode(event.target.value)} /></label>
              <label><span><input required type="checkbox" checked={replacementConfirmed} onChange={(event) => setReplacementConfirmed(event.target.checked)} /> {text("replacementConfirm")}</span></label>
              <div className="actions">
                <button disabled={replacementBusy || savingBackup || !replacementConfirmed}>{text("replacementAction")}</button>
                <button type="button" className="secondary" disabled={replacementBusy} onClick={() => { setReplacementBackup(""); setReplacementPassword(""); setReplacementCode(""); setBackupError(""); }}>{text("cancel")}</button>
              </div>
            </form>}
          </section>
        </>
      )}
    </main>
  );
}
