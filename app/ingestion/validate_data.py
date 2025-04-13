import pandas as pd

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates and cleans the swift codes data.

    Returns the validated DataFrame if validation passes,
    otherwise, raises a ValueError with details.
    """
    errors = []

    required_columns = ["swift_code", "bank_name", "country_iso2", "country_name"]
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")
    
    for idx, row in df.iterrows():
        if pd.isna(row["bank_name"]) or str(row["bank_name"]).strip() == "":
            errors.append(f"Row {idx}: 'bank_name' is empty")

        if pd.isna(row["country_name"]) or str(row["country_name"]).strip() == "":
            errors.append(f"Row {idx}: 'country_name' is empty")

        if pd.isna(row["swift_code"]) or not (8 <= len(str(row["swift_code"])) <= 11):
            errors.append(f"Row {idx}: 'swift_code' must be 8 to 11 characters")

        if pd.isna(row["country_iso2"]) or len(str(row["country_iso2"]).strip()) != 2:
            errors.append(f"Row {idx}: 'country_iso2' must be 2 characters")
    
    if errors:
        raise ValueError("Data validation errors:\n" + "\n".join(errors))
    
    df["bank_name"] = df["bank_name"].str.strip()
    df["country_name"] = df["country_name"].str.strip()
    df["country_iso2"] = df["country_iso2"].str.upper()
    
    return df