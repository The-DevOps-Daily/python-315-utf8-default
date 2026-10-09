#!/usr/bin/env python3
"""Find calls that use Python's default text encoding.

These are the calls whose behaviour depends on the locale before Python 3.15,
and on UTF-8 mode from 3.15. Each finding is a place to add encoding="utf-8"
(or encoding="locale", if the file really is in the locale encoding).

    python3 check_default_encoding.py src/ scripts/deploy.py

Exit status is 1 when anything is found, and 2 when nothing is found but some
files could not be parsed (run it with the interpreter your code targets).

This is a static check, so it misses calls made through a variable
(f = open; f(path)), wrappers in your own code, Path objects it cannot see
(a Path returned by another function), and calls whose **kwargs it cannot
read. Run your tests with -X warn_default_encoding as well; that catches what
this misses.
"""
import ast
import sys
from pathlib import Path

SUBPROCESS_TEXT = {"run", "Popen", "call", "check_call", "check_output"}
SUBPROCESS_ALWAYS = {"getoutput", "getstatusoutput"}
# handler name -> position of encoding in its positional arguments
LOGGING_HANDLERS = {"FileHandler": 2, "WatchedFileHandler": 2, "RotatingFileHandler": 4,
                    "TimedRotatingFileHandler": 4}
# compressed-file openers: text only with "t" in the mode
COMPRESSED_OPEN = {"gzip.open": 3, "bz2.open": 3, "lzma.open": None}
# tempfile class -> (position of mode, position of encoding)
TEMPFILE_TEXT = {"TemporaryFile": (0, 2), "NamedTemporaryFile": (0, 2),
                 "SpooledTemporaryFile": (1, 3)}
PATH_CLASSES = {"Path", "PosixPath", "WindowsPath"}
# Path methods that return another Path
PATH_METHODS = {"joinpath", "with_name", "with_stem", "with_suffix", "resolve", "absolute",
                "expanduser", "relative_to"}


def keyword(call, name):
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def is_none(node):
    return isinstance(node, ast.Constant) and node.value is None


def has_encoding(call, position):
    """True if a non-None encoding is given as a keyword or at positional `position`.

    A **mapping that is a dict literal is read; any other **mapping might carry
    an encoding, so it counts as given (a known blind spot, see the docstring)."""
    node = keyword(call, "encoding")
    if node is not None:
        return not is_none(node)
    for kw in call.keywords:
        if kw.arg is None:
            if not isinstance(kw.value, ast.Dict):
                return True
            for key, value in zip(kw.value.keys, kw.value.values):
                if key is None:  # {**other}: cannot tell
                    return True
                if isinstance(key, ast.Constant) and key.value == "encoding":
                    return not is_none(value)
    if position is not None and len(call.args) > position:
        return not is_none(call.args[position])
    return False


def mode_of(call, position, default):
    """The mode string if it is a literal, None if it cannot be known statically."""
    node = keyword(call, "mode")
    if node is None and len(call.args) > position:
        node = call.args[position]
    if node is None:
        return default
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def truthy_literal(node):
    return isinstance(node, ast.Constant) and bool(node.value)


class Finder(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.modules = {}  # local name -> module, from "import x" and "import x as y"
        self.names = {}    # local name -> "module.attr", from "from x import y"
        self.path_vars = set()  # names assigned a Path or annotated as one (module-wide)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname:
                self.modules[alias.asname] = alias.name
            else:
                top = alias.name.split(".")[0]
                self.modules[top] = top
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if node.module:
                self.names[alias.asname or alias.name] = f"{node.module}.{alias.name}"
        self.generic_visit(node)

    def visit_Assign(self, node):
        if self.is_path_expr(node.value):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.path_vars.add(target.id)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name) and (
                self.is_path_annotation(node.annotation)
                or (node.value is not None and self.is_path_expr(node.value))):
            self.path_vars.add(node.target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        args = node.args
        for arg in [*args.posonlyargs, *args.args, *args.kwonlyargs]:
            if arg.annotation is not None and self.is_path_annotation(arg.annotation):
                self.path_vars.add(arg.arg)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def is_path_annotation(self, node):
        name = self.qualified(node) if isinstance(node, (ast.Name, ast.Attribute)) else None
        return bool(name) and name.rsplit(".", 1)[-1] in PATH_CLASSES

    def is_path_expr(self, node):
        if isinstance(node, ast.Name):
            return node.id in self.path_vars
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return self.is_path_expr(node.left)
        if isinstance(node, ast.Attribute) and node.attr == "parent":
            return self.is_path_expr(node.value)
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in PATH_METHODS:
                return self.is_path_expr(func.value)
            name = self.qualified(func)
            return bool(name) and name.rsplit(".", 1)[-1] in PATH_CLASSES
        return False

    def qualified(self, func):
        """Return "module.attr" for a call target, or the bare builtin name."""
        if isinstance(func, ast.Name):
            return self.names.get(func.id, func.id)
        parts = []
        node = func
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if not isinstance(node, ast.Name) or not parts:
            return None
        root = self.modules.get(node.id) or self.names.get(node.id)
        if root is None:
            return None
        return ".".join([root, *reversed(parts)])

    def add(self, node, message):
        self.findings.append((node.lineno, node.col_offset + 1, message))

    def visit_Call(self, node):
        self.check(node)
        self.generic_visit(node)

    def check(self, node):
        name = self.qualified(node.func)
        func = node.func

        if name in ("open", "io.open", "builtins.open", "codecs.open"):
            mode = mode_of(node, 1, "r")
            position = 3 if name != "codecs.open" else 2
            if mode is not None and "b" in mode:
                return
            if not has_encoding(node, position):
                suffix = "" if mode is not None else " (mode is not a literal)"
                self.add(node, f"{name}() without encoding{suffix}")
            return

        if name in COMPRESSED_OPEN:
            mode = mode_of(node, 1, "rb")
            if (mode is None or "t" in mode) and not has_encoding(node, COMPRESSED_OPEN[name]):
                self.add(node, f"{name}() in text mode without encoding")
            return

        if name == "locale.getpreferredencoding":
            self.add(node, "locale.getpreferredencoding() returns 'utf-8' in UTF-8 mode; "
                           "use locale.getencoding() for the locale encoding")
            return

        if name == "os.fdopen":
            mode = mode_of(node, 1, "r")
            if (mode is None or "b" not in mode) and not has_encoding(node, 3):
                self.add(node, "os.fdopen() without encoding")
            return

        if name == "io.TextIOWrapper":
            if not has_encoding(node, 1):
                self.add(node, "io.TextIOWrapper() without encoding")
            return

        if name == "os.popen":
            self.add(node, "os.popen() always decodes with the default encoding")
            return

        if name and name.startswith("subprocess."):
            attr = name.split(".", 1)[1]
            if attr in SUBPROCESS_ALWAYS:
                self.add(node, f"subprocess.{attr}() always decodes with the default encoding")
                return
            if attr in SUBPROCESS_TEXT:
                text = keyword(node, "text") or keyword(node, "universal_newlines")
                errors = keyword(node, "errors")
                text_mode = (text is not None and truthy_literal(text)) or \
                    (errors is not None and not is_none(errors))
                if text_mode and not has_encoding(node, None):
                    self.add(node, f"subprocess.{attr}() in text mode without encoding")
            return

        if name and (name.startswith("logging.") or name.startswith("logging.handlers.")):
            attr = name.rsplit(".", 1)[1]
            if attr in LOGGING_HANDLERS and not has_encoding(node, LOGGING_HANDLERS[attr]):
                self.add(node, f"logging {attr} without encoding")
            if attr == "basicConfig" and keyword(node, "filename") is not None \
                    and not has_encoding(node, None):
                self.add(node, "logging.basicConfig(filename=...) without encoding")
            return

        if name and name.startswith("tempfile."):
            attr = name.split(".", 1)[1]
            if attr in TEMPFILE_TEXT:
                mode_pos, enc_pos = TEMPFILE_TEXT[attr]
                mode = mode_of(node, mode_pos, "w+b")
                if mode is not None and "b" not in mode and not has_encoding(node, enc_pos):
                    self.add(node, f"tempfile.{attr}(mode={mode!r}) without encoding")
            return

        if isinstance(func, ast.Attribute):
            if func.attr == "read_text" and not has_encoding(node, 0):
                self.add(node, ".read_text() without encoding")
            elif func.attr == "write_text" and not has_encoding(node, 1):
                self.add(node, ".write_text() without encoding")
            elif func.attr == "open" and self.is_path_expr(func.value):
                mode = mode_of(node, 0, "r")
                if (mode is None or "b" not in mode) and not has_encoding(node, 2):
                    self.add(node, "Path.open() without encoding")


def python_files(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*.py")
                              if not any(part in (".venv", "venv", ".git", "node_modules",
                                                  "site-packages", "__pycache__")
                                         for part in p.parts))
        elif path.suffix == ".py" or path.is_file():
            yield path


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    total = 0
    skipped = 0
    for path in python_files(argv):
        try:
            tree = ast.parse(path.read_bytes(), filename=str(path))
        except (SyntaxError, ValueError) as exc:
            print(f"{path}: skipped, cannot parse: {exc}", file=sys.stderr)
            skipped += 1
            continue
        finder = Finder()
        finder.visit(tree)
        for line, col, message in sorted(finder.findings):
            print(f"{path}:{line}:{col}: {message}")
        total += len(finder.findings)
    sys.stdout.flush()
    print(f"{total} call(s) use the default encoding"
          + (f", {skipped} file(s) skipped" if skipped else ""), file=sys.stderr)
    if total:
        return 1
    return 2 if skipped else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
