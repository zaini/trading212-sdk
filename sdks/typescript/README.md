# t212 — Trading 212 TypeScript SDK

Unofficial, fully typed TypeScript/JavaScript client for the [Trading 212 Public API](https://docs.trading212.com/api).
Generated from Trading 212's OpenAPI spec. Zero runtime dependencies. Works with Node 18+ and any runtime with `fetch`.
Not affiliated with Trading 212.

```sh
npm install t212
```

## Usage

```ts
import { Trading212Client, Trading212Environment } from "t212";

const client = new Trading212Client({
    environment: Trading212Environment.Demo, // or .Live (real money)
    apiKey: "...", // defaults to the T212_API_KEY env var
    apiSecret: "...", // defaults to the T212_API_SECRET env var
});

const summary = await client.account.getSummary();
const positions = await client.positions.list();
await client.orders.placeMarket({ ticker: "AAPL_US_EQ", quantity: 1 });
```

### Pagination

History endpoints return a `Page` that fetches further pages as you iterate:

```ts
for await (const order of await client.history.listOrders({ limit: 50 })) {
    console.log(order.order?.id);
}
```

Or page by page: `page.data`, `page.hasNextPage()`, `await page.getNextPage()`.

### Deprecated endpoints

`client.pies.*` still works, but Trading 212 no longer supports or updates the Pies API.
These methods are marked `@deprecated`.

### Errors, retries and timeouts

Non-2xx responses throw typed errors (`Trading212.UnauthorizedError`, `Trading212.TooManyRequestsError`, ...),
all extending `Trading212Error`. Requests are retried up to twice with backoff on 408, 429 and 5xx.
Per-request options: `{ timeoutInSeconds, maxRetries, abortSignal }`.

See [docs/naming-map.md](https://github.com/zaini/trading212-sdk/blob/main/docs/naming-map.md) for every method.
