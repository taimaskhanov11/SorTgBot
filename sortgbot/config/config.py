import typing
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent
TEMP_DIR = BASE_DIR / f"sortgbot/bot/temp"


def load_yaml(file) -> dict:
    with open(Path(BASE_DIR, file), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Database(BaseModel):
    username: str
    password: str
    host: str
    port: int
    db_name: str


class Bot(BaseModel):
    token: str
    admins: Optional[list[int]]


class Config(BaseModel):
    bot: Bot
    db: Database


config = Config(**load_yaml("config.yml"))
