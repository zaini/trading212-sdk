# Trading 212 API gotchas

The official basics are in the introduction of Trading 212's
[API reference](https://docs.trading212.com/api), which is also the `info.description` of `openapi/api.yaml`.
This page collects what the reference doesn't say, from Trading 212's own
[agent-skills](https://github.com/trading212-labs/agent-skills) guide, the official community forum threads
([2023–25](https://community.trading212.com/t/61788), [Oct 2025 onwards](https://community.trading212.com/t/87988)),
and other community clients. Items marked *(unverified)* come from a single report.

## Accounts and keys

- **Each API key belongs to one environment and one account.** A demo key returns 401 on live, and vice versa.
  Invest and Stocks ISA accounts use identical endpoints; the key decides which account you're using.
  SIPP and CFD accounts aren't supported.
- **The API secret is shown only once**, when the key is created.
- **Keys can be IP-restricted** in the app's API settings. Worth doing for anything running on a fixed server.
- **Keys have scopes.** A missing permission returns 403 `Scope(orders:execute) missing for API key`.
- **Server-side only.** The API rejects browser CORS preflight requests, so don't call it from a web page
  (which would also expose your key).

## Placing orders

- **Sell by sending a negative quantity.** `quantity: 1` buys, `quantity: -1` sells. There is no side field.
- **Quantities allow at most 4 decimal places**, but positions can hold up to 8. Selling a whole
  12.09032128-share position fails with `quantity-precision-mismatch`; truncate to 4 decimals yourself.
- **Orders trade only in the account's primary currency.** Proceeds are converted to it, and an FX fee applies.
  Multi-currency accounts aren't supported; all values in responses are in the primary currency.
- **`extendedHours` is valid on market orders only.** Sending it on a limit or stop order returns 400.
- **Set `timeValidity` explicitly** (`DAY` or `GOOD_TILL_CANCEL`). Sources disagree on the default.
  Order *responses* call the same field `timeInForce`.
- **`SellingEquityNotOwned` can happen while you hold the shares.** Shares tied up in pending orders or pies
  don't count; check `quantityAvailableForTrading` on the position.
- **Order placement is not idempotent.** A request that timed out may still have executed. The SDKs
  therefore **never automatically retry POST requests**. Check `orders.list()` before retrying yourself.
- **Cancelling is best-effort.** The order may already have been filled.
- At most 50 pending orders per ticker. Value-based orders aren't supported.
- Live trading was rolled out in stages: market orders in Oct 2025, limit/stop orders in Jan 2026.
  Older posts saying "demo only" are outdated.

## Rate limits

- **Limits are per account**, not per key, and they differ per endpoint. For example, `instruments.list` is
  limited to 1 request per 50s and `account.getSummary` to 1 per 5s. Each method's docs show its limit.
- Responses include `x-ratelimit-limit`, `x-ratelimit-period`, `x-ratelimit-remaining`, `x-ratelimit-reset`
  (Unix seconds) and `x-ratelimit-used`. The SDKs wait until `x-ratelimit-reset` before retrying a 429
  (reads only).
- The official docs say bursting is allowed: you can use a period's whole allowance at once, then wait for
  `x-ratelimit-reset`. Trading 212's agent-skills guide recommends pacing requests evenly instead, which is
  gentler on the shared per-account budget.

## Instruments and tickers

- **Tickers are Trading 212's own format**: `AAPL_US_EQ`, `VODl_EQ` (lowercase `l` = London), `SXR8d_EQ`
  (`d` = Germany). Look them up from `instruments.list()`; don't build them by hand.
- **`instruments.list()` returns about 5 MB and is limited to 1 request per 50s.** Cache it (agent-skills
  suggests 1 hour).
- UK instruments priced in GBX are quoted in **pence**.
- After a rename, history keeps the old ticker (e.g. SOFI appears as IPOE). Use `isin` or `shortName` to match.

## History and pagination

- The SDKs follow `nextPagePath` for you. They handle a full path, a bare query string, and
  `null` / `""` / `"null&..."` as the end.
- Transactions use a string cursor **plus** a `time` parameter, and both are required together. Orders and
  dividends use a numeric millisecond cursor.
- `limit` defaults to 20 and is capped at 50. There's no date-range filter.
- The API has had history bugs: skipped blocks (fixed late 2025), non-chronological dividends, and
  transactions returning 404 on later pages for some accounts *(reported Feb 2026, open)*. For a complete
  record, use the CSV export.

## CSV exports

`history.requestReport()` returns a `reportId`. Poll `history.listReports()` (1 request per minute)
until that report's status is `Finished`, then download `downloadLink`. Don't send your API credentials to
that URL. Each export also sends a notification to the account's app.

## Errors

Error bodies come in several shapes: problem-details JSON (`{type, title, status, detail}`), legacy
`{code, clarification}`, `{code, message}` on 401, or an empty or plain-text body. The SDK error types
expose the status code and the raw body whatever the shape.

## Data

- Some fields can be `null` even though the spec doesn't say so (e.g. `limitPrice`, `stopPrice`, `fill`
  details, `downloadLink`, `nextPagePath`). Treat every field as optional.
- New enum values appear over time (transaction and dividend types). The SDKs accept unknown values rather
  than failing.
- Pies are deprecated and may be removed. Some users reported them missing as early as Oct 2025.
