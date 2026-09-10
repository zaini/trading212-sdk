# Trading 212 SDKs

Unofficial, generated, fully typed SDKs for the [Trading 212 Public API](https://docs.trading212.com/api):

| Language | Package | Install | Source |
| --- | --- | --- | --- |
| TypeScript / JavaScript | [`t212`](https://www.npmjs.com/package/t212) | `npm install t212` | [`sdks/typescript`](sdks/typescript) |
| Python | [`t212-sdk`](https://pypi.org/project/t212-sdk/) (`import t212`) | `pip install t212-sdk` | [`sdks/python`](sdks/python) |

> Not affiliated with or endorsed by Trading 212. Use at your own risk — the live environment trades real money.

```ts
import { Trading212Client } from "t212";

const client = new Trading212Client({ apiKey: "...", apiSecret: "..." }); // demo by default
const positions = await client.positions.list();
for await (const order of await client.history.listOrders()) console.log(order);
```

```python
from t212 import Trading212Client
from t212.pagination import paginate

client = Trading212Client(api_key="...", api_secret="...")  # demo by default
positions = client.positions.list()
for order in paginate(client.history.list_orders):
    print(order)
```

## Why

The existing community SDK, [`codeledge/t212-sdk`](https://github.com/codeledge/t212-sdk), is no longer
kept up to date with the current API. Instead of maintaining clients by hand, this repo generates them from
Trading 212's official OpenAPI spec with [Fern](https://github.com/fern-api/fern)'s open-source generators,
run locally. When the API changes, we update the spec and regenerate.

## Features

- Every endpoint in the spec, with consistent names in each language's style ([naming map](docs/naming-map.md))
- `apiKey` / `apiSecret` auth, with `T212_API_KEY` / `T212_API_SECRET` env var fallback
- `Demo` / `Live` environments, with demo as the default
- Auto-pagination over history endpoints
- Deprecated Pies endpoints still available, marked as deprecated
- Typed errors, timeouts, and retries with backoff for reads (order placement is never retried)
- Sync and async Python clients; zero-dependency TypeScript client (ESM + CJS)

## Repository layout

```
openapi/        Trading 212's spec, untouched (api.yaml; api.json has the same content)
fern/           Fern config: generators.yml (auth, versions) + overrides.yml (names, pagination, ...)
scripts/        generate.sh, post-processing patches, naming-map generator
sdks/typescript generated src/ + our package.json, tests
sdks/python     generated src/t212/ + our pyproject.toml, tests
tests/          spec coverage: every operation is mapped, and every override applied
docs/           how-it-works.md, naming-map.md
```

## Development

```sh
scripts/generate.sh                                        # regenerate both SDKs (needs Docker)
uv run --project sdks/python pytest tests                  # spec coverage checks
(cd sdks/python && uv run pytest)                          # Python tests
(cd sdks/typescript && npm install && npm test)            # TypeScript tests
```

Live tests against a demo account run when `T212_API_KEY` / `T212_API_SECRET` are set.
**Before trading, read [docs/api-gotchas.md](docs/api-gotchas.md)** — e.g. you sell by sending a negative quantity.

[docs/how-it-works.md](docs/how-it-works.md) explains every change we make to the spec, the
post-generation patches, CI secrets, and how to generate SDKs for other languages.
