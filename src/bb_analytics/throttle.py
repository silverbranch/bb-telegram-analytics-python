"""Throttle для события activity: не чаще 60 сек на пользователя."""
import time

_activity_last_sent: dict[int, float] = {}
ACTIVITY_THROTTLE_SEC = 60


def should_skip_activity(tg_user_id: int) -> bool:
    """
    Возвращает True, если отправку activity для данного tg_user_id нужно пропустить
    (прошло меньше ACTIVITY_THROTTLE_SEC с последней отправки).
    При False обновляет время последней отправки для tg_user_id.
    """
    now = time.monotonic()
    last = _activity_last_sent.get(tg_user_id, 0)
    if now - last < ACTIVITY_THROTTLE_SEC:
        return True
    _activity_last_sent[tg_user_id] = now
    return False
