# Reference
## Account
<details><summary><code>client.account.<a href="src/t212/account/client.py">get_summary</a>() -> AccountSummary</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Provides a breakdown of your account's cash and investment metrics,
including available funds, invested capital, and total account value.

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.account.get_summary()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## History
<details><summary><code>client.history.<a href="src/t212/history/client.py">list_dividends</a>(...) -> PaginatedResponseHistoryDividendItem</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>



**Rate limit:** 6 req / 1m0s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.history.list_dividends()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[int]` — Pagination cursor
    
</dd>
</dl>

<dl>
<dd>

**ticker:** `typing.Optional[str]` — Ticker filter
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Max items: 50
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/t212/history/client.py">list_reports</a>() -> typing.List[ReportResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a list of all requested CSV reports and their current status. 


**Asynchronous Workflow:**

1. Call `POST /history/exports` to request a report. You will receive a
`reportId`.

2. Periodically call this endpoint (`GET /history/exports`) to check the
`status` of the report corresponding to your `reportId`.

3. Once the status is `Finished`, the `downloadLink` field will contain
a URL to download the CSV file.

**Rate limit:** 1 req / 1m0s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.history.list_reports()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/t212/history/client.py">request_report</a>(...) -> EnqueuedReportResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Initiates the generation of a CSV report containing historical account
data. This is an asynchronous operation. The response will include a
`reportId` which you can use to track the status of the generation
process using the `GET /history/exports` endpoint.

**Rate limit:** 1 req / 30s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.history.request_report()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**data_included:** `typing.Optional[ReportDataIncluded]` 
    
</dd>
</dl>

<dl>
<dd>

**time_from:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**time_to:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/t212/history/client.py">list_orders</a>(...) -> PaginatedResponseHistoricalOrder</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>



**Rate limit:** 6 req / 1m0s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.history.list_orders()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[int]` — Pagination cursor
    
</dd>
</dl>

<dl>
<dd>

**ticker:** `typing.Optional[str]` — Ticker filter
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Max items: 50
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/t212/history/client.py">list_transactions</a>(...) -> PaginatedResponseHistoryTransactionItem</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch superficial information about movements to and from your account

**Rate limit:** 6 req / 1m0s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.history.list_transactions()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Pagination cursor
    
</dd>
</dl>

<dl>
<dd>

**time:** `typing.Optional[datetime.datetime]` — Retrieve transactions starting from the specified time
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Max items: 50
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Instruments
<details><summary><code>client.instruments.<a href="src/t212/instruments/client.py">list_exchanges</a>() -> typing.List[Exchange]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves all accessible exchanges and their corresponding working schedules.
Data is refreshed every 10 minutes.

**Rate limit:** 1 req / 30s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.instruments.list_exchanges()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.instruments.<a href="src/t212/instruments/client.py">list</a>() -> typing.List[TradableInstrument]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves all accessible instruments.
Data is refreshed every 10 minutes.

**Rate limit:** 1 req / 50s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.instruments.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Orders
<details><summary><code>client.orders.<a href="src/t212/orders/client.py">list</a>() -> typing.List[Order]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a list of all orders that are currently active (i.e., not yet
filled, cancelled, or expired). This is useful for monitoring the status
of your open positions and managing your trading strategy.

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="src/t212/orders/client.py">place_limit</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new Limit order, which executes at a specified price or
better.

- To place a **buy** order, use a positive `quantity`. The order will
fill at the `limitPrice` or lower.

- To place a **sell** order, use a negative `quantity`. The order will
fill at the `limitPrice` or higher.



**Order Limitations**

* Orders can be executed only in the **main account currency**


**Important:** In this beta version, this endpoint is **not
idempotent**. Sending the same request multiple times may result in
duplicate orders.

**Rate limit:** 1 req / 2s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.place_limit()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit_price:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**ticker:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**time_validity:** `typing.Optional[TimeValidity]` — Expiration
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="src/t212/orders/client.py">place_market</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new Market order, which is an instruction to trade a security
immediately at the next available price. 

- To place a **buy** order, use a positive `quantity`. 

- To place a **sell** order, use a negative `quantity`.


- **`extendedHours`**: Set to `true` to allow the order to be filled
outside of the standard trading session.

- If placed when the market is closed, the order will be queued to
execute when the market next opens.

x
**Order Limitations**

* Orders can be executed only in the **main account currency**


**Warning:** Market orders can be subject to price slippage, where the
final execution price may differ from the price at the time of order
placement.


**Important:** In this beta version, this endpoint is **not
idempotent**. Sending the same request multiple times may result in
duplicate orders.

**Rate limit:** 50 req / 1m0s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.place_market()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**extended_hours:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**ticker:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="src/t212/orders/client.py">place_stop</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new Stop order, which places a Market order once the
`stopPrice` is reached.

- To place a **buy** stop order, use a positive `quantity`.

- To place a **sell** stop order (commonly a 'stop-loss'), use a
negative `quantity`.


- The `stopPrice` is triggered by the instrument's **Last Traded Price
(LTP)**.




**Order Limitations**

* Orders can be executed only in the **main account currency**

**Important:** In this beta version, this endpoint is **not
idempotent**. Sending the same request multiple times may result in
duplicate orders.

**Rate limit:** 1 req / 2s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.place_stop()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**quantity:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**stop_price:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**ticker:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**time_validity:** `typing.Optional[TimeValidity]` — Expiration
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="src/t212/orders/client.py">place_stop_limit</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new Stop-Limit order, combining features of a Stop and a Limit
order. The direction of the trade (buy/sell) is determined by the sign
of the `quantity` field.


**Execution Logic:**

1.  When the instrument's **Last Traded Price (LTP)** reaches the
specified `stopPrice`, the order is triggered.

2.  A Limit order is then automatically placed at the specified
`limitPrice`.


This two-step process helps protect against price slippage that can
occur with a standard Stop order.


**Order Limitations**

* Orders can be executed only in the **main account currency**


**Important:** In this beta version, this endpoint is **not
idempotent**. Sending the same request multiple times may result in
duplicate orders.

**Rate limit:** 1 req / 2s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.place_stop_limit()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit_price:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**stop_price:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**ticker:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**time_validity:** `typing.Optional[TimeValidity]` — Expiration
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="src/t212/orders/client.py">get</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a single pending order using its unique numerical ID. This is
useful for checking the status of a specific order you have previously
placed.

**Rate limit:** 1 req / 1s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.get(
    id=1000000,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `int` — The unique identifier of the order you want to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="src/t212/orders/client.py">cancel</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Attempts to cancel an active, unfilled order by its unique ID.
Cancellation is not guaranteed if the order is already in the process of
being filled. A successful response indicates the cancellation request
was accepted.

**Rate limit:** 50 req / 1m0s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.orders.cancel(
    id=1000000,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `int` — The unique identifier of the order you want to cancel.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Pies
<details><summary><code>client.pies.<a href="src/t212/pies/client.py">list</a>() -> typing.List[AccountBucketResultResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches all pies for the account

**Rate limit:** 1 req / 30s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.pies.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pies.<a href="src/t212/pies/client.py">create</a>(...) -> AccountBucketInstrumentsDetailedResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a pie for the account by given params

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.pies.create()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `PieRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pies.<a href="src/t212/pies/client.py">get</a>(...) -> AccountBucketInstrumentsDetailedResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a pies for the account with detailed information

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.pies.get(
    id=1000000,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pies.<a href="src/t212/pies/client.py">update</a>(...) -> AccountBucketInstrumentsDetailedResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a pie for the account by given params

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.pies.update(
    id=1000000,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request:** `PieRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pies.<a href="src/t212/pies/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a pie by given id

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.pies.delete(
    id=1000000,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pies.<a href="src/t212/pies/client.py">duplicate</a>(...) -> AccountBucketInstrumentsDetailedResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Duplicates a pie for the account 

**Rate limit:** 1 req / 5s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.pies.duplicate(
    id=1000000,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Positions
<details><summary><code>client.positions.<a href="src/t212/positions/client.py">list</a>(...) -> typing.List[Position]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch all open positions for your account

**Rate limit:** 1 req / 1s
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from t212 import Trading212Client
from t212.environment import Trading212ClientEnvironment

client = Trading212Client(
    api_key="<username>",
    api_secret="<password>",
    environment=Trading212ClientEnvironment.DEMO,
)

client.positions.list(
    ticker="AAPL_US_EQ",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ticker:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

