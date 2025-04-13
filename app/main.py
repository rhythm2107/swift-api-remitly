from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

from ingestion import parse_data
from core.config import settings

print("===================================================")
csv = parse_data.parse_csv(settings.CSV_FILE_PATH)
print(csv)

print("===================================================")

xlsx = parse_data.parse_xlsx(settings.XLSX_FILE_PATH)
print(xlsx)

print("===================================================")
google = parse_data.parse_google_sheet(settings.GOOGLE_SHEET_URL)
print(google)