# How the SDKs are built

```
openapi/api.yaml          Trading 212's spec, untouched
        +
fern/overrides.yml        our changes: names, pagination, deprecation, environments
fern/generators.yml       generator versions, auth, output paths
        │
        ▼  scripts/generate.sh  (Fern's open-source generators, run locally in Docker)
        │
        ├─ sdks/typescript/src    generated ─┐
        └─ sdks/python/src/t212   generated ─┤ + post-processing patches (scripts/postprocess_*.py)
                                             │ + hand-written files (.fernignore)
                                             ▼
                              package.json / pyproject.toml (ours) → npm / PyPI
```

Everything runs locally with the Apache-2.0 [Fern](https://github.com/fern-api/fern) generators.
No Fern account, token or paid plan is used. Updating the spec, upgrading Fern and releasing are covered in
[maintaining.md](maintaining.md).

## What we change, and why

### Method names (`fern/overrides.yml`)

Upstream `operationId`s are inconsistent (`orders_1`, `placeStopOrder_1` for the *stop-limit* endpoint,
`getAll`), so every operation gets an explicit group and method name. Names are written once in
camelCase; Fern converts them per language (`placeStopLimit` in TypeScript, `place_stop_limit` in Python).
The full table is in [naming-map.md](naming-map.md), generated from the overrides file.

### Auth (`fern/generators.yml`)

The spec defines two schemes: Basic auth (API key + secret) and a legacy raw `Authorization` header key.
Every operation lists both **in one security requirement**, which in OpenAPI means *both* are required.
Trading 212 actually accepts either. We define a single `KeyAndSecret` Basic scheme in `generators.yml`,
which exposes `apiKey` / `apiSecret` (`api_key` / `api_secret` in Python) and falls back to the
`T212_API_KEY` / `T212_API_SECRET` environment variables. The legacy header is not exposed.

### Environments

`x-fern-server-name` names the two servers `Demo` and `Live`. **Demo is the default** in both SDKs, so
forgetting to set it can never place a real-money trade.

### Pagination

History endpoints return `{ items, nextPagePath }`, where `nextPagePath` is a path plus query string
(`/api/v0/equity/history/orders?limit=50&cursor=1760346100000`). `x-fern-pagination.next_path` maps this directly.

Trading 212 has also returned other forms: a bare query string (`limit=5&cursor=...`), and
`"null&ticker=..."` on the last page. Both SDKs handle all of these (see [api-gotchas.md](api-gotchas.md)).

- **TypeScript:** methods return an async-iterable `Page`. Fern's generated code encoded the `?` in
  `nextPagePath` as `%3F`, breaking every page after the first, and only recognised `null`/`""` as the end.
  `scripts/postprocess_typescript.py` routes both through the hand-written `src/nextPage.ts`.
- **Python:** when you generate locally, Fern only enables pagination for accounts with the paid
  pagination feature. We ship a hand-written `t212/pagination.py` (`paginate`, `apaginate`, and page
  variants) that requests `nextPagePath`'s query string verbatim, and stops if the API ever repeats a page.

### Retries

The generated clients retry 408, 429 and 5xx with backoff, waiting for `x-ratelimit-reset` / `Retry-After`
when present. Placing an order is not idempotent, though: a timed-out request may still have executed. So
`x-fern-retries: { disabled: true }` turns retries off for every POST (orders, export requests, pie writes).

### Deprecated Pies endpoints

Kept, and marked with `x-fern-availability: deprecated`. TypeScript gets `@deprecated` JSDoc (strikethrough
in editors). Fern's Python generator does not emit deprecation markers, so `scripts/postprocess_python.py`
inserts `warnings.warn(..., DeprecationWarning)` into each deprecated method. The list of deprecated
methods is read from the overrides file.

### Package files

Fern only generates `package.json` / `pyproject.toml` / README on its Enterprise plan. When you generate
locally you get source files only. We maintain the package files ourselves, outside the generated folders.

## Custom code

Files listed in a `.fernignore` inside a generated folder survive regeneration
(e.g. `sdks/python/src/t212/.fernignore`). Anything else in `src/` is overwritten.

## Tests

| Suite | Where | Needs credentials |
| --- | --- | --- |
| Spec coverage and overrides applied | `tests/test_spec_coverage.py` | no |
| TypeScript unit (mocked HTTP) | `sdks/typescript/tests/client.test.ts` | no |
| Python unit (mocked HTTP) | `sdks/python/tests/test_client.py` | no |
| Live, read-only, demo account | `sdks/*/tests/live*` | yes |

Live tests skip when `T212_API_KEY` / `T212_API_SECRET` are unset. They only ever use the demo server,
never place orders, and space out requests to respect Trading 212's per-endpoint rate limits. The Python
live suite also warns when the API returns fields the spec doesn't document (spec drift).

## Adding another language

Only TypeScript and Python are maintained here, but Fern has generators for Go, Java, C#, PHP, Ruby,
Swift and Rust. To try one, add a group to `fern/generators.yml`:

```yaml
  go:
    generators:
      - name: fernapi/fern-go-sdk
        version: 1.58.0 # check Docker Hub for the latest
        output:
          location: local-file-system
          path: ../sdks/go
        config:
          module:
            path: github.com/<owner>/<repo>/sdks/go
```

Then run `npx fern-api generate --local --group go`. The overrides (names, auth, environments) apply
automatically. Notes:

- You'll need to write the language's package files yourself.
- As of mid-2026, Fern's Go and C# generators emit `next_path` endpoints as plain single-page methods.
- Check each generator's config options in Fern's docs. Unknown options can make a generator exit
  silently without writing anything; `scripts/generate.sh` catches this with an empty-output check.
