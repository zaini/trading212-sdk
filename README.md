# Trading 212 SDKs

Typed TypeScript and Python clients for the [Trading 212 Public API](https://docs.trading212.com/api),
generated from Trading 212's official OpenAPI spec.

| Language | Install | Import | Docs |
| --- | --- | --- | --- |
| TypeScript / JavaScript | `npm install t212` | `import { Trading212Client } from "t212"` | [sdks/typescript](sdks/typescript/README.md) |
| Python 3.9+ | `pip install t212-sdk` | `from t212 import Trading212Client` | [sdks/python](sdks/python/README.md) |

Unofficial and not affiliated with Trading 212. The `Live` environment trades real money.

## Quick start

Create an API key in the Trading 212 app (Settings → API). Keys are tied to one account and one
environment, so a demo key only works against `Demo`.

```ts
import { Trading212Client, Trading212Environment } from "t212";

const client = new Trading212Client({
    environment: Trading212Environment.Demo, // the default
    apiKey: process.env.T212_API_KEY,
    apiSecret: process.env.T212_API_SECRET,
});

const summary = await client.account.getSummary();

for await (const item of await client.history.listOrders({ limit: 50 })) {
    console.log(item.order?.ticker, item.fill?.price);
}
```

```python
from t212 import Trading212Client
from t212.pagination import paginate

client = Trading212Client()  # reads T212_API_KEY / T212_API_SECRET; demo by default

summary = client.account.get_summary()

for item in paginate(client.history.list_orders, limit=50):
    print(item.order.ticker, item.fill.price if item.fill else None)
```

Before placing orders, read [docs/api-gotchas.md](docs/api-gotchas.md). For example, you sell by sending a
negative `quantity`, quantities are limited to 4 decimal places, and order requests are never retried
automatically.

## What's covered

- All 22 operations in the spec: account, instruments, orders, positions, history, CSV exports, and the
  deprecated Pies endpoints. Method names are consistent across languages; see the [naming map](docs/naming-map.md).
- Key + secret auth, read from `T212_API_KEY` / `T212_API_SECRET` if not passed in.
- `Demo` and `Live` environments. Demo is the default.
- Pagination over `nextPagePath` for order, dividend and transaction history.
- Typed errors, timeouts, and retries with backoff for reads. POST requests are never retried.
- TypeScript: no runtime dependencies, ESM and CommonJS, Node 18+.
- Python: sync and async clients, pydantic models, `py.typed`.

## Why another SDK

[`codeledge/t212-sdk`](https://github.com/codeledge/t212-sdk) and the other community clients were written
by hand, and most of them target the API as it was before the October 2025 changes (key + secret auth,
`/account/summary`, the new history shape). These SDKs are generated from the spec instead, using
[Fern](https://github.com/fern-api/fern)'s open-source generators run locally, so an API update is a spec
update plus a regeneration.

## Repository layout

```
openapi/          Trading 212's spec, unmodified
fern/             generators.yml (versions, auth) and overrides.yml (names, pagination, retries, deprecation)
scripts/          generate.sh, post-generation patches, naming-map generator
sdks/typescript/  generated src/, plus package.json, README and tests we maintain
sdks/python/      generated src/t212/, plus pyproject.toml, README and tests we maintain
tests/            checks that every operation is mapped and every override made it into both SDKs
docs/             how-it-works, maintaining, api-gotchas, naming-map
```

## Development

Requires Docker (for generation), Node 18+, Python 3.9+ and [uv](https://docs.astral.sh/uv/).

```sh
scripts/generate.sh                           # regenerate both SDKs
uv run --project sdks/python pytest tests     # spec coverage checks
(cd sdks/python && uv run pytest)             # Python tests
(cd sdks/typescript && npm ci && npm test)    # TypeScript tests
```

Live tests run against a demo account when `T212_API_KEY` and `T212_API_SECRET` are set; otherwise they skip.

- [docs/how-it-works.md](docs/how-it-works.md): what we change in the spec and why, and the post-generation patches
- [docs/maintaining.md](docs/maintaining.md): updating the spec, upgrading Fern, releasing, CI secrets
- [docs/api-gotchas.md](docs/api-gotchas.md): API behaviour that the spec doesn't document

## Contributing

Issues and pull requests are welcome, especially:

- **API behaviour that surprised you**: a field that came back `null`, an undocumented error, a rate limit
  that doesn't match the docs. [Open an issue](https://github.com/zaini/trading212-sdk/issues) with the
  request and response (remove your keys). These become tests or entries in the gotchas doc.
- **Spec updates**, when Trading 212 publishes a new version.
- **Helpers on top of the generated clients**, such as an instruments cache or a wait-for-export helper.
- **Docs and examples.**

Most of `sdks/*/src` is generated, so fixes usually belong in `fern/overrides.yml`, a post-generation patch,
or a hand-written file. [CONTRIBUTING.md](CONTRIBUTING.md) explains where each kind of change goes.

## License

[MIT](LICENSE)
