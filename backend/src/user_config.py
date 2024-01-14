import re
from pathlib import Path

from pydantic import BaseModel, Field


class NotificationTiming(BaseModel):
    zero: bool = Field(alias="0時")
    six: bool = Field(alias="6時")
    twelve: bool = Field(alias="12時")
    eighteen: bool = Field(alias="18時")


class UserConfig(BaseModel):
    mail: str = Field(alias="メールアドレス")
    threshold_increase_rate_price: float = Field(alias="価格の増加倍率(%)")
    notification_timing: NotificationTiming = Field(alias="通知時間")
    period_days: int = Field(alias="価格の過去データの日数")


def get_user_config() -> UserConfig:
    user_config_path = Path(__file__).parent.parent / "user_config.jsonc"
    with open(
        user_config_path,
        "r",
        encoding="utf-8",
    ) as f:
        user_config_str = f.read()
        # jsoncのコメントを削除
        user_config_re = re.sub(r"/\*[\s\S]*?\*/|//.*", "", user_config_str)
        return UserConfig.model_validate_json(user_config_re)
