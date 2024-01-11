import os

from pydantic import BaseModel


class NotificationTiming(BaseModel):
    zero: bool = True
    six: bool = False
    twelve: bool = False
    eighteen: bool = False
