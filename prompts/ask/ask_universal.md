# Universal IDE Assistant Prompt — BB Telegram Analytics SDK

Copy this prompt to your IDE assistant when integrating BB Telegram Analytics SDK into any async Python Telegram bot.

---

**Task:** Integrate the BB Telegram Analytics Python SDK into my async Python Telegram bot. The bot sends events to the BB Analytics API for tracking user actions.

**Requirements:**

1. **Single client instance** — Create exactly one `bb_analytics.Client` at application startup. Do not instantiate it inside handlers. Pass it into handlers via dependency injection (e.g. middleware, context, or constructor).

2. **Environment configuration** — Read from env vars:
   - `BB_ANALYTICS_ENABLED` — enable/disable (default off)
   - `BB_API_BASE_URL` — base URL (e.g. `https://bb-bot.ru`)
   - `BB_INTEGRATION_KEY` — Bearer token from BB admin

3. **Safe send (never crash the bot)** — The SDK is fail-safe: `send_event()` never raises exceptions. Use it from handlers without try/except for analytics. Ensure you are not wrapping it in logic that could crash the bot on unrelated errors.

4. **Event sending** — Call `await bb_client.send_event(event_name, tg_user_id, chat_id, payload)` from handlers when events occur. Standard events: `user_started` (on /start), `command_used` (on commands), `activity` (repeat interactions, SDK throttles to 1 per 60 sec per user).

5. **Payload** — Use flat JSON-serializable dict, snake_case keys, no secrets. `tg_user_id` and `chat_id` may be `None` when unavailable.

**Reference:** BB Telegram Analytics SDK — `bb_analytics.Client`, `send_event()`. Endpoint: `{base_url}/api/bot/events`.
