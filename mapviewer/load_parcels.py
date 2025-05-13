#!/usr/bin/env python3
"""
Export the 2024 and 2023 parcel layers from the GeoPackage
`data/Parcelas_madeira.gpkg` into an Excel workbook that lives in `data/`.
The Excel file gets two sheets (Parcelas_2024, Parcelas_2023) and an extra
column `geometry_wkt` with the geometry in WKT format.
"""
from pathlib import Path
import geopandas as gpd
import pandas as pd

# ------------------------------------------------------------------ #
# Build absolute paths that never depend on the current working dir
HERE       = Path(__file__).resolve().parent          # …/mapviewer
DATA_DIR   = HERE.parent / "data"                     # …/data
GPKG_PATH  = DATA_DIR / "Parcelas_madeira.gpkg"
OUTPUT_XLS = DATA_DIR / "Parcelas_Madeira.xlsx"
# ------------------------------------------------------------------ #

LAYER_2024 = "P_madeira_2024"
LAYER_2023 = "P_madeira_2023"


def main() -> None:
    """Run the export."""
    # 1) Read parcel layers
    gdf_2024 = gpd.read_file(GPKG_PATH, layer=LAYER_2024)
    gdf_2023 = gpd.read_file(GPKG_PATH, layer=LAYER_2023)

    # 2) Add a WKT column (handy inside Excel)
    gdf_2024["geometry_wkt"] = gdf_2024.geometry.apply(lambda g: g.wkt if g else None)
    gdf_2023["geometry_wkt"] = gdf_2023.geometry.apply(lambda g: g.wkt if g else None)

    # 3) Write to Excel (drop the heavy geometry column)
    with pd.ExcelWriter(OUTPUT_XLS, engine="openpyxl") as xls:
        gdf_2024.drop(columns="geometry").to_excel(xls, sheet_name="Parcelas_2024", index=False)
        gdf_2023.drop(columns="geometry").to_excel(xls, sheet_name="Parcelas_2023", index=False)

    print(f"Excel file “{OUTPUT_XLS}” created successfully!")


if __name__ == "__main__":
    main()
