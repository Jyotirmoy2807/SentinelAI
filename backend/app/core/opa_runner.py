import logging
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_opa_process: subprocess.Popen | None = None


def start_opa_server(opa_cli_path: str = "opa", bundle_path: str = "./app/policies/rego", port: int = 8181) -> None:
    global _opa_process
    executable = shutil.which(opa_cli_path) or (opa_cli_path if Path(opa_cli_path).exists() else None)
    if not executable:
        logger.warning("OPA CLI executable '%s' not found on PATH. Automatic OPA server management skipped.", opa_cli_path)
        return

    policy_dir = Path(bundle_path)
    policy_dir.mkdir(parents=True, exist_ok=True)

    if _opa_process and _opa_process.poll() is None:
        logger.info("OPA server is already running (PID: %s).", _opa_process.pid)
        return

    cmd = [executable, "run", "--server", f"--addr=localhost:{port}", str(policy_dir)]
    try:
        _opa_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("Started OPA server process (PID: %s) serving %s on port %s", _opa_process.pid, policy_dir, port)
    except Exception as exc:
        logger.error("Failed to start OPA server: %s", exc)


def stop_opa_server() -> None:
    global _opa_process
    if _opa_process and _opa_process.poll() is None:
        logger.info("Stopping OPA server (PID: %s)...", _opa_process.pid)
        _opa_process.terminate()
        try:
            _opa_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _opa_process.kill()
        _opa_process = None


def restart_opa_server(opa_cli_path: str = "opa", bundle_path: str = "./app/policies/rego", port: int = 8181) -> None:
    logger.info("Restarting OPA server to enforce newly deployed Rego policies...")
    stop_opa_server()
    start_opa_server(opa_cli_path=opa_cli_path, bundle_path=bundle_path, port=port)
