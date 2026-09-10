// Hand-written (listed in .fernignore): how to follow Trading 212's `nextPagePath`.
//
// Observed forms of nextPagePath:
//   "/api/v0/equity/history/orders?limit=50&cursor=1705326600000"   full path (documented)
//   "limit=5&cursor=abc&time=2025-01-01T00:00:00Z"                    query string only
//   null / ""                                                        last page
//   "null&ticker=AAPL_US_EQ"                                          last page (older API)

function isQueryOnly(nextPagePath: string): boolean {
    return !nextPagePath.startsWith("/") && !nextPagePath.includes("?") && nextPagePath.includes("=");
}

function query(nextPagePath: string): URLSearchParams {
    const q = isQueryOnly(nextPagePath) ? nextPagePath : nextPagePath.split("?")[1] ?? "";
    return new URLSearchParams(q);
}

/** Whether `nextPagePath` points at another page. */
export function hasNextPage(nextPagePath: string | null | undefined): boolean {
    if (nextPagePath == null) return false;
    const value = nextPagePath.trim();
    if (value === "" || value === "null" || value.startsWith("null&") || value.startsWith("null?")) return false;
    return query(value).get("cursor") !== "null";
}

/** Absolute URL for the next page. `requestPath` is used when nextPagePath is only a query string. */
export function resolveNextPageUrl(baseUrl: string, nextPagePath: string, requestPath: string): string {
    if (isQueryOnly(nextPagePath)) {
        return new URL(`${requestPath}?${nextPagePath}`, baseUrl).toString();
    }
    // Plain URL resolution keeps the query string intact (Fern's url.join would encode the `?`).
    return new URL(nextPagePath, baseUrl).toString();
}
