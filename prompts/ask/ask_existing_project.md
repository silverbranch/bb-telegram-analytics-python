# IDE Assistant Prompt — Integrate SDK into Existing Bot

Copy this prompt when adding BB Telegram Analytics to an already-running bot with minimal changes.

---

**Task:** Add BB Telegram Analytics SDK to my existing Telegram bot with minimal code changes.

**Checklist:**

- [ ] Install SDK: `pip install "git+https://github.com/silverbranch/bb-telegram-analytics-python.git"`
- [ ] Add env vars: `BB_ANALYTICS_ENABLED`, `BB_API_BASE_URL`, `BB_INTEGRATION_KEY`
- [ ] Create a single `bb_analytics.Client` instance at startup (where the bot/app is initialized)
- [ ] Inject client into handlers (middleware, DI container, or global/store — avoid creating client per request)
- [ ] In `/start` handler: add `await bb_client.send_event("user_started", tg_user_id, chat_id, payload)`
- [ ] In command handlers: add `send_event("command_used", ...)` with appropriate payload
- [ ] Optionally: add `send_event("activity", ...)` for repeat interactions (SDK throttles automatically)
- [ ] Do not wrap `send_event` in try/except — SDK is fail-safe and never raises
- [ ] Ensure no new dependencies beyond the SDK (it brings httpx)
- [ ] Verify env vars are loaded before client creation (e.g. from `.env` or docker `environment`)

**Minimal change approach:** Add one client factory call at startup, one middleware (or equivalent) to inject it, and one `send_event` call per handler you want to track. Do not refactor unrelated logic.
