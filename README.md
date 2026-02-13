# BB Telegram Analytics — Python SDK

Async Python SDK for sending Telegram bot analytics events to BB Analytics API (bb-bot.ru / bb.center).

## Installation

From GitHub:

```bash
pip install "git+https://github.com/silverbranch/bb-telegram-analytics-python.git"
```

Local editable install (development):

```bash
pip install -e /path/to/bb-telegram-analytics-python
```

Requires Python 3.11+ and httpx.

## Quick Start (aiogram 3)

1. Set environment variables: `BB_ANALYTICS_ENABLED`, `BB_API_BASE_URL`, `BB_INTEGRATION_KEY` (see Configuration).

2. Create the client once at startup and pass it to your handlers (e.g. via middleware as `data["bb_client"]`).

3. Call `send_event()` from handlers when events occur.

Example: send `user_started` on /start:

```python
import os
import bb_analytics
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

def get_bb_client():
    return bb_analytics.Client(
        base_url=os.getenv("BB_API_BASE_URL", "https://bb-bot.ru"),
        integration_key=os.getenv("BB_INTEGRATION_KEY", ""),
        enabled=os.getenv("BB_ANALYTICS_ENABLED", "false").lower() in ("true", "1", "yes"),
    )

# At startup: bb_client = get_bb_client(); inject bb_client via middleware into data["bb_client"].

@router.message(CommandStart())
async def cmd_start(message: Message, bb_client: bb_analytics.Client):
    await message.answer("Hello!")
    await bb_client.send_event(
        event_name="user_started",
        tg_user_id=message.from_user.id if message.from_user else None,
        chat_id=message.chat.id,
        payload={"source": "telegram", "handler": "start"},
    )
```

## Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `BB_ANALYTICS_ENABLED` | Enable or disable sending events | `true`, `false` |
| `BB_API_BASE_URL` | Base URL of the BB API (no trailing slash) | `https://bb-bot.ru`, `https://bb.center` |
| `BB_INTEGRATION_KEY` | Integration key (Bearer token) from BB admin | secret string |

If `BB_ANALYTICS_ENABLED` is not truthy, the client does not send any requests.

## Backend neutrality

The SDK is backend-agnostic. All requests are sent to:

```
{base_url}/api/bot/events
```

You choose the backend by setting `BB_API_BASE_URL`:

- **bb-bot.ru** — production
- **bb.center** — alternative / staging
- **Local** — e.g. `http://host.docker.internal:8001` when the bot runs in Docker

The same code works with any of these; only the environment variable changes.

## Events

Events are identified by `event_name` (string) and an optional `payload` (dict). The API requires `event_name`, `occurred_at`, and `idempotency_key`; the SDK sets `occurred_at` (UTC ISO) and `idempotency_key` (UUID) automatically. You provide `tg_user_id`, `chat_id`, and `payload`.

Conventional event names:

- **user_started** — user triggered /start
- **choice_made** — user made a choice (button, command)
- **activity** — repeat interaction (e.g. “my choice”); throttled (see Activity throttle)

`payload` is arbitrary JSON-serializable data (e.g. `{"team_code": "bra", "handler": "choice"}`). It is sent as-is; default is `{}`. `tg_user_id` and `chat_id` may be `None`.

## Activity throttle

For `event_name == "activity"`, the SDK sends at most one request per 60 seconds per `tg_user_id`. Additional `send_event(..., event_name="activity", ...)` calls for the same user within that window are skipped (no request, no error). Other event names are not throttled.

## Fail-safe behavior

The SDK does not raise exceptions to your bot logic. On network or API errors (4xx/5xx), it logs a warning and returns. Your bot continues running; analytics failures do not affect user-facing behavior.

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| **401 Unauthorized** | Verify `BB_INTEGRATION_KEY`. The API expects header `Authorization: Bearer <key>`. |
| **422 Validation error** | API requires `event_name`, `occurred_at`, `idempotency_key`. The SDK sends these; if calling the API directly, match the contract. |
| **Bot in Docker cannot reach API on host** | Use `BB_API_BASE_URL=http://host.docker.internal:PORT`. On Linux, add `extra_hosts: ["host.docker.internal:host-gateway"]` in docker-compose or use host network. |

## Support

- Telegram: [@bb_analytics_helper_bot](https://t.me/bb_analytics_helper_bot)
