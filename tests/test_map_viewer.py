import pytest
from pathlib import Path
import shutil

import mapviewer.map_viewer as map_viewer


@pytest.fixture
def mock_csv(tmp_path, monkeypatch):
    """
    Prepare a mock environment for testing map_viewer.py using a temporary CSV.

    This fixture creates:
      - A temporary CSV file `Madeira-Moodle-2.0.csv` with test parcel data
      - A temporary HTML output path for the Folium map

    It also monkeypatches:
      - `map_viewer.CSV_FILE` to point to the temp CSV
      - `map_viewer.OUT_HTML` to redirect map output to a temp path

    Args:
        tmp_path (pathlib.Path): Pytest fixture for isolated filesystem access
        monkeypatch: Pytest monkeypatch utility

    Returns:
        pathlib.Path: Path to the expected HTML output file
    """
    # Sample semicolon-delimited CSV with WKT geometries
    csv_data = (
        "OBJECTID;OWNER;geometry\n"
        "1;Alice;POINT(-16.91 32.66)\n"
        "2;Bob;POINT(-16.92 32.67)\n"
    )

    # Paths
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "Madeira-Moodle-2.0.csv"
    csv_path.write_text(csv_data, encoding="utf-8")

    html_path = tmp_path / "map_properties.html"

    # Patch constants in map_viewer
    monkeypatch.setattr(map_viewer, "CSV_FILE", csv_path)
    monkeypatch.setattr(map_viewer, "OUT_HTML", html_path)

    return html_path

def test_main_creates_map_html(mock_csv):
    """
    Integration test for `map_viewer.main()`.

    Verifies:
      - That the function executes end-to-end without error
      - That the HTML map file is generated at the expected location
      - That the output contains valid Folium markup and known attribute content

    Args:
        mock_csv (pathlib.Path): Path to the patched HTML output file (from fixture)

    Raises:
        AssertionError: If the map is not created or expected content is missing
    """
    # Run the map creation
    map_viewer.main()

    # Check that the map was created
    assert mock_csv.exists(), "Expected HTML file was not created."

    # Basic content check
    content = mock_csv.read_text(encoding="utf-8")
    assert "<div class=\"folium-map\"" in content, "Folium map container missing."
    assert "Alice" in content and "Bob" in content, "Expected owner names missing from tooltip content."
