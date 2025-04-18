import re
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.swift_code import SwiftCode
from app.schemas.swift_code import (
    BranchSwiftCodeResponse,
    FullBranchSwiftCodeResponse,
    HeadquarterSwiftCodeResponse,
    SwiftCodeCreate,
    CountrySwiftCodesResponse
)

router = APIRouter()

@router.get("/{swift_code}")
async def get_swift_code(swift_code: str, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    Retrieve details of a single SWIFT code. If the code represents a headquarters (ends with "XXX"),
    include a list of SWIFT codes that share the first 8 characters (branches).
    """

    # Using uppercase for safety
    query = select(SwiftCode).where(SwiftCode.swift_code == swift_code.upper())
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Swift code not found")

    # Headquarter Logic
    if record.swift_code.endswith("XXX"):
        head_prefix = record.swift_code[:8]
        
        branch_query = select(SwiftCode).where(
            SwiftCode.swift_code.startswith(head_prefix),
            SwiftCode.swift_code != record.swift_code
        )
        branch_result = await db.execute(branch_query)
        branch_records = branch_result.scalars().all()
        
        # Create branch responses using the model that skips countryName
        branches = [BranchSwiftCodeResponse.from_orm(branch) for branch in branch_records]
        
        base_data = {
            "address": record.address,
            "bank_name": record.bank_name,
            "country_iso2": record.country_iso2,
            "country_name": record.country_name,
            "is_headquarter": record.is_headquarter,
            "swift_code": record.swift_code,
        }
        hq_response = HeadquarterSwiftCodeResponse(**base_data, branches=branches)
        return JSONResponse(content=hq_response.model_dump(by_alias=False))
    
    # Branch Logic
    else:
        # Using FullBranchSwiftCodeResponse model instead, to include CountryName
        branch_response = FullBranchSwiftCodeResponse.from_orm(record)
        return JSONResponse(content=branch_response.model_dump(by_alias=False))


@router.get("/country/{country_iso2}", response_model=CountrySwiftCodesResponse)
async def get_swift_codes_by_country(country_iso2: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all SWIFT codes for a given country (both headquarters and branches).
    """
    query = select(SwiftCode).where(SwiftCode.country_iso2 == country_iso2.upper())
    result = await db.execute(query)
    records = result.scalars().all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No SWIFT codes found for this country"
        )

    country_name = records[0].country_name  # Assuming DB consistency (potential edge case, refer to README)
    swift_codes = [BranchSwiftCodeResponse.from_orm(record) for record in records]

    return CountrySwiftCodesResponse(
        countryISO2=country_iso2.upper(),
        countryName=country_name,
        swiftCodes=swift_codes
    )


@router.post("", response_model=dict)
async def create_swift_code(entry: SwiftCodeCreate, db: AsyncSession = Depends(get_db)):
    """
    Add a new SWIFT code entry to the database.
    """

    # Validation & Exception logic could be modulated further for code clarity & maintenance (refer to README)
    swift = entry.swiftCode
    if swift != swift.upper():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A SWIFT code must be uppercase.")

    if entry.isHeadquarter and not swift.endswith("XXX"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="For a headquarter entry, the swiftCode must end with 'XXX'."
        )
    
    if not re.fullmatch(r'[A-Z0-9]+', swift):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SWIFT code must contain only uppercase letters and digits (A-Z, 0-9)."
        )

    new_record = SwiftCode(
        swift_code=entry.swiftCode,
        bank_name=entry.bankName,
        address=entry.address,
        country_iso2=entry.countryISO2.upper(),
        country_name=entry.countryName.upper(),
        is_headquarter=entry.isHeadquarter
    )
    db.add(new_record)

    try:
        await db.commit()
        await db.refresh(new_record)
        return {"message": f"Swift code created successfully with ID {new_record.id}"}
    
    except IntegrityError as e:
        await db.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A SWIFT code with this value already exists."
            )
        
        # Fallback, in case it's a different IntegrityError
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create record: {str(e)}"
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to create record: {str(e)}")


@router.delete("/{swift_code}", response_model=dict)
async def delete_swift_code(swift_code: str, db: AsyncSession = Depends(get_db)):
    """
    DELETE a SWIFT code entry from database.
    """

    query = select(SwiftCode).where(SwiftCode.swift_code == swift_code.upper())
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Swift code not found")

    await db.delete(record)

    try:
        await db.commit()
        return {"message": f"Swift code {swift_code} deleted successfully"}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to delete record: {str(e)}")