import dataclasses
import os

from dotenv import load_dotenv


@dataclasses.dataclass
class Config:
    GCP__CREDENTIALS_JSON: str = None
    ALPHAVANTAGE__API_KEY: str = None

    def __init__(self):
        self.GCP__CREDENTIALS_JSON: str = os.getenv("GCP__CREDENTIALS_JSON")
        self.ALPHAVANTAGE__API_KEY: str = os.getenv("ALPHAVANTAGE__API_KEY")


@dataclasses.dataclass
class Consts:
    pass


class Settings:
    _config = None
    _consts = None

    @classmethod
    def init(cls):
        load_dotenv()
        cls._config = Config()
        cls._consts = Consts()

    @property
    def config(self) -> Config:
        if self._config is not None:
            return self._config
        raise Exception("Config not initialized")

    @property
    def consts(self) -> Consts:
        if self._consts is not None:
            return self._consts
        raise Exception("Consts not initialized")


settings = Settings()
