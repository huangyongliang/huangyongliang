#!/usr/bin/env python3
"""Drop the email row text from generated profile-details cards.

vn7n24fzkq/github-profile-summary-cards@release has no input that hides
the address or skips this card. It draws GitHub's public profile email
as a <text> node whenever that field is set. Remove those nodes so a
later scheduled run does not commit the address. Other detail rows
(contributions, repos, joined, company, location) are left in place.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "profile-summary-card-output"

# A profile-details value that is only an email address.
EMAIL_TEXT = re.compile(
    r"<text\b[^>]*>[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}</text>"
)
# Fallback if the address uses characters outside the pattern above.
ANY_AT_TEXT = re.compile(r"<text\b[^>]*>[^<]*@[^<]*</text>")


def strip_email_text(svg: str, path: Path) -> str:
    updated, _ = EMAIL_TEXT.subn("", svg)
    if "@" in updated:
        updated, _ = ANY_AT_TEXT.subn("", updated)
    if "@" in updated:
        sys.exit(f"{path}: '@' remains after removing email text; refusing to keep this card")
    return updated


def main() -> None:
    files = sorted(ROOT.glob("*/0-profile-details.svg"))
    if not files:
        sys.exit(f"no profile-details cards under {ROOT}")
    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        updated = strip_email_text(original, path)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"stripped email text from {changed} of {len(files)} profile-details card(s)")


if __name__ == "__main__":
    main()
