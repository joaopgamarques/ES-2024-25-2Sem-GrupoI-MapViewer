#!/usr/bin/env python3
import geopandas as gpd
import pandas as pd


def main():
    """
    Main entry point for exporting parcel layers from a GeoPackage to an Excel workbook.

    Steps:
      1. Read the 2024 parcel layer from the GeoPackage into a GeoDataFrame.
      2. Read the 2023 parcel layer from the GeoPackage into a GeoDataFrame.
      3. Optionally convert geometry to WKT strings for readability in Excel.
      4. Create an Excel workbook with two sheets: one for 2024 and one for 2023 data.
      5. Drop GeoPandas geometry objects and include only WKT or other attributes.
      6. Save the Excel file to disk.

    :return: None
    """
    # File paths and layer names
    gpkg_path = "data/Parcelas_madeira.gpkg"
    layer_2024 = "P_madeira_2024"
    layer_2023 = "P_madeira_2023"
    output_excel = "data/Parcelas_Madeira.xlsx"

    # 1) Load 2024 parcel layer
    gdf_2024 = gpd.read_file(gpkg_path, layer=layer_2024)

    # 2) Load 2023 parcel layer
    gdf_2023 = gpd.read_file(gpkg_path, layer=layer_2023)

    # 3) Convert geometries to WKT for Excel readability
    gdf_2024["geometry_wkt"] = gdf_2024.geometry.apply(lambda geom: geom.wkt if geom else None)
    gdf_2023["geometry_wkt"] = gdf_2023.geometry.apply(lambda geom: geom.wkt if geom else None)

    # 4) Write dataframes to an Excel workbook with two sheets
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        # Write the 2024 sheet, dropping the native geometry column
        gdf_2024.drop(columns="geometry").to_excel(
            writer,
            sheet_name="Parcelas_2024",
            index=False
        )
        # Write the 2023 sheet, dropping the native geometry column
        gdf_2023.drop(columns="geometry").to_excel(
            writer,
            sheet_name="Parcelas_2023",
            index=False
        )

    # Notify completion
    print(f"Excel file '{output_excel}' created successfully!")


if __name__ == "__main__":
    main()
