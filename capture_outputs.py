"""Capture API exchanges and benchmark all examples."""

import csv
import json
import runpy
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXAMPLES = {
    "chat_completion.py": "Say test passed.",
    "response.py": "Say test passed.",
    "decision_predicate.py": "I was charged twice for one order.",
    "decision_choice.py": "I cannot sign in to my account.",
    "decision_score.py": "Checkout fails for every customer with no workaround.",
}
SENSITIVE_HEADERS = {"authorization", "proxy-authorization", "cookie", "set-cookie", "x-api-key"}


def safe_headers(headers) -> dict[str, str]:
    return {
        name: "[REDACTED]" if name.lower() in SENSITIVE_HEADERS else value
        for name, value in headers.items()
    }


def json_body(body) -> object:
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    return json.loads(body) if isinstance(body, str) else body


def output_path(folder: str, filename: str, iteration: int | None = None) -> Path:
    stem = Path(filename).stem
    if iteration is None:
        return ROOT / "output" / folder / f"{stem}.json"
    return ROOT / "output" / "iterations" / folder / stem / f"{iteration:02}.json"


def save_exchange(
    folder: str, filename: str, request, response, elapsed_ms: float,
    iteration: int | None = None,
) -> None:
    output = output_path(folder, filename, iteration)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "response_time_ms": round(elapsed_ms, 3),
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": safe_headers(request.headers),
                    "payload": json_body(request.content if folder != "requests" else request.body),
                },
                "response": {
                    "status_code": response.status_code,
                    "headers": safe_headers(response.headers),
                    "payload": (
                        response.http_response.json()
                        if hasattr(response, "http_response")
                        else response.json()
                    ),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


class SDKProxy:
    """Use the SDK's raw response view, then return its normal parsed object."""

    def __init__(self, target, folder: str, filename: str, iteration: int | None):
        self.target = target
        self.folder = folder
        self.filename = filename
        self.iteration = iteration

    def __getattr__(self, name):
        if name == "create":
            def create(*args, **kwargs):
                started = time.perf_counter()
                raw = self.target.with_raw_response.create(*args, **kwargs)
                elapsed_ms = (time.perf_counter() - started) * 1000
                save_exchange(
                    self.folder, self.filename, raw.http_response.request, raw,
                    elapsed_ms, self.iteration,
                )
                return raw.parse()

            return create
        return SDKProxy(getattr(self.target, name), self.folder, self.filename, self.iteration)


def run_child(folder: str, filename: str, prompt: str, iteration: int | None = None) -> None:
    sys.path.insert(0, str(ROOT / folder))
    import common

    if folder == "sdk":
        original_client = common.client
        common.client = lambda: SDKProxy(original_client(), folder, filename, iteration)
    elif folder == "httpx":
        import httpx

        original_post = httpx.Client.post

        def post(client, *args, **kwargs):
            started = time.perf_counter()
            response = original_post(client, *args, **kwargs)
            elapsed_ms = (time.perf_counter() - started) * 1000
            save_exchange(folder, filename, response.request, response, elapsed_ms, iteration)
            return response

        httpx.Client.post = post
    elif folder == "requests":
        import requests

        original_post = requests.post

        def post(*args, **kwargs):
            started = time.perf_counter()
            response = original_post(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - started) * 1000
            save_exchange(folder, filename, response.request, response, elapsed_ms, iteration)
            return response

        requests.post = post
    else:
        raise ValueError(folder)

    sys.argv = [str(ROOT / folder / filename), prompt]
    runpy.run_path(sys.argv[0], run_name="__main__")


def run_all() -> None:
    for folder in ("sdk", "httpx", "requests"):
        for filename, prompt in EXAMPLES.items():
            command = [sys.executable, __file__, "--child", folder, filename, prompt]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            label = f"{folder}/{filename}"
            if result.returncode:
                raise RuntimeError(f"{label} failed:\n{result.stderr}")
            output = output_path(folder, filename)
            exchange = json.loads(output.read_text())
            exchange["example_stdout"] = result.stdout.strip()
            output.write_text(json.dumps(exchange, indent=2, ensure_ascii=False) + "\n")
            print(f"Saved {output.relative_to(ROOT)} (HTTP {exchange['response']['status_code']})")


def run_benchmark() -> None:
    rows = []
    started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for iteration in range(1, 11):
        for folder in ("sdk", "httpx", "requests"):
            for filename, prompt in EXAMPLES.items():
                command = [
                    sys.executable, __file__, "--child", folder, filename, prompt,
                    str(iteration),
                ]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
                label = f"{folder}/{filename} run {iteration}"
                if result.returncode:
                    raise RuntimeError(f"{label} failed:\n{result.stderr}")
                output = output_path(folder, filename, iteration)
                exchange = json.loads(output.read_text())
                exchange["example_stdout"] = result.stdout.strip()
                output.write_text(json.dumps(exchange, indent=2, ensure_ascii=False) + "\n")
                rows.append({
                    "client": folder,
                    "example": filename,
                    "iteration": iteration,
                    "response_time_ms": exchange["response_time_ms"],
                    "status_code": exchange["response"]["status_code"],
                    "exchange_file": str(output.relative_to(ROOT)),
                })
        print(f"Completed iteration {iteration}/10 (15 calls)", flush=True)

    csv_path = ROOT / "output" / "response_times.csv"
    with csv_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# API response times",
        "",
        f"Measured {started_at} (UTC). Ten sequential runs per example, 150 calls total."
        " Timing starts immediately before the client call and ends when the HTTP response"
        " returns. It includes connection setup and network time, but excludes Python"
        " process startup, JSON parsing, and file writing. Each run uses a fresh process.",
        "",
        "All times are milliseconds. Individual exchanges are in [`iterations/`](iterations/);"
        " machine-readable timings are in [`response_times.csv`](response_times.csv).",
        "",
        "| Client | Example | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Mean | Median | Min | Max |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for folder in ("sdk", "httpx", "requests"):
        for filename in EXAMPLES:
            times = [
                row["response_time_ms"] for row in rows
                if row["client"] == folder and row["example"] == filename
            ]
            values = [*times, statistics.mean(times), statistics.median(times), min(times), max(times)]
            lines.append(
                f"| {folder} | {filename} | "
                + " | ".join(f"{value:.1f}" for value in values)
                + " |"
            )
    (ROOT / "output" / "response_times.md").write_text("\n".join(lines) + "\n")
    print("Saved output/response_times.csv and output/response_times.md", flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 6 and sys.argv[1] == "--child":
        run_child(*sys.argv[2:5], iteration=int(sys.argv[5]))
    elif len(sys.argv) == 5 and sys.argv[1] == "--child":
        run_child(*sys.argv[2:])
    elif sys.argv[1:] == ["--benchmark"]:
        run_benchmark()
    elif len(sys.argv) == 1:
        run_all()
    else:
        raise SystemExit("Usage: python capture_outputs.py [--benchmark]")
