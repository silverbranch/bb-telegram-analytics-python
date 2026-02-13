# Event Contract

Conventions for event names and payloads when using BB Telegram Analytics SDK.

## Event Names

Use snake_case. Standard names:

| Event         | When to use                                      |
|---------------|--------------------------------------------------|
| `user_started`| User triggered /start                            |
| `command_used`| User executed a command (e.g. /help, /settings)  |
| `activity`    | Repeat interaction (e.g. button click, menu); SDK throttles to 1 per 60 sec per user |
| `choice_made` | User made a choice (button, inline, etc.)        |

## Payload Conventions

- **Flat JSON** — Use a single-level dict. Avoid deeply nested structures.
- **snake_case** — Keys: `handler`, `source`, `team_code`, `choice_id`, etc.
- **No secrets** — Do not send tokens, keys, or sensitive user data in payload.
- **JSON-serializable** — str, int, float, bool, list, dict only.

## Examples

```python
# user_started
payload={"source": "telegram", "handler": "start"}

# command_used
payload={"command": "help", "handler": "commands"}

# activity
payload={"action": "button_click", "button_id": "main_menu"}

# choice_made
payload={"choice_id": "team_bra", "handler": "worldcup"}
```
