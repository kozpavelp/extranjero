from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_ids: list


@dataclass
class Config:
    tgbot : TgBot


def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tgbot=TgBot(token=env('BOT_TOKEN'), admin_ids=list(map(int, env.list('ADMIN_IDS')))))
