"""Canonical external path identifiers for scale-sol-luna-goals."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse


SEGMENT = re.compile(r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$")
DNS_HOST = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)
LOCAL_HASH = re.compile(r"^[0-9a-f]{12}$")


def fail(message: str) -> None:
    raise ValueError(message)


def canonical_repository_id(value: str) -> str:
    """Validate and return one canonical repository identifier."""
    if value != value.strip() or "\x00" in value or "\\" in value:
        fail("repository_id contains invalid whitespace or path characters")
    if "://" in value or value.startswith("/") or value.endswith("/"):
        fail("repository_id must be a slash-separated identifier, not a URL or path")
    parts = value.split("/")
    if len(parts) != 3 or any(not SEGMENT.fullmatch(part) for part in parts):
        fail(
            "repository_id must be lowercase host/owner/repository or "
            "local/repository/path-hash"
        )
    if value != value.lower():
        fail("repository_id must be lowercase")
    if parts[0] == "local":
        if not LOCAL_HASH.fullmatch(parts[2]):
            fail("local repository_id must end with a 12-character lowercase SHA-256 prefix")
    elif not DNS_HOST.fullmatch(parts[0]):
        fail("hosted repository_id must begin with a DNS host name")
    if parts[2].endswith(".git"):
        fail("repository_id must omit the .git suffix")
    return value


def canonical_record_id(value: str, field: str) -> str:
    """Validate one lowercase, path-safe goal or invocation identifier."""
    if value != value.strip() or not SEGMENT.fullmatch(value) or value != value.lower():
        fail(f"{field} must be one lowercase path-safe segment")
    return value


def repository_id_from_remote(remote_url: str) -> str:
    """Convert a Git transport URL into canonical host/owner/repository form."""
    remote_url = remote_url.strip()
    if not remote_url:
        fail("remote URL is empty")

    if "://" in remote_url:
        parsed = urlparse(remote_url)
        host = parsed.hostname
        path = parsed.path
    else:
        match = re.fullmatch(r"(?:[^@/:]+@)?([^/:]+):(.+)", remote_url)
        if match is None:
            fail("remote URL must use a supported URL or SCP-style Git form")
        host, path = match.groups()

    path_parts = [part for part in path.strip("/").split("/") if part]
    if host is None or len(path_parts) != 2:
        fail("remote URL must identify exactly one owner and repository")
    repository = path_parts[1]
    if repository.endswith(".git"):
        repository = repository[:-4]
    return canonical_repository_id(f"{host}/{path_parts[0]}/{repository}".lower())


def local_repository_id(repository_root: Path) -> str:
    """Build the documented fallback for a repository without a canonical remote."""
    root = repository_root.expanduser().resolve()
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    common_dir = Path(result.stdout.strip()).resolve()
    digest = hashlib.sha256(str(common_dir).encode()).hexdigest()[:12]
    repository = re.sub(r"[^a-z0-9._-]+", "-", root.name.lower()).strip("-._")
    if not repository:
        fail("could not derive a local repository name")
    return canonical_repository_id(f"local/{repository}/{digest}")
