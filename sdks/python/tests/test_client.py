"""Offline tests for the Python SDK, with HTTP mocked by respx."""

from __future__ import annotations

import base64

import httpx
import pytest
import respx

from t212 import AsyncTrading212Client, Trading212Client, Trading212ClientEnvironment
from t212.pagination import apaginate, next_page_kwargs, paginate, paginate_pages

DEMO = "https://demo.trading212.com"
LIVE = "https://live.trading212.com"


def basic(key: str, secret: str) -> str:
    return "Basic " + base64.b64encode(f"{key}:{secret}".encode()).decode()


@pytest.fixture
def client() -> Trading212Client:
    return Trading212Client(api_key="key", api_secret="secret")


def order_page(ids: list[int], next_path: str | None) -> dict:
    return {"items": [{"order": {"id": i}} for i in ids], "nextPagePath": next_path}


@respx.mock
def test_basic_auth_header_and_demo_default(client):
    route = respx.get(f"{DEMO}/api/v0/equity/positions").respond(json=[])
    client.positions.list()
    assert route.calls.last.request.headers["authorization"] == basic("key", "secret")


@respx.mock
def test_live_environment():
    route = respx.get(f"{LIVE}/api/v0/equity/positions").respond(json=[])
    Trading212Client(environment=Trading212ClientEnvironment.LIVE, api_key="k", api_secret="s").positions.list()
    assert route.called


@respx.mock
def test_credentials_from_env(monkeypatch):
    monkeypatch.setenv("T212_API_KEY", "env-key")
    monkeypatch.setenv("T212_API_SECRET", "env-secret")
    # The generated client reads env vars as parameter defaults at import time,
    # so reload the module after setting them.
    import importlib

    import t212.client

    importlib.reload(t212.client)
    route = respx.get(f"{DEMO}/api/v0/equity/positions").respond(json=[])
    t212.client.Trading212Client().positions.list()
    assert route.calls.last.request.headers["authorization"] == basic("env-key", "env-secret")


def test_missing_credentials_raise(monkeypatch):
    monkeypatch.delenv("T212_API_KEY", raising=False)
    with pytest.raises(Exception, match="api_key"):
        Trading212Client(api_key=None, api_secret="s")


@respx.mock
def test_paginate_follows_next_page_path(client):
    route = respx.get(f"{DEMO}/api/v0/equity/history/orders").mock(
        side_effect=[
            httpx.Response(200, json=order_page([3, 2], "/api/v0/equity/history/orders?limit=2&cursor=200")),
            httpx.Response(200, json=order_page([1], None)),
        ]
    )
    ids = [o.order.id for o in paginate(client.history.list_orders, limit=2)]
    assert ids == [3, 2, 1]
    first, second = (dict(c.request.url.params) for c in route.calls)
    assert first == {"limit": "2"}
    assert second == {"limit": "2", "cursor": "200"}


@respx.mock
def test_paginate_forwards_unknown_query_params(client):
    route = respx.get(f"{DEMO}/api/v0/equity/history/transactions").mock(
        side_effect=[
            httpx.Response(200, json={"items": [], "nextPagePath": "/api/v0/equity/history/transactions?cursor=abc&time=2024-01-01T00%3A00%3A00Z&newParam=x"}),
            httpx.Response(200, json={"items": [], "nextPagePath": None}),
        ]
    )
    pages = list(paginate_pages(client.history.list_transactions))
    assert len(pages) == 2
    assert dict(route.calls[1].request.url.params) == {"cursor": "abc", "time": "2024-01-01T00:00:00Z", "newParam": "x"}


def test_next_page_kwargs_keeps_request_options():
    kwargs = next_page_kwargs(
        "/api/v0/equity/history/dividends?limit=5&cursor=9&extra=1",
        request_options={"timeout_in_seconds": 3},
    )
    assert kwargs == {
        "request_options": {
            "timeout_in_seconds": 3,
            "additional_query_parameters": {"limit": "5", "cursor": "9", "extra": "1"},
        },
    }


@respx.mock
async def test_apaginate():
    client = AsyncTrading212Client(api_key="k", api_secret="s")
    respx.get(f"{DEMO}/api/v0/equity/history/dividends").mock(
        side_effect=[
            httpx.Response(200, json={"items": [{"ticker": "A"}], "nextPagePath": "/api/v0/equity/history/dividends?cursor=1"}),
            httpx.Response(200, json={"items": [{"ticker": "B"}], "nextPagePath": None}),
        ]
    )
    tickers = [d.ticker async for d in apaginate(client.history.list_dividends)]
    assert tickers == ["A", "B"]


@respx.mock
def test_deprecated_pies_warn(client):
    respx.get(f"{DEMO}/api/v0/equity/pies").respond(json=[])
    with pytest.warns(DeprecationWarning, match="pies.list is deprecated"):
        client.pies.list()


@respx.mock
def test_non_deprecated_methods_do_not_warn(client, recwarn):
    respx.get(f"{DEMO}/api/v0/equity/positions").respond(json=[])
    client.positions.list()
    assert not [w for w in recwarn if issubclass(w.category, DeprecationWarning)]


@pytest.mark.parametrize(
    "next_path, expected",
    [
        (None, False),
        ("", False),
        ("null", False),
        ("null&ticker=AAPL_US_EQ", False),
        ("/api/v0/equity/history/orders?limit=2&cursor=null", False),
        ("/api/v0/equity/history/orders?limit=2&cursor=5", True),
        ("limit=5&cursor=abc&time=2025-01-01T00:00:00Z", True),
    ],
)
def test_has_next_page(next_path, expected):
    from t212.pagination import has_next_page

    assert has_next_page(next_path) is expected


@respx.mock
def test_paginate_handles_query_only_next_page_path(client):
    route = respx.get(f"{DEMO}/api/v0/equity/history/transactions").mock(
        side_effect=[
            httpx.Response(200, json={"items": [], "nextPagePath": "limit=5&cursor=abc&time=2025-01-01T00:00:00Z"}),
            httpx.Response(200, json={"items": [], "nextPagePath": "null&limit=5"}),
        ]
    )
    assert len(list(paginate_pages(client.history.list_transactions, limit=5))) == 2
    assert dict(route.calls[1].request.url.params) == {"limit": "5", "cursor": "abc", "time": "2025-01-01T00:00:00Z"}


@respx.mock
def test_paginate_stops_if_the_same_page_repeats(client):
    same = order_page([1], "/api/v0/equity/history/orders?cursor=1")
    respx.get(f"{DEMO}/api/v0/equity/history/orders").mock(return_value=httpx.Response(200, json=same))
    with pytest.warns(UserWarning, match="same next page twice"):
        pages = list(paginate_pages(client.history.list_orders))
    assert len(pages) == 2


@respx.mock
def test_order_placement_is_not_retried(client):
    route = respx.post(f"{DEMO}/api/v0/equity/orders/market").respond(503)
    with pytest.raises(Exception):
        client.orders.place_market(ticker="AAPL_US_EQ", quantity=1)
    assert route.call_count == 1


@respx.mock
def test_reads_are_retried(client):
    route = respx.get(f"{DEMO}/api/v0/equity/positions").mock(
        side_effect=[httpx.Response(503), httpx.Response(200, json=[])]
    )
    client.positions.list()
    assert route.call_count == 2
