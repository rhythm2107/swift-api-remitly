from typing import List, Optional, Union
from pydantic import BaseModel, Field

class BranchSwiftCodeResponse(BaseModel):
    address: Optional[str] = Field(None)
    bankName: str = Field(..., alias="bank_name")
    countryISO2: str = Field(..., alias="country_iso2")
    isHeadquarter: bool = Field(..., alias="is_headquarter")
    swiftCode: str = Field(..., alias="swift_code")

    class Config:
        from_attributes = True
        validate_by_name = True


class FullBranchSwiftCodeResponse(BaseModel):
    address: Optional[str] = Field(None)
    bankName: str = Field(..., alias="bank_name")
    countryISO2: str = Field(..., alias="country_iso2")
    countryName: str = Field(..., alias="country_name")
    isHeadquarter: bool = Field(..., alias="is_headquarter")
    swiftCode: str = Field(..., alias="swift_code")
    
    class Config:
        from_attributes = True
        validate_by_name = True


class HeadquarterSwiftCodeResponse(BaseModel):
    address: Optional[str] = Field(None)
    bankName: str = Field(..., alias="bank_name")
    countryISO2: str = Field(..., alias="country_iso2")
    countryName: str = Field(..., alias="country_name")
    isHeadquarter: bool = Field(..., alias="is_headquarter")
    swiftCode: str = Field(..., alias="swift_code")
    branches: List[BranchSwiftCodeResponse]

    class Config:
        from_attributes = True
        validate_by_name = True


class SwiftCodeCreate(BaseModel):
    address: Optional[str] = None
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str

    class Config:
        json_schema_extra = {
            "example": {
                "address": "Example Street 12/34",
                "bankName": "Example Bank",
                "countryISO2": "US",
                "countryName": "UNITED STATES",
                "isHeadquarter": True,
                "swiftCode": "EXAMPLEXXX" # Ends with "XXX" = Headquarter
            }
        }


class CountrySwiftCodesResponse(BaseModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[BranchSwiftCodeResponse]