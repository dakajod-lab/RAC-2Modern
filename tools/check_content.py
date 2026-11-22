#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Checks the repository against CONTENT_POLICY.md.

    python3 tools/check_content.py [ROOT]

Reads the files git tracks, and the new ones it does not ignore. Outside a git checkout it reads
every file under ROOT except .git, .sdk, build, dist and private. It prints one line per problem
and exits with 1 if there is any:

- a disc image, game file or archive, found by its extension or by a PS2 serial name such as
  SCES_516.07;
- a file larger than MAX_BYTES;
- a picture, model or sound with no row in ASSETS.tsv, or with a row whose origin is not
  original or procedural, or whose author, license or source is empty;
- a row of ASSETS.tsv that names a file that is missing, appears twice, or names a source file
  that is missing.

Standard library only.
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

MAX_BYTES = 25 * 1024 * 1024

# Disc images, the PS2's own file types, and archives (a release's archives are built by CI, not
# committed).
FORBIDDEN = {
    ".iso", ".chd", ".cso", ".zso", ".gz", ".img", ".mdf", ".mds", ".nrg", ".cue", ".ecm",
    ".bin", ".elf", ".irx", ".wad", ".vag", ".vb", ".pss",
    ".ps2", ".mcd", ".mc2", ".psu", ".max", ".sav",
    ".zip", ".7z", ".rar", ".tar",
}
SERIAL = re.compile(r"^S[CL][EUPK][SMD]_\d{3}\.\d{2}$", re.IGNORECASE)
FORBIDDEN_NAMES = {"system.cnf"}

# Files that need a row in ASSETS.tsv.
ASSET_TYPES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".tga", ".dds", ".ktx2", ".exr", ".hdr", ".svg",
    ".glb", ".gltf", ".fbx", ".obj", ".blend",
    ".wav", ".ogg", ".flac", ".mp3",
}
ORIGINS = {"original", "procedural"}
HEADER = ["path", "origin", "author", "license", "source"]
SKIP_DIRS = {".git", ".sdk", "build", "dist", "private", "__pycache__"}


def repository_files(root: Path) -> list[str]:
    """The repository's files as POSIX paths from root: git's tracked and new files, else a walk."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            check=True, capture_output=True,
        ).stdout.decode("utf-8")
        return sorted({p for p in out.split("\0") if p and (root / p).is_file()})
    except (OSError, subprocess.CalledProcessError):
        found = []
        for p in root.rglob("*"):
            rel = p.relative_to(root)
            if p.is_file() and not any(part in SKIP_DIRS for part in rel.parts):
                found.append(rel.as_posix())
        return sorted(found)


def read_assets(root: Path, problems: list[str]) -> dict[str, dict[str, str]]:
    """ASSETS.tsv's rows by path; what is wrong with the file itself goes into problems."""
    table = root / "ASSETS.tsv"
    if not table.is_file():
        problems.append("ASSETS.tsv: missing (CONTENT_POLICY.md, Provenance)")
        return {}
    rows: dict[str, dict[str, str]] = {}
    with table.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        if header != HEADER:
            problems.append(f"ASSETS.tsv: the first line must be {chr(9).join(HEADER)!r}")
            return {}
        for number, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) != len(HEADER):
                problems.append(f"ASSETS.tsv:{number}: {len(row)} columns, not {len(HEADER)}")
                continue
            entry = dict(zip(HEADER, (cell.strip() for cell in row)))
            path = entry["path"]
            if path in rows:
                problems.append(f"ASSETS.tsv:{number}: {path} is listed twice")
                continue
            rows[path] = entry | {"line": str(number)}
    return rows


def looks_like_path(text: str) -> bool:
    """A source that names a file of this repository rather than describing how it was made."""
    return " " not in text and PurePosixPath(text).suffix != ""


def check(root: Path, files: list[str]) -> list[str]:
    """Every problem, one line each; empty when the repository keeps the policy."""
    problems: list[str] = []
    rows = read_assets(root, problems)
    present = set(files)
    for rel in files:
        path = PurePosixPath(rel)
        suffix = path.suffix.lower()
        if suffix in FORBIDDEN or SERIAL.match(path.name) or path.name.lower() in FORBIDDEN_NAMES:
            problems.append(f"{rel}: a disc image, game file or archive cannot be committed")
        size = (root / rel).stat().st_size
        if size > MAX_BYTES:
            problems.append(f"{rel}: {size / 1024 / 1024:.1f} MB, more than {MAX_BYTES // 1024 // 1024} MB")
        if suffix in ASSET_TYPES:
            entry = rows.get(rel)
            if entry is None:
                problems.append(f"{rel}: no row in ASSETS.tsv")
                continue
            where = f"ASSETS.tsv:{entry['line']}"
            if entry["origin"] not in ORIGINS:
                problems.append(f"{where}: {rel}: origin {entry['origin']!r} is not original or procedural")
            for column in ("author", "license", "source"):
                if not entry[column]:
                    problems.append(f"{where}: {rel}: {column} is empty")
            source = entry["source"]
            if source and looks_like_path(source) and source not in present:
                problems.append(f"{where}: {rel}: its source {source} is not in the repository")
    for rel, entry in rows.items():
        if rel not in present:
            problems.append(f"ASSETS.tsv:{entry['line']}: {rel} is not in the repository")
    return problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    files = repository_files(root)
    problems = check(root, files)
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problem(s): see CONTENT_POLICY.md", file=sys.stderr)
        return 1
    print(f"check_content: {len(files)} files, no problems")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
