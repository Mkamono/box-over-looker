import os

from pydantic import BaseModel


class NotificationTiming(BaseModel):
    zero: bool = True
    six: bool = False
    twelve: bool = False
    eighteen: bool = False


class EnvConfig(BaseModel):
    mail: str
    threshold_increase_rate_price: float
    notification_timing: NotificationTiming
    period_days: int


def get_notification_timing() -> NotificationTiming:
    def to_bool(value: str) -> bool:
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            raise ValueError(f"{value} is not True or False")

    notification_timing = NotificationTiming()
    notification_timing.zero = to_bool(os.environ["NOTIFICATION_TIMING_ZERO"])
    notification_timing.six = to_bool(os.environ["NOTIFICATION_TIMING_SIX"])
    notification_timing.twelve = to_bool(os.environ["NOTIFICATION_TIMING_TWELVE"])
    notification_timing.eighteen = to_bool(os.environ["NOTIFICATION_TIMING_EIGHTEEN"])
    return notification_timing
