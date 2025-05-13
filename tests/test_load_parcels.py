from pathlib import Path

import pandas as pd
import pytest

from mapviewer import load_parcels

# Use the exact same path the script writes to
OUTPUT_XLS = load_parcels.OUTPUT_XLS


@pytest.fixture(autouse=True)
def clean_up_excel():
    """
    Remove the Excel file before *and* after each test so runs are independent.
    The file handle is only released after pandas closes it, so we delete
    it *after* the test has finished.
    """
    if OUTPUT_XLS.exists():
        OUTPUT_XLS.unlink()
    yield
    if OUTPUT_XLS.exists():
        OUTPUT_XLS.unlink()


def test_load_parcels_creates_excel():
    """The script should create an Excel workbook with the right sheets/columns."""
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
