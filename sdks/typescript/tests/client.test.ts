import { afterEach, describe, expect, it, vi } from "vitest";
import { Trading212Client, Trading212Environment } from "../src/index.js";

const DEMO = "https://demo.trading212.com";
const LIVE = "https://live.trading212.com";

type Call = { url: string; headers: Headers };

function mockFetch(...bodies: unknown[]) {
    const calls: Call[] = [];
    const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        calls.push({ url: String(input), headers: new Headers(init?.headers) });
        const body = bodies.length > 1 ? bodies.shift() : bodies[0];
        return new Response(JSON.stringify(body), { status: 200, headers: { "content-type": "application/json" } });
    });
    return { fetch: fetch as unknown as typeof globalThis.fetch, calls };
}

const basic = (key: string, secret: string) => `Basic ${Buffer.from(`${key}:${secret}`).toString("base64")}`;

afterEach(() => {
    vi.unstubAllEnvs();
});

describe("auth and environments", () => {
    it("sends key + secret as Basic auth to demo by default", async () => {
        const { fetch, calls } = mockFetch([]);
        await new Trading212Client({ apiKey: "key", apiSecret: "secret", fetch }).positions.list();
        expect(calls[0].url).toBe(`${DEMO}/api/v0/equity/positions`);
        expect(calls[0].headers.get("authorization")).toBe(basic("key", "secret"));
    });

    it("supports the live environment", async () => {
        const { fetch, calls } = mockFetch([]);
        const client = new Trading212Client({
            environment: Trading212Environment.Live,
            apiKey: "k",
            apiSecret: "s",
            fetch,
        });
        await client.positions.list();
        expect(calls[0].url).toBe(`${LIVE}/api/v0/equity/positions`);
    });

    it("falls back to T212_API_KEY / T212_API_SECRET", async () => {
        vi.stubEnv("T212_API_KEY", "env-key");
        vi.stubEnv("T212_API_SECRET", "env-secret");
        const { fetch, calls } = mockFetch([]);
        await new Trading212Client({ fetch }).positions.list();
        expect(calls[0].headers.get("authorization")).toBe(basic("env-key", "env-secret"));
    });
});

describe("pagination", () => {
    it("follows nextPagePath until it is null", async () => {
        const { fetch, calls } = mockFetch(
            { items: [{ order: { id: 3 } }, { order: { id: 2 } }], nextPagePath: "/api/v0/equity/history/orders?limit=2&cursor=200" },
            { items: [{ order: { id: 1 } }], nextPagePath: null },
        );
        const client = new Trading212Client({ apiKey: "k", apiSecret: "s", fetch });

        const ids: number[] = [];
        for await (const item of await client.history.listOrders({ limit: 2 })) {
            ids.push(item.order!.id!);
        }

        expect(ids).toEqual([3, 2, 1]);
        expect(calls.map((c) => c.url)).toEqual([
            `${DEMO}/api/v0/equity/history/orders?limit=2`,
            `${DEMO}/api/v0/equity/history/orders?limit=2&cursor=200`,
        ]);
    });

    it("passes the whole nextPagePath query string through", async () => {
        const next = "/api/v0/equity/history/transactions?cursor=abc&time=2024-01-01T00%3A00%3A00Z";
        const { fetch, calls } = mockFetch({ items: [], nextPagePath: next }, { items: [], nextPagePath: null });
        const client = new Trading212Client({ apiKey: "k", apiSecret: "s", fetch });

        const page = await client.history.listTransactions();
        expect(page.hasNextPage()).toBe(true);
        await page.getNextPage();

        expect(calls[1].url).toBe(`${DEMO}${next}`);
    });
});
