#!/usr/bin/env python3
"""Simple HTTP API for triggering MkDocs rebuilds."""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

BUILD_COMMAND = ["/etc/cont-init.d/10-build-mkdocs"]


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class BuildState:
    running: bool = False
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    last_exit_code: Optional[int] = None
    last_success: Optional[bool] = None
    last_message: str = "No rebuild triggered yet"
    last_output_tail: str = ""


class RebuildController:
    def __init__(self) -> None:
        self._state = BuildState()
        self._lock = threading.Lock()

    def snapshot(self) -> BuildState:
        with self._lock:
            return BuildState(**asdict(self._state))

    def trigger(self) -> tuple[bool, str]:
        with self._lock:
            if self._state.running:
                return False, "Rebuild already in progress"

            self._state.running = True
            self._state.started_at = iso_now()
            self._state.finished_at = None
            self._state.last_message = "Rebuild started"

        thread = threading.Thread(target=self._run_build, daemon=True)
        thread.start()
        return True, "Rebuild started"

    def _run_build(self) -> None:
        lines: list[str] = []
        exit_code = 1

        try:
            print("[rebuild-api] Running build command: /etc/cont-init.d/10-build-mkdocs", flush=True)
            process = subprocess.Popen(
                BUILD_COMMAND,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            assert process.stdout is not None
            for line in process.stdout:
                line = line.rstrip("\n")
                print(f"[rebuild-api][build] {line}", flush=True)
                lines.append(line)

            exit_code = process.wait()
        except Exception as exc:  # pragma: no cover
            lines.append(f"Internal error: {exc}")
            print(f"[rebuild-api] Build process failed: {exc}", flush=True)

        tail = "\n".join(lines[-200:])
        success = exit_code == 0
        message = "Rebuild finished successfully" if success else "Rebuild failed"

        with self._lock:
            self._state.running = False
            self._state.finished_at = iso_now()
            self._state.last_exit_code = exit_code
            self._state.last_success = success
            self._state.last_message = message
            self._state.last_output_tail = tail


class RebuildHandler(BaseHTTPRequestHandler):
    controller: RebuildController

    server_version = "MkDocsRebuildAPI/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[rebuild-api][http] {self.address_string()} - {fmt % args}", flush=True)

    def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_text(self, payload: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _consume_body(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 0:
            self.rfile.read(length)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_text("healthy\n")
            return

        if self.path == "/status":
            state = asdict(self.controller.snapshot())
            self._send_json({"ok": True, "status": state})
            return

        self._send_json({"ok": False, "error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        self._consume_body()

        if self.path in ("/rebuild", "/webhook"):
            triggered, message = self.controller.trigger()
            status = HTTPStatus.ACCEPTED if triggered else HTTPStatus.CONFLICT
            state = asdict(self.controller.snapshot())
            self._send_json(
                {
                    "ok": triggered,
                    "message": message,
                    "status": state,
                },
                status,
            )
            return

        self._send_json({"ok": False, "error": "Not found"}, HTTPStatus.NOT_FOUND)


def main() -> None:
    parser = argparse.ArgumentParser(description="MkDocs rebuild API server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8083)
    args = parser.parse_args()

    controller = RebuildController()
    RebuildHandler.controller = controller

    server = ThreadingHTTPServer((args.host, args.port), RebuildHandler)
    print(f"[rebuild-api] Listening on {args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
