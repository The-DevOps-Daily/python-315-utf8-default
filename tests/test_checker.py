import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import check_default_encoding  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "sample.py"


class CheckerTest(unittest.TestCase):
    def test_reports_exactly_the_marked_lines(self):
        lines = FIXTURE.read_text(encoding="utf-8").splitlines()
        expected = {n for n, line in enumerate(lines, 1) if line.endswith("# expect")}
        finder = check_default_encoding.Finder()
        finder.visit(ast.parse(FIXTURE.read_bytes()))
        found = {line for line, _col, _msg in finder.findings}
        self.assertEqual(sorted(found - expected), [], "reported but not marked")
        self.assertEqual(sorted(expected - found), [], "marked but not reported")
        self.assertEqual(len(finder.findings), len(found), "one finding per line")


if __name__ == "__main__":
    unittest.main()
