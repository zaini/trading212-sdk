"""Post-generation patches for the TypeScript SDK.

Fern's `next_path` pagination builds the next page URL with
`core.url.join(baseUrl, nextPagePath)`, which assigns the whole value to
`URL.pathname`. Trading 212's `nextPagePath` includes a query string
(`/api/v0/equity/history/orders?limit=2&cursor=123`), so the `?` gets encoded
as `%3F` and every page after the first requests the wrong URL.

This swaps it for standard URL resolution, which keeps the query string intact.
Remove once fixed upstream in fern-api/fern.
"""

from __future__ import annotations

import sys

from overrides import ROOT, operations

RESOURCES = ROOT / "sdks" / "typescript" / "src" / "api" / "resources"
BROKEN = "list(core.url.join(_baseUrl, response?.nextPagePath!))"
FIXED = "list(new URL(response?.nextPagePath!, _baseUrl).toString())"


def main() -> None:
    expected: dict[str, int] = {}
    for op in operations():
        if op.paginated:
            expected[op.group] = expected.get(op.group, 0) + 1

    total = 0
    for group, count in expected.items():
        path = RESOURCES / group / "client" / "Client.ts"
        source = path.read_text()
        found = source.count(BROKEN)
        if found == 0 and source.count(FIXED) == count:
            continue  # already patched
        if found != count:
            sys.exit(f"{path}: expected {count} occurrences of the next-page URL join, found {found}")
        path.write_text(source.replace(BROKEN, FIXED))
        total += found
    print(f"postprocess_typescript: patched {total} next-page URLs")


if __name__ == "__main__":
    main()
