# Minimal aiogram 3 Structure with BB Analytics

Recommended folder layout for an aiogram 3 bot integrating the SDK.

```
bot/
├── main.py           # Entry point: load config, create client, register middleware, start polling
├── config.py         # Load BB_ANALYTICS_ENABLED, BB_API_BASE_URL, BB_INTEGRATION_KEY
├── middleware.py     # BBMiddleware: injects bb_client into data["bb_client"]
├── handlers/
│   ├── __init__.py   # Router registration
│   ├── start.py      # /start handler → send_event("user_started", ...)
│   └── commands.py   # Other commands → send_event("command_used", ...)
├── .env              # BB_* variables (gitignore in production)
└── requirements.txt  # aiogram, bb-analytics-sdk (or git+url), python-dotenv
```

**main.py** creates the client once, registers the middleware, and starts the dispatcher.

**config.py** reads env vars; optional validation when enabled.

**middleware.py** sets `data["bb_client"]` before handlers run.

**handlers/** use `bb_client: bb_analytics.Client` as a keyword argument and call `send_event`.
