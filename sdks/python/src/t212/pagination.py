"""Auto-pagination for Trading 212 history endpoints.

Hand-written (listed in .fernignore). Fern's local Python generator does not
emit paginated methods, so this follows `next_page_path` for us.

Trading 212 returns `nextPagePath`, a path + query string such as
`/api/v0/equity/history/orders?limit=50&cursor=1760346100000`. Its query
parameters are exactly the arguments for the next call, so each page is fetched
by calling the same SDK method again with exactly that query string.

    from t212 import Trading212Client
    from t212.pagination import paginate

    client = Trading212Client()
    for order in paginate(client.history.list_orders, limit=50):
        print(order.id)
"""

from __future__ import annotations

import typing
from urllib.parse import parse_qsl, urlsplit

from .core.request_options import RequestOptions

T = typing.TypeVar("T")


class _Page(typing.Protocol[T]):
    items: typing.Optional[typing.List[T]]
    next_page_path: typing.Optional[str]


def next_page_kwargs(
    next_page_path: str,
    request_options: typing.Optional[RequestOptions] = None,
) -> typing.Dict[str, typing.Any]:
    """Keyword arguments that make an SDK method request `next_page_path`.

    The query string is sent verbatim as additional query parameters rather
    than mapped onto typed arguments, so values such as `time` are passed
    through exactly as Trading 212 returned them.
    """
    query = dict(parse_qsl(urlsplit(next_page_path).query, keep_blank_values=True))
    options: RequestOptions = dict(request_options or {})  # type: ignore[assignment]
    options["additional_query_parameters"] = {**options.get("additional_query_parameters", {}), **query}
    return {"request_options": options}


def paginate_pages(method: typing.Callable[..., _Page[T]], **kwargs: typing.Any) -> typing.Iterator[_Page[T]]:
    """Yield every page from a paginated history method, starting with `kwargs`."""
    request_options = kwargs.get("request_options")
    page = method(**kwargs)
    while True:
        yield page
        if not page.next_page_path:
            return
        page = method(**next_page_kwargs(page.next_page_path, request_options))


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
    while True:
        yield page
        if not page.next_page_path:
            return
        page = await method(**next_page_kwargs(page.next_page_path, request_options))


async def apaginate(
    method: typing.Callable[..., typing.Awaitable[_Page[T]]], **kwargs: typing.Any
) -> typing.AsyncIterator[T]:
    """Async version of `paginate`, for `AsyncTrading212Client`."""
    async for page in apaginate_pages(method, **kwargs):
        for item in page.items or []:
            yield item
