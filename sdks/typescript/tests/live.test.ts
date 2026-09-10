/**
 * Read-only tests against a real Trading 212 *demo* account.
 * Skipped unless T212_API_KEY and T212_API_SECRET are set. Never places orders.
 * The Python live suite covers every endpoint; this one checks the TypeScript
 * client end to end without doubling up on rate-limited calls.
 */
import { describe, expect, it } from "vitest";
import { Trading212Client, Trading212Environment } from "../src/index.js";

const hasCredentials = Boolean(process.env.T212_API_KEY && process.env.T212_API_SECRET);
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

describe.skipIf(!hasCredentials)("live (demo account)", () => {
    // Only ever run against demo.
    const client = new Trading212Client({ environment: Trading212Environment.Demo, maxRetries: 4 });

    it("gets the account summary", async () => {
        const summary = await client.account.getSummary();
        expect(summary.currency).toBeTruthy();
    });

    it("lists positions", async () => {
        await sleep(1500);
        expect(Array.isArray(await client.positions.list())).toBe(true);
    });

    it("paginates historical orders", async () => {
        await sleep(1500);
        const page = await client.history.listOrders({ limit: 1 });
        expect(Array.isArray(page.data)).toBe(true);
        if (page.hasNextPage()) {
            await sleep(11_000); // history endpoints: 6 req / 1m
            const next = await page.getNextPage();
            expect(next.data).not.toEqual(page.data);
        }
    }, 30_000);
});
