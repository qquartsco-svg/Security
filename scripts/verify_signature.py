from __future__ import annotations

import hashlib
from pathlib import Path
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    signature_path = root / "SIGNATURE.sha256"
    if not signature_path.exists():
        print("SIGNATURE.sha256 not found")
        return 1

    failed = False
    checked = 0
    for line in signature_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            expected, rel = line.split("  ", 1)
        except ValueError:
            print(f"Malformed signature line: {line}")
            failed = True
            continue
        path = root / rel
        if not path.exists():
            print(f"MISSING  {rel}")
            failed = True
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            print(f"FAIL     {rel}")
            failed = True
        else:
            print(f"OK       {rel}")
        checked += 1

    print(f"Checked {checked} entries")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
