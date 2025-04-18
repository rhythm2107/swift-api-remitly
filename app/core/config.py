from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    INPUT_SOURCE: str = "xlsx"
    XLSX_FILE_PATH: str = "data/swift_codes.xlsx"
    CSV_FILE_PATH: str = "data/swift_codes.csv"
    GOOGLE_SHEET_URL: str
    TEST_DATABASE_URL: str
    DEV_MODE: str

    model_config = ConfigDict(
        env_file = ".env",
        extra = "ignore"
    )

settings = Settings()