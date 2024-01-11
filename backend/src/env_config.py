import os

from pydantic import BaseModel


class NotificationTiming(BaseModel):
    zero: bool = False
    six: bool = False
    twelve: bool = False
    eighteen: bool = False


def get_notification_timing() -> NotificationTiming:
    notification_timing = NotificationTiming()

    for timing in notification_timing.model_dump():
        notification_timing.__setattr__(
            timing, os.environ[f"NOTIFICATION_TIMING_{timing.upper()}"]
        )
    return notification_timing
