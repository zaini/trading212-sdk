"""Post-generation patches for the Python SDK.

Fern's Python generator does not emit anything for deprecated endpoints
(only the TypeScript generator adds `@deprecated`). This inserts a
`warnings.warn(..., DeprecationWarning)` call at the top of every deprecated
method, in both the sync and async clients. The list of deprecated methods is
read from fern/overrides.yml, so there is a single source of truth.
"""

from __future__ import annotations

import ast
import sys
from collections import defaultdict

from overrides import ROOT, operations, snake_case

PACKAGE_DIR = ROOT / "sdks" / "python" / "src" / "t212"
MARKER = "# t212: deprecation warning"


def patch_file(group: str, methods: dict[str, str]) -> int:
    path = PACKAGE_DIR / group / "client.py"
    source = path.read_text()
    if MARKER in source:
        return 0
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)

    inserts: list[tuple[int, str]] = []
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef) or cls.name.startswith("Raw") or cls.name.startswith("AsyncRaw"):
            continue
        for fn in cls.body:
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or fn.name not in methods:
                continue
            body = fn.body
            # Insert after the docstring, if there is one.
            first = body[1] if isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) else body[0]
            indent = " " * first.col_offset
            message = f"{cls.name.removeprefix('Async')[:-len('Client')].lower()}.{fn.name} is deprecated. {methods[fn.name]}"
            inserts.append(
                (
                    first.lineno - 1,
                    f"{indent}warnings.warn({message!r}, DeprecationWarning, stacklevel=2)  {MARKER}\n",
                )
            )

    expected = 2 * len(methods)  # sync + async client
    if len(inserts) != expected:
        sys.exit(f"{path}: expected {expected} deprecated methods, found {len(inserts)}")

    for lineno, text in sorted(inserts, reverse=True):
        lines.insert(lineno, text)

    # Add `import warnings` after the generated header comment.
    import_at = next(i for i, line in enumerate(lines) if line.startswith(("import ", "from ")))
    lines.insert(import_at, "import warnings\n")
    path.write_text("".join(lines))
    return len(inserts)


def main() -> None:
    by_group: dict[str, dict[str, str]] = defaultdict(dict)
    for op in operations():
        if op.deprecated and op.group and op.sdk_method:
            by_group[op.group][snake_case(op.sdk_method)] = op.deprecation_message or ""
    total = sum(patch_file(group, methods) for group, methods in by_group.items())
    print(f"postprocess_python: added {total} deprecation warnings")


if __name__ == "__main__":
    main()
