# Architecture Plan — New aiogram 3 Bot with BB Analytics

Same plan as universal, oriented for aiogram 3.

---

## Modules

1. **Config** — Load `BB_ANALYTICS_ENABLED`, `BB_API_BASE_URL`, `BB_INTEGRATION_KEY` from environment (e.g. `python-dotenv`). Validate presence of key when enabled.

2. **Client factory** — `get_bb_client()` returning `bb_analytics.Client`. Called in `main()` before `dp.start_polling()`.

3. **Middleware** — aiogram 3 `BaseMiddleware` subclass that:
   - Accepts `bb_client` in `__init__`
   - In `__call__`: sets `data["bb_client"] = self.bb_client`, then `await handler(event, data)`
   - Register via `router.message.middleware()` or `dp.update.middleware()`

4. **Handlers** — Use `bb_client: bb_analytics.Client` as keyword arg (from `data`). Call `send_event("user_started", ...)` in /start, `send_event("command_used", ...)` in command handlers, `send_event("activity", ...)` for repeat interactions.

5. **Docker** — `BB_API_BASE_URL=http://host.docker.internal:PORT`. Linux: `extra_hosts: ["host.docker.internal:host-gateway"]`. See [docker_networking.md](../troubleshooting/docker_networking.md).

6. **Testing** — Mock `bb_client` or use `BB_ANALYTICS_ENABLED=false`. aiogram 3 supports handler testing with overridden `data`.

## Flow

- `main()` → load config → `bb_client = get_bb_client()` → register `BBMiddleware(bb_client)` → `dp.start_polling()`
- Handler receives `bb_client` via keyword; calls `send_event` without try/except
