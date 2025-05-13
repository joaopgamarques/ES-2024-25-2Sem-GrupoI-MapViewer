#!/usr/bin/env python3
"""
load_properties.py
==================

Reads a semicolon-delimited CSV file containing WKT geometries,
converts it to a GeoDataFrame, and writes the result to a PostGIS table.

CSV Requirements:
  - File path: ../data/Madeira-Moodle-1.2.csv
  - Must use ';' as delimiter
  - Include a column named 'geometry' with WKT strings
  - Coordinates should be in EPSG:5016 (Portugal Mainland)

Output:
  - Table `properties_data` in PostGIS database (EPSG:4326)
"""
import pandas as pd
import geopandas as gpd
from shapely import wkt
from sqlalchemy import create_engine

def main():
    """
    Load geometries from CSV and write to PostGIS.

    Steps:
      1. Read a semicolon-delimited CSV file containing WKT geometry strings into a Pandas DataFrame.
      2. Parse the WKT geometry column into Shapely geometry objects.
      3. Construct a GeoPandas GeoDataFrame with the proper geometry column.
      4. Assign the source CRS (EPSG:5016) and reproject to WGS84 (EPSG:4326).
      5. Connect to a Postgres database via SQLAlchemy.
      6. Write the GeoDataFrame to a PostGIS table, replacing any existing table.

    Raises:
        FileNotFoundError: If the CSV path is incorrect or inaccessible
        ValueError: If the geometry column cannot be parsed as WKT
        sqlalchemy.exc.SQLAlchemyError: If the database connection or write fails
    """
    # Path to the CSV file containing data and WKT geometries
    csv_file_path = "../data/Madeira-Moodle-1.2.csv"

    # Read CSV into DataFrame (semicolon separator, UTF-8 encoding)
    df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')

    # Convert WKT strings in the 'geometry' column to Shapely geometry objects
    df['geometry'] = df['geometry'].apply(wkt.loads)

    # Create a GeoDataFrame, specifying the geometry column
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Set the source CRS to EPSG:5016 (Portugal Mainland) if not already defined
    gdf = gdf.set_crs(epsg=5016, allow_override=True)

    # Reproject geometries to WGS84 (EPSG:4326) for PostGIS storage
    gdf = gdf.to_crs(epsg=4326)

    # Create a SQLAlchemy engine for the Postgres database
    engine = create_engine("postgresql://postgres:ES2425GI@localhost:5432/postgres")

    # Write the GeoDataFrame to PostGIS, replacing any existing 'properties_data' table
    gdf.to_postgis(
        name='properties_data',
        con=engine,
        if_exists='replace',  # options: 'replace' or 'append'
        index=False
    )

    # Inform the user upon successful completion
    print("Data has been successfully loaded into PostGIS (properties_data).")


if __name__ == "__main__":
    main()
