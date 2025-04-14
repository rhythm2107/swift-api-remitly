import asyncio
import pandas as pd

from app.ingestion.parse_data import parse_data
from app.ingestion.validate_data import validate_data
from app.core.database import SessionLocal
from app.models.swift_code import SwiftCode

async def seed_data() -> None:
    """
    Seeds the Postgres database with data from a pandas DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame containing SwiftCode data.
    """

    # Parse & Validate
    raw_data = parse_data()
    validated_data = validate_data(raw_data)

    async with SessionLocal() as session:
        for _, row in validated_data.iterrows():
            swift_code = SwiftCode(
                swift_code=row.get("swift_code"),
                bank_name=row.get("bank_name"),
                address=row.get("address"),
                country_iso2=row.get("country_iso2"),
                country_name=row.get("country_name"),
                is_headquarter=row.get("is_headquarter", False)
            )
            session.add(swift_code)
        await session.commit()

def run_seed_data() -> None:
    """
    Runs the asynchronous seeding operation, used in entrypoint for Docker.
    """
    asyncio.run(seed_data())

if __name__ == "__main__":
    run_seed_data()