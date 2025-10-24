from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    The model path is defined here, pointing to where the Dockerfile will download it.
    """
    MODEL_PATH: str = "/app/model/mobileclip2_s0.pt"
    MODEL_NAME: str = "MobileCLIP2-S0"

    class Config:
        env_file = ".env"

settings = Settings()