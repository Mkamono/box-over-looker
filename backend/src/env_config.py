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
