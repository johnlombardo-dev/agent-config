#!/usr/bin/env python3
"""Resolve the canonical scale-sol-luna-goals repository identifier."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from path_conventions import local_repository_id, repository_id_from_remote


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print canonical host/owner/repository identity for SSLG persistence."
    )
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--remote", default="origin")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.repository_root.expanduser().resolve()
    remote = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", args.remote],
        capture_output=True,
        text=True,
    )
    if remote.returncode == 0 and remote.stdout.strip():
        try:
            print(repository_id_from_remote(remote.stdout))
        except ValueError as error:
            raise SystemExit(str(error)) from error
        return
    try:
        print(local_repository_id(root))
    except (ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
