from functools import cached_property
from typing import List

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ms-cc-admin"

    db_host: str = "db"
    db_port: int = 3306
    db_name: str = "appdb"
    db_user: str = "appuser"
    db_password: str = "apppass"

    allow_origins: List[str] = ["*"]
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]

    @computed_field
    @cached_property
    def title(self) -> str:
        return self.app_name.replace("-", " ").replace("_", " ").title()

    @computed_field
    @cached_property
    def root_path(self) -> str:
        return f"/{self.app_name}"

    @computed_field
    @cached_property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
