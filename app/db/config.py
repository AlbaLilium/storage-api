from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsPostgres(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # class Config:
    # secrets_dir = '/run/secrets/'
    model_config = SettingsConfigDict(
        env_file="utils/environments/db.env",
        env_file_encoding="utf-8",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = SettingsPostgres()
# print(f"{settings.sqlalchemy_database_url=}".upper())
