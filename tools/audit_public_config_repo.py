"""Report public-configuration findings without printing matching content.

Usage:
    python tools/audit_public_config_repo.py .
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

RULES = {
    "private_key_material": re.compile(
        r"-----BEGIN(?: [A-Z]+)? PRIVATE KEY-----", re.IGNORECASE
    ),
    "cloud_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "model_or_api_secret": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    "credential_assignment": re.compile(
        r"(?i)(?:[\"']?(?:api[_ -]?key|access[_ -]?key|secret|token|password)[\"']?)\s*[:=]\s*"
        r"[\"']?(?!<|\$\{|YOUR_|REPLACE_|example|changeme)[^\s\"']{8,}"
    ),
    "absolute_user_or_drive_path": re.compile(r"(?i)(?:[a-z]:\\|/(?:home|users)/)"),
    "private_adapter_or_personal_root": re.compile(
        r"weixin_oc_user_id|wechat-private|个人分身|Obsidian"
    ),
    "raw_ipv4_address": re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
}
FORBIDDEN_NAMES = re.compile(
    r"(?i)^(?:cmd_config\.json|.*_config\.json|\.env(?:\..*)?|id_rsa|"
    r"local\.settings\.json|.*\.(?:pem|key|crt|pfx))$"
)
ALLOWED_EXAMPLE_NAMES = {"astrbot_plugin_himeko.config.example.json"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".toml"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv"}
AUDITOR_RELATIVE_PATH = "tools/audit_public_config_repo.py"


def categories_in_text(text: str) -> set[str]:
    return {category for category, pattern in RULES.items() if pattern.search(text)}


def config_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.relative_to(root).as_posix() == AUDITOR_RELATIVE_PATH:
            continue
        yield path


def scan_tree(root: Path) -> list[tuple[str, str]]:
    findings: set[tuple[str, str]] = set()
    for path in config_files(root):
        relative = path.relative_to(root).as_posix()
        if (
            FORBIDDEN_NAMES.fullmatch(path.name)
            and path.name not in ALLOWED_EXAMPLE_NAMES
        ):
            findings.add(("forbidden_filename", relative))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.add(("non_utf8_text_file", relative))
            continue
        for category in categories_in_text(text):
            findings.add((category, relative))
    return sorted(findings)


def git_output(repo: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def scan_history(repo: Path) -> list[tuple[str, str, str]]:
    """Scan reachable history without exposing any matching content."""
    findings: set[tuple[str, str, str]] = set()
    commits = [
        value for value in git_output(repo, ["rev-list", "--all"]).splitlines() if value
    ]
    for commit in commits:
        for path in git_output(
            repo, ["ls-tree", "-r", "--name-only", commit]
        ).splitlines():
            if path == AUDITOR_RELATIVE_PATH:
                continue
            if (
                FORBIDDEN_NAMES.fullmatch(Path(path).name)
                and Path(path).name not in ALLOWED_EXAMPLE_NAMES
            ):
                findings.add(("forbidden_filename", commit[:12], path))
            if Path(path).suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = git_output(repo, ["show", f"{commit}:{path}"])
            except subprocess.CalledProcessError:
                continue
            for category in categories_in_text(text):
                findings.add((category, commit[:12], path))
    return sorted(findings)


def print_findings(title: str, findings: list[tuple[str, ...]]) -> None:
    print(f"{title}: {len(findings)} finding(s)")
    for finding in findings:
        print(" | ".join(finding))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--history", type=Path, help="Optional Git repository to scan")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("root must be an existing directory")
    tree_findings = scan_tree(root)
    print_findings("public-config-tree", tree_findings)
    history_findings: list[tuple[str, str, str]] = []
    if args.history:
        history = args.history.resolve()
        try:
            history_findings = scan_history(history)
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"history-scan-error: {type(exc).__name__}", file=sys.stderr)
            return 2
        print_findings("public-config-history", history_findings)
    return 1 if tree_findings or history_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
