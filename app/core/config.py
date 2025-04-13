from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    INPUT_SOURCE: str
    XLSX_FILE_PATH: str
    CSV_FILE_PATH: str
    GOOGLE_SHEET_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()