"""Checks the catalog: every plugin and publisher file is valid. Run: python tools/check.py"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
CATEGORIES = {"code", "assist", "know", "tickets", "product", "community"}
TRUST = {"content", "web", "code"}
STATUS = {"planned", "listed"}


def main() -> int:
    errors: list[str] = []
    publishers = {}
    for f in sorted((ROOT / "publishers").glob("*.yml")):
        p = yaml.safe_load(f.read_text()) or {}
        if p.get("name") != f.stem or not ID.match(str(p.get("name"))):
            errors.append(f"{f.name}: name must be the file name and a valid id")
        if not isinstance(p.get("keys"), list) or not all(str(k).startswith("ed25519:") for k in p["keys"]):
            errors.append(f"{f.name}: keys must be a list of ed25519:<public key>")
        publishers[f.stem] = p
    for f in sorted((ROOT / "plugins").glob("*.yml")):
        p = yaml.safe_load(f.read_text()) or {}
        name = str(p.get("name"))
        if name != f.stem or not ID.match(name):
            errors.append(f"{f.name}: name must be the file name and a valid id")
        if p.get("publisher") not in publishers:
            errors.append(f"{f.name}: publisher {p.get('publisher')!r} has no file in publishers/")
        if not str(p.get("repo", "")).startswith("https://github.com/"):
            errors.append(f"{f.name}: repo must be a https://github.com/ URL")
        if p.get("category") not in CATEGORIES:
            errors.append(f"{f.name}: category must be one of {sorted(CATEGORIES)}")
        if p.get("trust") not in TRUST:
            errors.append(f"{f.name}: trust must be one of {sorted(TRUST)}")
        if p.get("status") not in STATUS:
            errors.append(f"{f.name}: status must be one of {sorted(STATUS)}")
        for key in ("title", "summary"):
            if not str(p.get(key) or "").strip():
                errors.append(f"{f.name}: {key} is missing")
    revoked = yaml.safe_load((ROOT / "revoked.yml").read_text()) or {}
    if not isinstance(revoked.get("revoked"), list):
        errors.append("revoked.yml: revoked must be a list")
    for e in errors:
        print("error:", e)
    print(f"{len(publishers)} publishers, {len(list((ROOT / 'plugins').glob('*.yml')))} plugins, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
