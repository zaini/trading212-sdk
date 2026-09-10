# t212-sdk

Typed Python client for the [Trading 212 Public API](https://docs.trading212.com/api), generated from
Trading 212's OpenAPI spec. Unofficial and not affiliated with Trading 212.

```sh
pip install t212-sdk
```

The package installs as `t212-sdk` and imports as `t212`.

## Usage

```python
from t212 import Trading212Client, Trading212ClientEnvironment

client = Trading212Client(
    environment=Trading212ClientEnvironment.DEMO,  # default; LIVE trades real money
    api_key="...",     # optional: defaults to the T212_API_KEY env var
    api_secret="...",  # optional: defaults to the T212_API_SECRET env var
)

summary = client.account.get_summary()
positions = client.positions.list()

client.orders.place_market(ticker="AAPL_US_EQ", quantity=1)   # buy
client.orders.place_market(ticker="AAPL_US_EQ", quantity=-1)  # sell: negative quantity
```

`AsyncTrading212Client` has the same methods, as coroutines.

Responses are pydantic models. Every method is listed in the
[naming map](https://github.com/zaini/trading212-sdk/blob/main/docs/naming-map.md).

## Pagination

History methods return one page. `paginate` follows `nextPagePath` and yields every item:

```python
from t212.pagination import paginate

for item in paginate(client.history.list_orders, limit=50):
    print(item.order.ticker, item.order.status)
```

- `apaginate` is the async version (`async for item in apaginate(async_client.history.list_orders)`).
- `paginate_pages` and `apaginate_pages` yield whole pages instead of items.

## Errors, retries and timeouts

Non-2xx responses raise `t212.core.api_error.ApiError`, or one of its subclasses in `t212.errors`
(`UnauthorizedError`, `ForbiddenError`, `TooManyRequestsError`, ...). `status_code` and `body` hold the
response details.

```python
from t212.errors import TooManyRequestsError

try:
    client.positions.list()
except TooManyRequestsError as e:
    print(e.headers.get("x-ratelimit-reset"))
```

Reads are retried twice on 408, 429 and 5xx, waiting for the rate-limit reset where the API provides it.
POST requests (placing orders, requesting exports) are never retried, because a request that timed out may
still have gone through.

Set `timeout` and `max_retries` on the client, or per call with
`request_options={"timeout_in_seconds": 10, "max_retries": 0}`.

## Deprecated endpoints

`client.pies.*` still works, but Trading 212 no longer maintains the Pies API. These methods emit a
`DeprecationWarning` (the `with_raw_response` variants don't).

## Before you trade

Read the [API gotchas](https://github.com/zaini/trading212-sdk/blob/main/docs/api-gotchas.md):
rate limits per account, 4-decimal quantity precision, ticker formats, what isn't available on demo, and more.
