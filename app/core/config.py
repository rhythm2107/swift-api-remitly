from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    INPUT_SOURCE: str = "xlsx"
    XLSX_FILE_PATH: str = "data/swift_codes.xlsx"
    CSV_FILE_PATH: str = "data/swift_codes.csv"
    GOOGLE_SHEET_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()