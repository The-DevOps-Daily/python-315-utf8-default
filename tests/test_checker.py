import ast
import contextlib
import io
import sys
import tempfile
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

    def test_exit_status(self):
        with tempfile.TemporaryDirectory() as folder:
            clean = Path(folder, "clean.py")
            clean.write_text('open("a", encoding="utf-8")\n', encoding="utf-8")
            broken = Path(folder, "broken.py")
            broken.write_text("def (:\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(check_default_encoding.main([str(clean)]), 0)
                self.assertEqual(check_default_encoding.main([str(broken)]), 2)
                self.assertEqual(check_default_encoding.main([str(FIXTURE)]), 1)


if __name__ == "__main__":
    unittest.main()
