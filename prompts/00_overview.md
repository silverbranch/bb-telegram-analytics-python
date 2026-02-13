# BB Telegram Analytics SDK — Prompt Library Overview

## What the SDK Does

BB Telegram Analytics SDK is an async Python client that sends bot analytics events to the BB Analytics API (bb-bot.ru / bb.center). It is backend-agnostic: you can use it with any async Python Telegram bot framework (aiogram, python-telegram-bot, pyTelegramBotAPI, etc.).

Key behaviors:
- **Single client instance** — create one `bb_analytics.Client` at startup and inject it into handlers
- **Fail-safe** — never raises exceptions to your bot; on 4xx/5xx it logs a warning and returns
- **Activity throttle** — for `event_name == "activity"`, at most one request per 60 seconds per user

## ASK vs PLAN Prompts

| Prompt type | When to use |
|-------------|-------------|
| **ASK** | Use when you want the IDE assistant to help integrate the SDK into an existing or new bot. Copy-paste the prompt and let it guide implementation. |
| **PLAN** | Use when you need a full architecture plan before coding. Covers modules, config, client factory, injection, Docker, and testing. |

- **ASK** → [ask_universal.md](ask/ask_universal.md), [ask_aiogram3.md](ask/ask_aiogram3.md), [ask_existing_project.md](ask/ask_existing_project.md)
- **PLAN** → [plan_universal.md](plan/plan_universal.md), [plan_aiogram3.md](plan/plan_aiogram3.md)

## Environment Variables

Set these before running the bot:

| Variable | Description | Example |
|----------|-------------|---------|
| `BB_ANALYTICS_ENABLED` | Enable or disable sending events | `true`, `false` |
| `BB_API_BASE_URL` | Base URL of the BB API (no trailing slash) | `https://bb-bot.ru`, `https://bb.center` |
| `BB_INTEGRATION_KEY` | Integration key (Bearer token) from BB admin | secret string |

Typical locations: `.env` file, Docker `environment`, or shell export.

## Event Contract

Standard event names:
- **user_started** — user triggered /start
- **command_used** — user executed a command (e.g. /help, /settings)
- **activity** — repeat interaction; throttled (max 1 per 60 sec per user)

See [event_contract.md](examples/event_contract.md) for payload conventions and structure.

## Troubleshooting

If you hit 401, 422, or Docker networking issues, use:

- [errors_401_422.md](troubleshooting/errors_401_422.md) — API auth and validation errors
- [docker_networking.md](troubleshooting/docker_networking.md) — reaching the API from inside containers
