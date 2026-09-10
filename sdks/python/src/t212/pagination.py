"""Auto-pagination for Trading 212 history endpoints.

Hand-written (listed in .fernignore). Fern's local Python generator does not
emit paginated methods, so this follows `next_page_path` for us.

Trading 212 returns `nextPagePath`, usually a path + query string such as
`/api/v0/equity/history/orders?limit=50&cursor=1760346100000`. Its query
parameters are exactly the arguments for the next call, so each page is fetched
by calling the same SDK method again with exactly that query string.

Other observed forms are handled too: a bare query string
(`limit=5&cursor=abc&time=...`), and `null` / `""` / `"null&ticker=..."` for
the last page.

    from t212 import Trading212Client
    from t212.pagination import paginate

    client = Trading212Client()
    for order in paginate(client.history.list_orders, limit=50):
        print(order.id)
"""

from __future__ import annotations

import typing
import warnings
from urllib.parse import parse_qsl

from .core.request_options import RequestOptions

T = typing.TypeVar("T")


class _Page(typing.Protocol[T]):
    items: typing.Optional[typing.List[T]]
    next_page_path: typing.Optional[str]


def _query(next_page_path: str) -> str:
    if "?" in next_page_path:
        return next_page_path.split("?", 1)[1]
    return "" if next_page_path.startswith("/") else next_page_path


def has_next_page(next_page_path: typing.Optional[str]) -> bool:
    """Whether `next_page_path` points at another page."""
    if next_page_path is None:
        return False
    value = next_page_path.strip()
    if value in ("", "null") or value.startswith(("null&", "null?")):
        return False
    return dict(parse_qsl(_query(value))).get("cursor") != "null"


def next_page_kwargs(
    next_page_path: str,
    request_options: typing.Optional[RequestOptions] = None,
) -> typing.Dict[str, typing.Any]:
    """Keyword arguments that make an SDK method request `next_page_path`.

    The query string is sent verbatim as additional query parameters rather
    than mapped onto typed arguments, so values such as `time` are passed
    through exactly as Trading 212 returned them.
    """
    query = dict(parse_qsl(_query(next_page_path)))
    options: RequestOptions = dict(request_options or {})  # type: ignore[assignment]
    options["additional_query_parameters"] = {**options.get("additional_query_parameters", {}), **query}
    return {"request_options": options}


def paginate_pages(method: typing.Callable[..., _Page[T]], **kwargs: typing.Any) -> typing.Iterator[_Page[T]]:
    """Yield every page from a paginated history method, starting with `kwargs`."""
    request_options = kwargs.get("request_options")
    page = method(**kwargs)
    seen: typing.Set[str] = set()
    while True:
        yield page
        next_path = page.next_page_path
        if not has_next_page(next_path):
            return
        if next_path in seen:
            warnings.warn(f"Stopping pagination: the API returned the same next page twice ({next_path})")
            return
        seen.add(typing.cast(str, next_path))
        page = method(**next_page_kwargs(typing.cast(str, next_path), request_options))


def paginate(method: typing.Callable[..., _Page[T]], **kwargs: typing.Any) -> typing.Iterator[T]:
    """Yield every item from a paginated history method, across all pages."""
    for page in paginate_pages(method, **kwargs):
        yield from page.items or []


async def apaginate_pages(
    method: typing.Callable[..., typing.Awaitable[_Page[T]]], **kwargs: typing.Any
) -> typing.AsyncIterator[_Page[T]]:
    """Async version of `paginate_pages`, for `AsyncTrading212Client`."""
    request_options = kwargs.get("request_options")
    page = await method(**kwargs)
    seen: typing.Set[str] = set()
    while True:
        yield page
        next_path = page.next_page_path
        if not has_next_page(next_path):
            return
        if next_path in seen:
            warnings.warn(f"Stopping pagination: the API returned the same next page twice ({next_path})")
            return
        seen.add(typing.cast(str, next_path))
        page = await method(**next_page_kwargs(typing.cast(str, next_path), request_options))


async def apaginate(
    method: typing.Callable[..., typing.Awaitable[_Page[T]]], **kwargs: typing.Any
) -> typing.AsyncIterator[T]:
    """Async version of `paginate`, for `AsyncTrading212Client`."""
    async for page in apaginate_pages(method, **kwargs):
        for item in page.items or []:
            yield item
