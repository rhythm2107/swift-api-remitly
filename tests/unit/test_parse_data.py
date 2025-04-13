import pandas as pd

from app.ingestion.parse_data import parse_csv, parse_xlsx, parse_google_sheet

def test_parse_csv(tmp_path):
    """
    Test parse_csv by creating a temp CSV file with sample data,
    calling parse_csv, and asserting that the resulting DataFrame matches 
    the expected DataFrame.
    """
    csv_content = "col1,col2\n1,2\n3,4"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)
    
    df = parse_csv(str(csv_file))
    
    expected_df = pd.DataFrame({
        "col1": [1, 3],
        "col2": [2, 4]
    })
    
    pd.testing.assert_frame_equal(df, expected_df)


def test_parse_xlsx(tmp_path):
    """
    Test parse_xlsx by writing a sample DataFrame to a temporary XLSX file 
    (using the 'openpyxl' engine), calling parse_xlsx, and asserting that 
    the DataFrame returned matches the expected DataFrame.
    """
    expected_df = pd.DataFrame({
        "col1": [10, 20],
        "col2": [30, 40]
    })
    
    xlsx_file = tmp_path / "test.xlsx"
    expected_df.to_excel(xlsx_file, index=False, engine='openpyxl')
    
    df = parse_xlsx(str(xlsx_file))
    
    pd.testing.assert_frame_equal(df, expected_df)


def test_parse_google_sheet(monkeypatch):
    """
    Test the Google Sheets parser by monkeypatching pandas.read_csv
    so that we don’t perform a real network call.
    """
    dummy_df = pd.DataFrame({
        "col1": [5, 6],
        "col2": [7, 8]
    })
    
    def fake_read_csv(url, *args, **kwargs):
        # Verify that URL was correctly converted to an export format
        assert "export?format=csv" in url
        return dummy_df

    monkeypatch.setattr(pd, "read_csv", fake_read_csv)
    dummy_url = "https://docs.google.com/spreadsheets/d/TESTSPREADSHEETID/expsort?format=cXsv&id=TESTSPREADSHEETID&gid=0"
    df = parse_google_sheet(dummy_url)

    pd.testing.assert_frame_equal(df, dummy_df)