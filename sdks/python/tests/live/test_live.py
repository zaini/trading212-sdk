"""Read-only tests against a real Trading 212 *demo* account.

Skipped unless T212_API_KEY and T212_API_SECRET are set. Never places orders.
Endpoints are rate limited (e.g. instruments: 1 req / 50s), so each endpoint is
called at most once or twice, and requests are spaced out.

    T212_API_KEY=... T212_API_SECRET=... uv run pytest tests/live -v
"""

from __future__ import annotations

import os
import time
import typing
import warnings

import pydantic
import pytest

from t212 import Trading212Client, Trading212ClientEnvironment
from t212.errors import ForbiddenError
from t212.pagination import paginate_pages

pytestmark = pytest.mark.skipif(
    not (os.getenv("T212_API_KEY") and os.getenv("T212_API_SECRET")),
    reason="T212_API_KEY / T212_API_SECRET not set",
)


@pytest.fixture(scope="module")
def client() -> Trading212Client:
    # Only ever run against demo, whatever the environment says.
    return Trading212Client(environment=Trading212ClientEnvironment.DEMO, max_retries=4)


@pytest.fixture(autouse=True)
def _space_out_requests():
    yield
    time.sleep(1.5)


def undocumented_fields(model: typing.Any, raw: typing.Any, path: str = "") -> list[str]:
    """Fields present in the raw JSON but missing from the generated model (= spec drift)."""
    if isinstance(model, list):
        return [f for m, r in zip(model, raw) for f in undocumented_fields(m, r, f"{path}[]")][:20]
    if not isinstance(model, pydantic.BaseModel) or not isinstance(raw, dict):
        return []
    known = {field.alias or name for name, field in type(model).model_fields.items()}
    missing = [f"{path}.{key}" for key in raw if key not in known]
    for name, field in type(model).model_fields.items():
        key = field.alias or name
        if key in raw:
            missing += undocumented_fields(getattr(model, name), raw[key], f"{path}.{key}")
    return missing


def check(call: typing.Callable[[], typing.Any]) -> typing.Any:
    """Make a raw-response call, assert it parses, and warn about undocumented fields."""
    response = call()
    drift = undocumented_fields(response.data, response._response.json())
    if drift:
        warnings.warn(f"API returned fields not in the spec: {sorted(set(drift))}")
    return response.data


def test_account_summary(client):
    summary = check(client.account.with_raw_response.get_summary)
    assert summary.currency


def test_positions(client):
    assert isinstance(check(client.positions.with_raw_response.list), list)


def test_pending_orders(client):
    assert isinstance(check(client.orders.with_raw_response.list), list)


def test_exchanges(client):
    assert check(client.instruments.with_raw_response.list_exchanges)


def test_instruments(client):
    assert check(client.instruments.with_raw_response.list)


def test_reports(client):
    try:
        assert isinstance(check(client.history.with_raw_response.list_reports), list)
    except ForbiddenError as e:
        if "not-available-in-demo-account" in str(e.body):
            pytest.skip("CSV exports are not available on demo accounts")
        raise


def test_pies_deprecated_but_working(client):
    with pytest.warns(DeprecationWarning):
        assert isinstance(client.pies.list(), list)


@pytest.mark.parametrize("method", ["list_orders", "list_dividends", "list_transactions"])
def test_history_pagination(client, method):
    """Fetch up to two pages of one item each and check the cursor moved on."""
    pages = []
    for page in paginate_pages(getattr(client.history, method), limit=1):
        pages.append(page)
        if len(pages) == 2:
            break
        time.sleep(11)  # history endpoints: 6 req / 1m
    first = pages[0]
    assert isinstance(first.items, list)
    if first.next_page_path:
        assert len(pages) == 2, "nextPagePath was set but the next page was not fetched"
        assert pages[1].items != first.items, "second page returned the same items as the first"
