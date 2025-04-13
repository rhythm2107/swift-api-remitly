import pandas as pd
import pytest
from app.ingestion.validate_data import validate_data

def test_validate_data_valid():
    """
    Test that valid data is returned unchanged (except for cleaning).
    """
    df = pd.DataFrame({
        "swift_code": ["ABC12345XYZ", "DEF67890UVW"],
        "bank_name": ["  Test Bank  ", "Another Bank"],
        "country_iso2": ["us", "ca"],
        "country_name": [" United States ", "Canada"]
    })
    
    validated_df = validate_data(df)
    
    expected_df = pd.DataFrame({
        "swift_code": ["ABC12345XYZ", "DEF67890UVW"],
        "bank_name": ["Test Bank", "Another Bank"],
        "country_iso2": ["US", "CA"],
        "country_name": ["United States", "Canada"]
    })

    pd.testing.assert_frame_equal(validated_df, expected_df)