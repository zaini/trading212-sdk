# Maintaining

How to update the SDKs when Trading 212 changes the API, upgrade the generators, and release.

Requirements: Docker, Node 18+, Python 3.9+ with PyYAML, [uv](https://docs.astral.sh/uv/), and the GitHub CLI.

## Updating the API spec

1. Download the latest spec from [docs.trading212.com/api](https://docs.trading212.com/api) ("Download OpenAPI
   description") and replace `openapi/api.yaml` and `openapi/api.json`. Don't edit these files by hand;
   all our changes live in `fern/overrides.yml`.
2. Regenerate and run the checks:
   ```sh
   scripts/generate.sh
   uv run --project sdks/python pytest tests
   ```
3. Fix whatever `tests/test_spec_coverage.py` reports:
   - **New operation**: add an entry to `fern/overrides.yml` with `x-fern-sdk-group-name` and
     `x-fern-sdk-method-name` (camelCase). Add `x-fern-retries: { disabled: true }` if it's a POST, and
     `x-fern-pagination` if it returns `nextPagePath`. Then regenerate.
   - **Removed or moved operation**: delete its stale override.
   - **Deprecated upstream**: add `x-fern-availability: { status: deprecated, message: ... }`.
4. Run the SDK tests (`uv run pytest` in `sdks/python`, `npm test` in `sdks/typescript`) and read the diff
   in `sdks/`. Type changes show up there first.
5. Commit the spec, overrides, generated code and `docs/naming-map.md` together. CI fails if the generated
   code doesn't match what `scripts/generate.sh` produces.

Anything you learn about API behaviour that the spec doesn't describe goes in [api-gotchas.md](api-gotchas.md).

## Upgrading Fern

Versions are pinned in two places:

- the CLI: `version` in `fern/fern.config.json`
- the generators: `version` under each generator in `fern/generators.yml`

Check for new releases on Docker Hub ([fern-typescript-sdk](https://hub.docker.com/r/fernapi/fern-typescript-sdk/tags),
[fern-python-sdk](https://hub.docker.com/r/fernapi/fern-python-sdk/tags)) and in the changelogs in
[fern-api/fern](https://github.com/fern-api/fern) under `generators/<language>/sdk/`.

After bumping, run `scripts/generate.sh`. Watch for:

- **A patch script failing.** `scripts/postprocess_typescript.py` and `postprocess_python.py` exit with an
  error if the generated code no longer has the shape they expect. Either Fern fixed the underlying problem
  (then delete the patch and its test assertions) or the patch needs updating.
- **Empty output.** A generator given a config option it doesn't recognise can exit without writing
  anything while the CLI still reports success. `scripts/generate.sh` checks for this.
- **Python pagination.** If Fern stops gating `next_path` pagination for local generation,
  `t212/pagination.py` can be replaced by the generated pager.

## Releasing

Both packages are released together, with the same version number:

| Registry | Package | Published from |
| --- | --- | --- |
| npm | `@azaini/t212-sdk` | `sdks/typescript` |
| PyPI | `t212-sdk` (imports as `t212`) | `sdks/python` |

1. Pick the version, following [semver](https://semver.org). While we're on 0.x, a breaking change (renamed
   method, removed endpoint, changed type) bumps the minor version; anything else bumps the patch version.
2. Set `version` in `sdks/typescript/package.json` and `sdks/python/pyproject.toml`, then run `npm install` in
   `sdks/typescript` so the lockfile picks it up.
3. Commit and push to `main`, and wait for CI to pass.
4. Tag and push:
   ```sh
   git tag -a v0.2.0 -m "v0.2.0"
   git push origin v0.2.0
   ```
5. The [Release workflow](../.github/workflows/release.yml) checks that the tag matches both versions, runs
   the tests, and publishes to npm and PyPI. Watch it with `gh run watch`.
6. Optionally, write release notes with `gh release create v0.2.0 --generate-notes`.

If one registry fails and the other succeeds, fix the cause and re-run only the failed job
(`gh run rerun <run-id> --failed`). A version can't be republished to either registry, so don't retag.

### How publishing is authenticated

Both registries use trusted publishing: they check that the upload comes from `release.yml` in this repo,
running in the `npm` or `pypi` GitHub environment. There are no registry tokens to store or rotate.

- PyPI: configured under the project's *Publishing* settings (owner `zaini`, repo `trading212-sdk`,
  workflow `release.yml`, environment `pypi`).
- npm: configured under the package's *Settings → Trusted Publisher* (same values, environment `npm`, with
  "Allow npm publish" ticked).

The `npm` and `pypi` environments only accept `v*` tags, so nothing else in the repo can publish.

## CI and secrets

| Workflow | Runs on | Does |
| --- | --- | --- |
| `ci.yml` | every push and PR | regenerates and diffs, spec coverage checks, TS tests on Node 18/20/22, Python tests on 3.9/3.12/3.13 |
| `live-tests.yml` | push to `main`, Mondays 07:00 UTC, manual | read-only tests against the demo account |
| `release.yml` | `v*` tags | publishes to npm and PyPI |

The live tests use `T212_API_KEY` and `T212_API_SECRET` from the `demo` environment, which only runs on
`main`. Secrets are encrypted, masked in logs, and not given to workflows from forked pull requests.

To create or rotate the demo key:

1. In the Trading 212 app, switch to the **Practice** account and go to Settings → API. Create a key with
   read permissions only (the live tests never trade). The secret is shown once.
2. Store it. `gh secret set` prompts for the value, so it stays out of your shell history and out of chats:
   ```sh
   gh secret set T212_API_KEY --env demo
   gh secret set T212_API_SECRET --env demo
   ```
3. Run the live tests: `gh workflow run live-tests.yml`, then `gh run watch`.
4. Delete the old key in the app.

To run the live tests locally, export the two variables (or put them in a git-ignored `.env`) and run
`uv run pytest tests/live -v` in `sdks/python` or `npx vitest run tests/live.test.ts` in `sdks/typescript`.

The live tests only cover what a demo account can do. CSV exports return 403 on demo, and pagination is only
exercised past the first page if the demo account has more than one historical order, dividend or
transaction.
