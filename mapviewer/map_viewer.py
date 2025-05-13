#!/usr/bin/env python3
"""
Map From CSV Script
====================

Generates an interactive HTML map from a semicolon-delimited CSV file
containing WKT geometries (Madeira-Moodle-2.0.csv). No database connection
is required.

Requirements:
  - CSV file at <project_root>/data/Madeira-Moodle-2.0.csv
  - Semicolon (`;`) as the delimiter
  - A column named `geometry` with WKT strings
  - Coordinates in WGS-84 (EPSG:4326); if the CSV is still in
    EPSG:5016, uncomment the reprojection line in `main()`.

Output:
  - An HTML file `map_properties.html` in the project root.
"""
from pathlib import Path

import pandas as pd
import geopandas as gpd
import folium
from shapely import wkt

# ---------------------------------------------------------------------- #
# Define file paths relative to this script for portability
# ---------------------------------------------------------------------- #
HERE      = Path(__file__).resolve().parent       # Directory of this script
DATA_DIR  = HERE.parent / "data"                  # ../data directory
CSV_FILE  = DATA_DIR / "Madeira-Moodle-2.0.csv"  # Input CSV path
OUT_HTML  = HERE.parent / "map_properties.html"  # Output HTML path
# ---------------------------------------------------------------------- #

def main() -> None:
    """
    Main entry point: reads the CSV, parses geometries, builds a Folium map,
    and saves it as HTML.

    Steps:
      1. Load the CSV with pandas (semicolon delimiter, UTF-8 encoding).
      2. Parse the 'geometry' column from WKT to Shapely objects.
      3. Wrap in a GeoDataFrame with CRS EPSG:4326.
         (Uncomment the reprojection line if using EPSG:5016.)
      4. Initialize a Folium map centered on Madeira (lat 32.65, lon -16.9).
      5. Overlay the parcels as GeoJSON with tooltips for OBJECTID and OWNER.
      6. Save the interactive map to `map_properties.html`.

    Raises:
      FileNotFoundError: If the input CSV cannot be found.
      ValueError: If WKT parsing fails for any geometry.
    """
    # 1) Read the CSV into a pandas DataFrame
    df = pd.read_csv(CSV_FILE, sep=";", encoding="utf-8")

    # 2) Convert WKT strings to Shapely geometry objects
    df["geometry"] = df["geometry"].apply(wkt.loads)

    # 3) Create a GeoDataFrame and set CRS to WGS-84
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

    # If the source CSV uses EPSG:5016, uncomment this reprojection:
    # gdf = gdf.to_crs(epsg=4326)

    # 4) Build a Folium map centered on Madeira
    m = folium.Map(location=[32.65, -16.9], zoom_start=12)

    # 5) Add the GeoJSON layer with hover tooltips
    folium.GeoJson(
        gdf,
        name="Properties",
        tooltip=folium.GeoJsonTooltip(fields=["OBJECTID", "OWNER"]),
    ).add_to(m)

    # 6) Save the map to an HTML file and notify
    m.save(OUT_HTML)
    print(f"Interactive map saved to: {OUT_HTML}")


if __name__ == "__main__":
    main()
