# @zaini/t212-sdk

Typed TypeScript/JavaScript client for the [Trading 212 Public API](https://docs.trading212.com/api),
generated from Trading 212's OpenAPI spec. No runtime dependencies; ESM and CommonJS; Node 18+ or any runtime
with `fetch`. Unofficial and not affiliated with Trading 212.

```sh
npm install @zaini/t212-sdk
```

## Usage

```ts
import { Trading212Client, Trading212Environment } from "@zaini/t212-sdk";

const client = new Trading212Client({
    environment: Trading212Environment.Demo, // default; Live trades real money
    apiKey: "...", // optional: defaults to the T212_API_KEY env var
    apiSecret: "...", // optional: defaults to the T212_API_SECRET env var
});

const summary = await client.account.getSummary();
const positions = await client.positions.list();

await client.orders.placeMarket({ ticker: "AAPL_US_EQ", quantity: 1 }); // buy
await client.orders.placeMarket({ ticker: "AAPL_US_EQ", quantity: -1 }); // sell: negative quantity
```

Request and response types are exported under the `Trading212` namespace (`Trading212.Position`,
`Trading212.MarketRequest`, ...). Every method is listed in the
[naming map](https://github.com/zaini/trading212-sdk/blob/main/docs/naming-map.md).

The API rejects browser (CORS) requests, so use this from a server, not a web page.

## Pagination

History methods return a `Page`, which fetches further pages as you iterate:

```ts
for await (const item of await client.history.listOrders({ limit: 50 })) {
    console.log(item.order?.ticker, item.order?.status);
}
```

Or one page at a time with `page.data`, `page.hasNextPage()` and `await page.getNextPage()`.

## Errors, retries and timeouts

Non-2xx responses throw `Trading212Error`, or a subclass such as `Trading212.UnauthorizedError` or
`Trading212.TooManyRequestsError`. `statusCode`, `body` and `rawResponse` hold the response details.

```ts
import { Trading212 } from "@zaini/t212-sdk";

try {
    await client.positions.list();
} catch (e) {
    if (e instanceof Trading212.TooManyRequestsError) {
        console.log(e.rawResponse.headers.get("x-ratelimit-reset"));
    }
}
```

Reads are retried twice on 408, 429 and 5xx, waiting for the rate-limit reset where the API provides it.
POST requests (placing orders, requesting exports) are never retried, because a request that timed out may
still have gone through.

Set `timeoutInSeconds` and `maxRetries` on the client, or per call as the last argument:
`client.positions.list({}, { timeoutInSeconds: 10, abortSignal })`.

## Deprecated endpoints

`client.pies.*` still works, but Trading 212 no longer maintains the Pies API. These methods are marked
`@deprecated`.

## Before you trade

Read the [API gotchas](https://github.com/zaini/trading212-sdk/blob/main/docs/api-gotchas.md):
rate limits per account, 4-decimal quantity precision, ticker formats, what isn't available on demo, and more.
