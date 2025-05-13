from pathlib import Path

import pandas as pd
import pytest

from mapviewer import load_parcels

# Use the exact same path the script writes to
OUTPUT_XLS = load_parcels.OUTPUT_XLS


@pytest.fixture(autouse=True)
def clean_up_excel():
    """
    Fixture to clean up the generated Excel file before and after each test.

    Ensures test isolation by:
      - Deleting the Excel file if it already exists before the test
      - Deleting the file again after the test (in case it was created)

    This avoids interference from previous test runs.
    """
    if OUTPUT_XLS.exists():
        OUTPUT_XLS.unlink()
    yield
    if OUTPUT_XLS.exists():
        OUTPUT_XLS.unlink()

def test_load_parcels_creates_excel():
    """
    Test that verifies the output of load_parcels.main().

    Ensures:
      - The Excel file is created after running the script
      - The expected sheets ('Parcelas_2024', 'Parcelas_2023') exist
      - Each sheet contains the column 'geometry_wkt'

    Raises:
      AssertionError: if the Excel file, sheets, or column are missing
    """
    # 1) Run the production script
    load_parcels.main()

    # 2) Check the file exists
    assert OUTPUT_XLS.is_file(), "Output Excel file was not created."

    # 3) Verify sheet names (make sure the handle is closed with a context manager)
    with pd.ExcelFile(OUTPUT_XLS) as book:
        assert {"Parcelas_2024", "Parcelas_2023"} <= set(book.sheet_names)

    # 4) Verify `geometry_wkt` column exists in both sheets
    for sheet in ("Parcelas_2024", "Parcelas_2023"):
        df = pd.read_excel(OUTPUT_XLS, sheet_name=sheet)
        assert "geometry_wkt" in df.columns, f"'geometry_wkt' missing in {sheet}"