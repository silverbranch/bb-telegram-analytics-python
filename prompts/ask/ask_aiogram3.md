# IDE Assistant Prompt — BB Telegram Analytics SDK (aiogram 3)

Copy this prompt to your IDE assistant when integrating the SDK into an aiogram 3 bot.

---

**Task:** Integrate the BB Telegram Analytics Python SDK into my aiogram 3 bot using middleware injection and handler usage.

**aiogram 3 specifics:**

1. **Middleware injection** — Register a middleware that injects `bb_client` into `data["bb_client"]` for every handler. Use `Dispatcher.update.middleware` or a custom `BaseMiddleware` that sets `data["bb_client"] = self.bb_client` and calls `await handler(event, data)`.

2. **Handler usage** — In message/command handlers, use `bb_client: bb_analytics.Client` as a keyword argument (from `data`). Call `await bb_client.send_event(event_name, tg_user_id, chat_id, payload)` when events occur.

3. **Extracting IDs** — From `message: Message`: `tg_user_id = message.from_user.id if message.from_user else None`, `chat_id = message.chat.id`. Handle optional `message.from_user`.

4. **Single client at startup** — Create the client in `main()` or the startup hook before `dp.start_polling()`. Pass it to the middleware constructor. Do not create the client inside handlers.

5. **Environment** — `BB_ANALYTICS_ENABLED`, `BB_API_BASE_URL`, `BB_INTEGRATION_KEY`. The client must be constructed with these; keep it framework-accurate (no hardcoded values).

6. **Safe send** — The SDK never raises; no try/except needed for analytics. Ensure middleware does not block or crash on analytics failures.

**Reference:** BB Telegram Analytics SDK — `bb_analytics.Client`, `send_event()`. aiogram 3: `BaseMiddleware`, `data` dict, keyword args from middleware.
