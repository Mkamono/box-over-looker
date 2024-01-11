import os

from pydantic import BaseModel


class NotificationTiming(BaseModel):
    zero: bool = False
    six: bool = False
    twelve: bool = False
    eighteen: bool = False


def get_notification_timing() -> NotificationTiming:
    notification_timing = NotificationTiming()

    def convert_to_bool(string: str) -> bool:
        if string == "True":
            return True
        elif string == "False":
            return False
        else:
            raise ValueError(f"Invalid value: {string}")

    notification_timing.zero = convert_to_bool(os.environ["NOTIFICATION_TIMING_ZERO"])
    notification_timing.six = convert_to_bool(os.environ["NOTIFICATION_TIMING_SIX"])
    notification_timing.twelve = convert_to_bool(
        os.environ["NOTIFICATION_TIMING_TWELVE"]
    )
    notification_timing.eighteen = convert_to_bool(
        os.environ["NOTIFICATION_TIMING_EIGHTEEN"]
    )
    return notification_timing
