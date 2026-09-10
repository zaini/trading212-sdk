"""Post-generation patches for the TypeScript SDK.

Fern's `next_path` pagination has two problems with Trading 212's `nextPagePath`:

1. It builds the next URL with `core.url.join(baseUrl, nextPagePath)`, which puts
   the whole value into `URL.pathname`, so the `?` is encoded as `%3F` and every
   page after the first requests the wrong URL.
2. It only treats null/"" as the last page, but Trading 212 has also returned a
   bare query string (`limit=5&cursor=...`) and `"null&ticker=..."`.

Both are routed through the hand-written src/nextPage.ts instead.
"""

from __future__ import annotations

import re
import sys

from overrides import ROOT, operations

RESOURCES = ROOT / "sdks" / "typescript" / "src" / "api" / "resources"
IMPORT = 'import { hasNextPage, resolveNextPageUrl } from "../../../../nextPage.js";\n'

PAGE_BLOCK = re.compile(
    r'(?P<head>"GET",\s*"(?P<path>/api/[^"]+)",\s*\);\s*\},\s*\);\s*'
    r"const dataWithRawResponse = await initialRequest\(\)\.withRawResponse\(\);.*?)"
    r'hasNextPage: \(response\) => response\?\.nextPagePath != null && response\?\.nextPagePath !== "",'
    r"(?P<mid>.*?)"
    r"return list\(core\.url\.join\(_baseUrl, response\?\.nextPagePath!\)\);",
    re.S,
)


def main() -> None:
    expected: dict[str, int] = {}
    for op in operations():
        if op.paginated:
            expected[op.group] = expected.get(op.group, 0) + 1

    total = 0
    for group, count in expected.items():
        path = RESOURCES / group / "client" / "Client.ts"
        source = path.read_text()
        if IMPORT in source:
            continue  # already patched
        source, found = PAGE_BLOCK.subn(
            lambda m: (
                f"{m['head']}hasNextPage: (response) => hasNextPage(response?.nextPagePath),{m['mid']}"
                f'return list(resolveNextPageUrl(_baseUrl, response!.nextPagePath!, "{m["path"]}"));'
            ),
            source,
        )
        if found != count:
            sys.exit(f"{path}: expected {count} paginated methods to patch, found {found}")
        first_import = source.index("import ")
        path.write_text(source[:first_import] + IMPORT + source[first_import:])
        total += found

    print(f"postprocess_typescript: patched {total} paginated methods")


if __name__ == "__main__":
    main()
