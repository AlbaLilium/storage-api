from pydantic_settings import BaseSettings


class SettingsPostgres(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


    class Config:
        secrets_dir = 'utils/secrets'
        env_file = "utils/environments/db.env"

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = SettingsPostgres()
