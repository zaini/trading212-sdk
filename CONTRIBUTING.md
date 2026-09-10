# Contributing

Thanks for helping. Bug reports, API quirks, spec updates, helpers, and docs fixes are all welcome.

## Reporting a problem

[Open an issue](https://github.com/zaini/trading212-sdk/issues) with:

- the SDK (`@azaini/t212-sdk` on npm or `t212-sdk` on PyPI) and its version
- the call you made, and what you expected
- the response or error, with your API key and secret removed
- whether it happened on `Demo` or `Live`

If the API itself behaves differently from its docs, that's useful too. It usually ends up in
[docs/api-gotchas.md](docs/api-gotchas.md) and, where we can, as a fix in the SDK.

## Making a change

Most code under `sdks/typescript/src` and `sdks/python/src/t212` is generated and is overwritten every time
`scripts/generate.sh` runs. **Don't edit generated files directly.** Put the change in one of these instead:

| To change | Edit |
| --- | --- |
| Method or group names, pagination, retries, deprecation | `fern/overrides.yml` |
| Auth, generator versions, generator options | `fern/generators.yml` |
| Generated code Fern gets wrong | a patch in `scripts/postprocess_typescript.py` or `scripts/postprocess_python.py`, with a test |
| A helper or other hand-written module | a new file under `src/`, listed in that folder's `.fernignore` |
| Packaging, READMEs, tests | `sdks/*/package.json`, `pyproject.toml`, `README.md`, `tests/`, which are never generated |

[docs/how-it-works.md](docs/how-it-works.md) explains the existing overrides and patches, and
[docs/maintaining.md](docs/maintaining.md) covers spec updates and generator upgrades.

## Before opening a pull request

```sh
scripts/generate.sh                           # needs Docker
uv run --project sdks/python pytest tests     # spec coverage and overrides
(cd sdks/python && uv run pytest)
(cd sdks/typescript && npm ci && npm run typecheck && npm test)
```

Commit the regenerated code along with your change; CI checks that they match. New behaviour needs a test in
both SDKs where it applies. Live tests are optional for contributors: they need a Trading 212 demo account
and skip without credentials.

Keep pull requests focused, and describe what changed and why.
