"""Клиент для отправки событий в BB API."""
from typing import Optional

from .throttle import should_skip_activity
from .transport import post_event


class Client:
    """
    Клиент аналитики. Один экземпляр на приложение.
    Метод send_event: при enabled=False не отправляет; для activity применяет throttle 60 сек.
    """

    def __init__(
        self,
        base_url: str,
        integration_key: str,
        enabled: bool,
    ) -> None:
        self._base_url = base_url
        self._integration_key = integration_key
        self._enabled = enabled

    async def send_event(
        self,
        event_name: str,
        tg_user_id: Optional[int],
        chat_id: Optional[int],
        payload: Optional[dict],
    ) -> None:
        """Отправляет событие в BB API. Ошибки не пробрасываются (fail-silent)."""
        if not self._enabled:
            return
        if event_name == "activity" and tg_user_id is not None:
            if should_skip_activity(tg_user_id):
                return
        await post_event(
            base_url=self._base_url,
            integration_key=self._integration_key,
            event_name=event_name,
            tg_user_id=tg_user_id,
            chat_id=chat_id,
            payload=payload,
        )

    async def track(
        self,
        event_name: str,
        tg_user_id: Optional[int],
        chat_id: Optional[int],
        payload: Optional[dict],
    ) -> None:
        """Алиас для send_event (будущая совместимость)."""
        await self.send_event(event_name, tg_user_id, chat_id, payload)
