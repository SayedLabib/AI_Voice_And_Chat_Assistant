from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str
    speech_recognition_service_url: str
    text_to_speech_service_url: str

    class Config:
        env_file = ".env"

settings = Settings()