import pandas as pd
import re
from app.core.config import settings

def parse_xlsx(file_path: str) -> pd.DataFrame:
    """
    Reads an XLSX file and returns a DataFrame.
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        return df
    except Exception as e:
        raise RuntimeError(f"Error reading XLSX file at {file_path}: {str(e)}") from e
    
def parse_csv(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file at {file_path}: {str(e)}") from e
    
def parse_google_sheet(sheet_url: str) -> pd.DataFrame:
    """
    Loads a public Google Sheet as a pandas DataFrame.

    This function extracts the spreadsheet ID and GID (sheet tab ID) from the URL
    and constructs a direct CSV export link.

    Args:
        sheet_url (str): Full URL to the public Google Sheet.

    Returns:
        pd.DataFrame: A DataFrame containing the sheet's contents.
    """
    # Extract spreadsheet ID
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
    if not match:
        raise ValueError("Invalid Google Sheets URL: Couldn't extract spreadsheet ID.")
    spreadsheet_id = match.group(1)

    # Extract gid if available or defaults to 0
    gid_match = re.search(r'(?:[?&]gid=|#gid=)(\d+)', sheet_url)
    gid = gid_match.group(1) if gid_match else '0'

    # Build CSV export URL
    csv_url = (
        f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export'
        f'?format=csv&id={spreadsheet_id}&gid={gid}'
    )

    df = pd.read_csv(csv_url)
    return df

def parse_data() -> pd.DataFrame:
    """
    Reads the INPUT_SOURCE environment variable and calls the appropriate
    parsing function. Default source is 'xlsx'.
    """
    input_source = settings.INPUT_SOURCE.lower()
    
    if input_source == "xlsx":
        return parse_xlsx(settings.XLSX_FILE_PATH)
    
    elif input_source == "csv":
        return parse_csv(settings.CSV_FILE_PATH)
    
    elif input_source == "google":
        if not settings.GOOGLE_SHEET_URL:
            raise ValueError("Google Sheets URL not specified in environment variable.")
        return parse_google_sheet(settings.GOOGLE_SHEET_URL)
    
    else:
        raise ValueError(f"Unsupported type of input source: {input_source}")