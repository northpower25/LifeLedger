#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use rcgen::generate_simple_self_signed;
use reqwest::blocking::Client;
use reqwest::Certificate;
use serde::{Deserialize, Serialize};
use std::io::{Error, ErrorKind, Write};
use std::net::TcpListener;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::thread;
use std::time::{Duration, Instant};
use tauri::{Manager, RunEvent, State};

struct ApiState {
    base_url: String,
    ipc_secret: String,
    client: Client,
    child: Mutex<Child>,
}

#[derive(Serialize)]
struct SidecarBootstrap {
    ipc_secret: String,
    certificate_pem: String,
    private_key_pem: String,
}

#[derive(Deserialize)]
struct ApiRequest {
    method: String,
    path: String,
    body: Option<String>,
    authorization: Option<String>,
}

#[derive(Serialize)]
struct ApiReply {
    status: u16,
    body: String,
}

fn target_sidecar_name() -> Result<String, String> {
    let target = match (std::env::consts::OS, std::env::consts::ARCH) {
        ("windows", "x86_64") => "x86_64-pc-windows-msvc",
        ("windows", "aarch64") => "aarch64-pc-windows-msvc",
        ("linux", "x86_64") => "x86_64-unknown-linux-gnu",
        ("macos", "aarch64") => "aarch64-apple-darwin",
        ("macos", "x86_64") => "x86_64-apple-darwin",
        _ => return Err("unsupported_sidecar_platform".into()),
    };
    let suffix = if std::env::consts::OS == "windows" {
        ".exe"
    } else {
        ""
    };
    Ok(format!("lifeledger-api-{target}{suffix}"))
}

fn start_api(app: &tauri::App) -> Result<ApiState, Box<dyn std::error::Error>> {
    let port_listener = TcpListener::bind(("127.0.0.1", 0))?;
    let port = port_listener.local_addr()?.port();
    drop(port_listener);

    let resource_dir = app.path().resource_dir()?;
    let sidecar_name =
        target_sidecar_name().map_err(|message| Error::new(ErrorKind::Unsupported, message))?;
    let candidates = [
        std::env::var_os("LIFELEDGER_API_BIN").map(PathBuf::from),
        Some(resource_dir.join(&sidecar_name)),
        Some(resource_dir.join("binaries").join(&sidecar_name)),
        std::env::current_exe()
            .ok()
            .and_then(|path| path.parent().map(|directory| directory.join(&sidecar_name))),
    ];
    let sidecar = candidates
        .into_iter()
        .flatten()
        .find(|path| path.is_file())
        .ok_or_else(|| {
            Error::new(
                ErrorKind::NotFound,
                format!("local_api_binary_missing: {sidecar_name}"),
            )
        })?;

    let mut random = [0u8; 32];
    getrandom::getrandom(&mut random)?;
    let ipc_secret = random
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect::<String>();
    let tls = generate_simple_self_signed(vec!["127.0.0.1".to_string()])?;
    let certificate_pem = tls.cert.pem();
    let private_key_pem = tls.signing_key.serialize_pem();
    let bootstrap = serde_json::to_vec(&SidecarBootstrap {
        ipc_secret: ipc_secret.clone(),
        certificate_pem: certificate_pem.clone(),
        private_key_pem,
    })?;
    let mut child = Command::new(sidecar)
        .args(["--port", &port.to_string(), "--ipc-stdin"])
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::inherit())
        .spawn()?;
    let mut child_stdin = child
        .stdin
        .take()
        .ok_or_else(|| Error::new(ErrorKind::BrokenPipe, "local_api_stdin_unavailable"))?;
    child_stdin.write_all(&bootstrap)?;
    child_stdin.write_all(b"\n")?;
    drop(child_stdin);

    let base_url = format!("https://127.0.0.1:{port}");
    let pinned_certificate = Certificate::from_pem(certificate_pem.as_bytes())?;
    let client = Client::builder()
        .no_proxy()
        .add_root_certificate(pinned_certificate)
        .timeout(Duration::from_millis(500))
        .build()?;
    let deadline = Instant::now() + Duration::from_secs(15);
    loop {
        let ready = client
            .get(format!("{base_url}/api/v1/health"))
            .header("X-LifeLedger-IPC", &ipc_secret)
            .send()
            .and_then(|response| response.json::<serde_json::Value>())
            .is_ok_and(|body| {
                body["status"] == "ok" && body["pid"].as_u64() == Some(u64::from(child.id()))
            });
        if ready && child.try_wait()?.is_none() {
            break;
        }
        if Instant::now() >= deadline {
            let _ = child.kill();
            return Err("local_api_start_timeout".into());
        }
        if child.try_wait()?.is_some() {
            return Err("local_api_process_exited".into());
        }
        thread::sleep(Duration::from_millis(100));
    }
    Ok(ApiState {
        base_url,
        ipc_secret,
        client,
        child: Mutex::new(child),
    })
}

#[tauri::command]
fn api_request(request: ApiRequest, state: State<'_, ApiState>) -> Result<ApiReply, String> {
    if !request.path.starts_with("/api/v1/")
        || request.path.starts_with("//")
        || request.path.contains("..")
        || request.path.contains('?')
    {
        return Err("api_path_not_allowed".into());
    }
    let method = reqwest::Method::from_bytes(request.method.as_bytes())
        .map_err(|_| "api_method_not_allowed")?;
    if method != reqwest::Method::GET && method != reqwest::Method::POST {
        return Err("api_method_not_allowed".into());
    }
    let mut call = state
        .client
        .request(method, format!("{}{}", state.base_url, request.path))
        .header("X-LifeLedger-IPC", &state.ipc_secret);
    if let Some(authorization) = request.authorization {
        if !authorization.starts_with("Bearer ")
            || authorization.bytes().any(|byte| byte.is_ascii_control())
        {
            return Err("authorization_header_invalid".into());
        }
        call = call.header("Authorization", authorization);
    }
    if let Some(body) = request.body {
        call = call.header("Content-Type", "application/json").body(body);
    }
    let response = call.send().map_err(|_| "local_api_unavailable")?;
    let status = response.status().as_u16();
    let body = response.text().map_err(|_| "local_api_response_invalid")?;
    Ok(ApiReply { status, body })
}

fn main() {
    let app = tauri::Builder::default()
        .setup(|app| {
            let state = start_api(app)?;
            app.manage(state);
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![api_request])
        .build(tauri::generate_context!())
        .expect("LifeLedger desktop host failed to start");
    app.run(|handle, event| {
        if matches!(event, RunEvent::Exit) {
            if let Some(state) = handle.try_state::<ApiState>() {
                if let Ok(mut child) = state.child.lock() {
                    let _ = child.kill();
                }
            }
        }
    });
}
