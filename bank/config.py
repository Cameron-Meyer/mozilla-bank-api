import os

from pydantic import BaseSettings


# https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support
class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), 'envs', f'{os.getenv("RUNTIME_ENV", "dev")}.env')
