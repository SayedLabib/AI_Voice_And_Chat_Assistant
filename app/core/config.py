from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    SPEECH_TO_TEXT_SERVICE_URL: str
    TEXT_TO_SPEECH_SERVICE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()