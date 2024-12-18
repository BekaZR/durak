from urllib.parse import urljoin
from pydantic import model_validator
from pydantic_settings import BaseSettings
from yarl import URL

# load_dotenv(".env", override=True)


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TIMER_EXPIRE_SECONDS: int = 400

    APP_TITLE: str = "template_project"
    APP_PORT: int = 8080
    ROOT_PATH: str = ""
    API_V1_STR: str = "/api"
    DEBUG: bool = True

    # Current environment
    ENV: str = "dev"

    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "durakservice"
    POSTGRES_ECHO: bool = False
    POSTGRES_URL: URL | None = None

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379

    @model_validator(mode="after")
    def assemble_db_url(self) -> "Settings":
        self.POSTGRES_URL = URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )
        return self


class UserServiceSettings(BaseSettings):
    BASE_URL: str = ""
    BET_ROUTER: str = ""
    MICROSERVICE_KEY: str = ""
    BALANCE_URL: str = "api/payments/user/{user_id}/balance/{balance_type}"

    @property
    def callback_url(self) -> str:
        return urljoin(self.BASE_URL, self.BET_ROUTER)


user_service_settings = UserServiceSettings()
settings = Settings()
