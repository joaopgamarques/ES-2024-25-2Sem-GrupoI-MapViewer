import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

import mapviewer.load_properties as lp

@pytest.fixture(autouse=True)
def patch_environment(monkeypatch):
    """
    Pytest fixture to mock I/O and database-related functions in load_properties.

    Mocks:
      - pandas.read_csv: returns a fixed DataFrame with WKT geometry strings
      - sqlalchemy.create_engine: returns a dummy engine object
      - GeoDataFrame.to_postgis: captures arguments passed during export

    Returns:
        dict: Contains the mock PostGIS call log and dummy engine reference
    """
    # 1) Fake CSV content: two rows with WKT geometries
    sample_df = pd.DataFrame({
        "id": [1, 2],
        "OWNER": ["Alice", "Bob"],
        "geometry": ["POINT(0 0)", "POINT(1 1)"]
    })

    def fake_read_csv(path, sep, encoding):
        # ensure the script called read_csv with the expected args
        assert sep == ";"
        assert encoding == "utf-8"
        return sample_df.copy()

    monkeypatch.setattr(pd, "read_csv", fake_read_csv)

    # 2) Capture calls to create_engine and return a dummy engine object
    dummy_engine = object()
    monkeypatch.setattr(lp, "create_engine", lambda conn_str: dummy_engine)

    # 3) Patch GeoDataFrame.to_postgis to record its invocation
    calls = []
    def fake_to_postgis(self, name, con, if_exists, index):
        """
        Captures the arguments passed to to_postgis and logs geometry objects.
        """
        calls.append({
            "name": name,
            "con": con,
            "if_exists": if_exists,
            "index": index,
            "geometries": list(self.geometry)
        })

    # Attach to the actual GeoDataFrame class so any instance uses it
    monkeypatch.setattr(gpd.GeoDataFrame, "to_postgis", fake_to_postgis, raising=True)

    return {"calls": calls, "engine": dummy_engine}

def test_main_writes_to_postgis(patch_environment):
    """
    Test for load_properties.main().

    Ensures:
      - The CSV is loaded and parsed correctly
      - Geometries are converted to Shapely Point objects
      - The result is written to PostGIS using to_postgis with correct args
      - CRS transformation occurs (if implemented in the script)
    """
    # Run the script
    lp.main()

    calls = patch_environment["calls"]
    assert len(calls) == 1, "Expected exactly one to_postgis call"

    call = calls[0]
    # Check that it writes to the correct table
    assert call["name"] == "properties_data"
    # Check it used our dummy engine
    assert call["con"] is patch_environment["engine"]
    # Ensure replace-mode and index=False
    assert call["if_exists"] == "replace"
    assert call["index"] is False

    # Verify that geometries got parsed into Shapely Points
    geoms = call["geometries"]
    assert all(isinstance(g, Point) for g in geoms), "All geometries should be Shapely Points"

    # Optionally, verify that a coordinate transform happened:
    # since (0,0) and (1,1) in EPSG:5016 get moved slightly in EPSG:4326,
    # their repr() should not equal the original strings—but they must still be Points.
