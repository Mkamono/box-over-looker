import os

from pydantic import BaseModel


class NotificationTiming(BaseModel):
    zero: bool = False
    six: bool = False
    twelve: bool = False
    eighteen: bool = False


def get_notification_timing() -> NotificationTiming:
    def convert_to_bool(string: str) -> bool:
        if string == "True":
            return True
        elif string == "False":
            return False
        else:
            raise ValueError(f"Invalid value: {string}")

    notification_timing = NotificationTiming()
    for timing in notification_timing.model_dump():
        notification_timing.__setattr__(
            timing, convert_to_bool(os.environ[f"NOTIFICATION_TIMING_{timing.upper()}"])
        )
    return notification_timing
