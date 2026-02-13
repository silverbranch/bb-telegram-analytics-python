"""HTTP transport для отправки событий в BB API."""
import logging
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

import httpx

logger = logging.getLogger(__name__)


async def post_event(
    base_url: str,
    integration_key: str,
    event_name: str,
    tg_user_id: Optional[int],
    chat_id: Optional[int],
    payload: Optional[dict],
) -> None:
    """
    Отправляет один запрос POST /api/bot/events.
    Authorization: Bearer. Fail-silent: логирует warning при ошибке, не пробрасывает исключение.
    """
    url = f"{base_url.rstrip('/')}/api/bot/events"
    headers = {
        "Authorization": f"Bearer {integration_key}",
        "Content-Type": "application/json",
    }
    body: dict[str, Any] = {
        "event_name": event_name,
        "occurred_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tg_user_id": tg_user_id,
        "chat_id": chat_id,
        "payload": payload or {},
        "idempotency_key": str(uuid4()),
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(url, json=body, headers=headers)
            if resp.status_code >= 400:
                logger.warning(
                    "BB API event %s failed: %s %s",
                    event_name,
                    resp.status_code,
                    resp.text[:200],
                )
    except Exception as e:
        logger.warning("BB API event %s error: %s", event_name, e)
