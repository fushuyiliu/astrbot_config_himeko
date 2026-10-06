"""Report public-configuration findings without printing matching content.

Usage:
    python tools/audit_public_config_repo.py .
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


RULES = {
    "private_key_material": re.compile(r"-----BEGIN(?: [A-Z]+)? PRIVATE KEY-----", re.I),
    "cloud_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "model_or_api_secret": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    "absolute_user_or_drive_path": re.compile(r"(?i)(?:[a-z]:\\|/(?:home|users)/)"),
    "private_adapter_or_personal_root": re.compile(
        r"weixin_oc_user_id|wechat-private|个人分身|Obsidian"
    ),
    "raw_ipv4_address": re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
}
FORBIDDEN_NAMES = re.compile(
    r"(?i)^(?:cmd_config\.json|.*_config\.json|\.env(?:\..*)?|.*\.(?:pem|key|crt|pfx))$"
)
ALLOWED_EXAMPLE_NAMES = {"astrbot_plugin_himeko.config.example.json"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    findings: set[tuple[str, str]] = set()
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        if relative == "tools/audit_public_config_repo.py":
            continue
        if FORBIDDEN_NAMES.fullmatch(path.name) and path.name not in ALLOWED_EXAMPLE_NAMES:
            findings.add(("forbidden_filename", relative))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.add(("non_utf8_text_file", relative))
            continue
        for category, pattern in RULES.items():
            if pattern.search(text):
                findings.add((category, relative))
    print(f"public-config-tree: {len(findings)} finding(s)")
    for category, relative in sorted(findings):
        print(f"{category} | {relative}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
