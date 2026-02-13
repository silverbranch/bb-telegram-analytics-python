# Architecture Plan — New Bot with BB Analytics (Universal)

Use this plan when designing a new async Python Telegram bot that integrates BB Telegram Analytics SDK.

---

## Modules

1. **Config** — Load `BB_ANALYTICS_ENABLED`, `BB_API_BASE_URL`, `BB_INTEGRATION_KEY` from environment. Validate presence of key when enabled. Support `.env` or equivalent.

2. **Client factory** — Function that returns a single `bb_analytics.Client` instance. Called once at startup. Parameters: `base_url`, `integration_key`, `enabled`.

3. **Injection** — Pass the client into handlers via:
   - Middleware (set `data["bb_client"]` or equivalent)
   - DI container / context
   - Constructor injection for handler classes

   Never instantiate the client inside handlers.

4. **Docker** — If bot runs in Docker and API on host: use `BB_API_BASE_URL=http://host.docker.internal:PORT`. On Linux: add `extra_hosts: ["host.docker.internal:host-gateway"]` or use host network. See [docker_networking.md](../troubleshooting/docker_networking.md).

5. **Testing** — Mock or substitute `bb_analytics.Client` in tests. Use `BB_ANALYTICS_ENABLED=false` for local runs if no API available. The SDK is fail-safe; integration tests can run without a live API.

## Flow

- Startup → load config → create client → register middleware/injection → start bot
- Handler → receives `bb_client` → calls `await bb_client.send_event(...)` when events occur
- SDK handles: HTTP, throttle, idempotency; no exceptions to bot
