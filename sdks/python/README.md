# t212 — Trading 212 Python SDK

Unofficial, fully typed Python client for the [Trading 212 Public API](https://docs.trading212.com/api).
Generated from Trading 212's OpenAPI spec. Not affiliated with Trading 212.

```sh
pip install t212
```

## Usage

```python
from t212 import Trading212Client, Trading212ClientEnvironment

client = Trading212Client(
    environment=Trading212ClientEnvironment.DEMO,  # or .LIVE (real money)
    api_key="...",      # defaults to the T212_API_KEY env var
    api_secret="...",   # defaults to the T212_API_SECRET env var
)

summary = client.account.get_summary()
positions = client.positions.list()
client.orders.place_market(ticker="AAPL_US_EQ", quantity=1)  # buy
client.orders.place_market(ticker="AAPL_US_EQ", quantity=-1)  # sell: negative quantity
```

An `AsyncTrading212Client` with the same methods is also available.

### Pagination

History endpoints return one page at a time. Use `paginate` to iterate over every item:

```python
from t212.pagination import paginate

for order in paginate(client.history.list_orders, limit=50):
    print(order.id)
```

For the async client use `apaginate` (`async for order in apaginate(...)`).
`paginate_pages` / `apaginate_pages` yield whole pages instead of items.

### Deprecated endpoints

`client.pies.*` still works, but Trading 212 no longer supports or updates the Pies API.
Calling these methods emits a `DeprecationWarning` (the `with_raw_response` variants don't).

Read the [API gotchas](https://github.com/zaini/trading212-sdk/blob/main/docs/api-gotchas.md) before trading.
See [docs/naming-map.md](https://github.com/zaini/trading212-sdk/blob/main/docs/naming-map.md) for every method.
