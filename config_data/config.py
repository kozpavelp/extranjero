from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_ids: list


@dataclass
class Config:
    tgbot : TgBot

@dataclass
class OpenAI:
    token: str


@dataclass
class AiConfig:
    ai: OpenAI

def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tgbot=TgBot(token=env('BOT_TOKEN'), admin_ids=list(map(int, env.list('ADMIN_IDS')))))

def load_ai(path: str | None) -> AiConfig:
    env = Env()
    env.read_env(path)
    return AiConfig(ai=OpenAI(token=env('OPENAI_TOKEN')))

