#!/usr/bin/env python3
"""Check external links in Markdown and llms.txt without making CI flaky."""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import re
import socket
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s<>\]\[()]+")
TRAILING_PUNCTUATION = ".,;:!?\"'”’"
HARD_FAILURES = {400, 404, 410}
SOFT_STATUSES = {401, 403, 408, 425, 429}
USER_AGENT = "BensariKnowledgeLinkChecker/1.0 (+https://github.com/tombensariworkshop-web/woodworking-knowledge)"


def source_files() -> list[Path]:
    return sorted(ROOT.rglob("*.md")) + [ROOT / "llms.txt"]


def links_by_source() -> dict[str, list[str]]:
    links: defaultdict[str, list[str]] = defaultdict(list)
    for path in source_files():
        if not path.exists():
            continue
        rel = path.relative_to(ROOT).as_posix()
        for match in URL_RE.findall(path.read_text(encoding="utf-8")):
            url = match.rstrip(TRAILING_PUNCTUATION)
            links[url].append(rel)
    return dict(links)


def request(url: str, method: str, timeout: float) -> int:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"}
    if method == "GET":
        headers["Range"] = "bytes=0-1023"
    req = Request(url, headers=headers, method=method)
    with urlopen(req, timeout=timeout) as response:
        return int(response.status)


def check(url: str, timeout: float, retries: int) -> tuple[str, str]:
    last_detail = "unknown error"
    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            try:
                status = request(url, method, timeout)
                return "ok", str(status)
            except HTTPError as exc:
                status = int(exc.code)
                last_detail = f"HTTP {status}"
                if status in HARD_FAILURES:
                    return "failed", last_detail
                if status in SOFT_STATUSES:
                    return "warning", last_detail
                if method == "HEAD" and status in {405, 501}:
                    continue
                if 500 <= status < 600:
                    break
                return "warning", last_detail
            except (URLError, TimeoutError, socket.timeout) as exc:
                last_detail = str(getattr(exc, "reason", exc))
                break
        if attempt < retries:
            time.sleep(1.5 * (attempt + 1))
    return "warning", last_detail


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    links = links_by_source()
    failures: list[str] = []
    warnings: list[str] = []
    successes: list[str] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        pending = {
            executor.submit(check, url, args.timeout, args.retries): (url, sources)
            for url, sources in links.items()
        }
        for future in as_completed(pending):
            url, sources = pending[future]
            result, detail = future.result()
            where = ", ".join(sorted(set(sources)))
            if result == "failed":
                failures.append(f"{url} — {detail} — {where}")
            elif result == "warning":
                warnings.append(f"{url} — {detail} — {where}")
            else:
                successes.append(f"OK {detail} {url}")

    for item in sorted(successes):
        print(item)
    for item in sorted(warnings):
        print(f"WARNING {item}")
    for item in sorted(failures):
        print(f"FAILED {item}")

    print(
        f"Checked {len(links)} unique external links: "
        f"{len(failures)} hard failures, {len(warnings)} warnings."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
