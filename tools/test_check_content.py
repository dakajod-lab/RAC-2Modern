# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests of check_content.py, on small repositories made in a temporary folder.

    python3 -m unittest discover -s tools -p 'test_*.py'
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_content  # noqa: E402

HEADER = "path\torigin\tauthor\tlicense\tsource\n"


class Repository:
    """A temporary folder of files, and check_content's verdict on it."""

    def __init__(self, files: dict[str, bytes | str]):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for name, data in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(data, str):
                path.write_text(data, encoding="utf-8")
            else:
                path.write_bytes(data)

    def problems(self) -> list[str]:
        files = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file())
        return check_content.check(self.root, files)

    def close(self) -> None:
        self._tmp.cleanup()


class CheckContent(unittest.TestCase):
    def verdict(self, files: dict[str, bytes | str]) -> list[str]:
        repo = Repository(files)
        self.addCleanup(repo.close)
        return repo.problems()

    def test_clean_repository(self):
        self.assertEqual(self.verdict({"ASSETS.tsv": HEADER, "README.md": "hello"}), [])

    def test_asset_with_its_row(self):
        files = {
            "ASSETS.tsv": HEADER + "mod/assets/level_00/textures/a.png\tprocedural\tme\tGPL-3.0-or-later\ttools/make.py\n",
            "mod/assets/level_00/textures/a.png": b"\x89PNG",
            "tools/make.py": "print(1)",
        }
        self.assertEqual(self.verdict(files), [])

    def test_described_source(self):
        files = {
            "ASSETS.tsv": HEADER + "a.png\toriginal\tme\tGPL-3.0-or-later\tpainted by hand in Krita\n",
            "a.png": b"\x89PNG",
        }
        self.assertEqual(self.verdict(files), [])

    def test_disc_files_refused(self):
        for name in ("game.iso", "disc.CHD", "SCES_516.07", "sces_516.07", "SYSTEM.CNF", "level.wad",
                     "mod.zip", "data.bin"):
            with self.subTest(name=name):
                problems = self.verdict({"ASSETS.tsv": HEADER, f"private-ish/{name}": b"x"})
                self.assertEqual(len(problems), 1, problems)
                self.assertIn("cannot be committed", problems[0])

    def test_serial_like_names_only(self):
        self.assertEqual(self.verdict({"ASSETS.tsv": HEADER, "notes/SCES.md": "about serials"}), [])

    def test_asset_without_row(self):
        problems = self.verdict({"ASSETS.tsv": HEADER, "mod/assets/x.glb": b"glTF"})
        self.assertEqual(problems, ["mod/assets/x.glb: no row in ASSETS.tsv"])

    def test_bad_origin_and_empty_columns(self):
        files = {"ASSETS.tsv": HEADER + "x.png\tripped\t\tGPL-3.0-or-later\tx\n", "x.png": b"p"}
        problems = self.verdict(files)
        self.assertTrue(any("origin 'ripped'" in p for p in problems), problems)
        self.assertTrue(any("author is empty" in p for p in problems), problems)

    def test_missing_source_file(self):
        files = {"ASSETS.tsv": HEADER + "x.png\tprocedural\tme\tGPL-3.0-or-later\ttools/gone.py\n", "x.png": b"p"}
        self.assertEqual(self.verdict(files), [
            "ASSETS.tsv:2: x.png: its source tools/gone.py is not in the repository"])

    def test_stale_and_duplicate_rows(self):
        row = "x.png\toriginal\tme\tGPL-3.0-or-later\tby hand\n"
        problems = self.verdict({"ASSETS.tsv": HEADER + row + row + "gone.png\toriginal\tme\tGPL\tby hand\n",
                                 "x.png": b"p"})
        self.assertIn("ASSETS.tsv:3: x.png is listed twice", problems)
        self.assertIn("ASSETS.tsv:4: gone.png is not in the repository", problems)

    def test_wrong_header(self):
        problems = self.verdict({"ASSETS.tsv": "file\twhere\n"})
        self.assertEqual(len(problems), 1)
        self.assertIn("first line", problems[0])

    def test_missing_table(self):
        self.assertEqual(self.verdict({"README.md": "hi"}),
                         ["ASSETS.tsv: missing (CONTENT_POLICY.md, Provenance)"])

    def test_large_file(self):
        big = b"0" * (check_content.MAX_BYTES + 1)
        problems = self.verdict({"ASSETS.tsv": HEADER, "notes.txt": big})
        self.assertEqual(len(problems), 1)
        self.assertIn("more than 25 MB", problems[0])


if __name__ == "__main__":
    unittest.main()
