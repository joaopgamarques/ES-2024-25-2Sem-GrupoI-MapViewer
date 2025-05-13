#!/usr/bin/env python3
import geopandas as gpd
import folium
from sqlalchemy import create_engine


def main():
    """
    Main entry point for generating an interactive property map and saving it as HTML.

    Steps:
      1. Connect to the Postgres database using SQLAlchemy.
      2. Execute a SQL query to load geometry and attribute data into a GeoDataFrame.
      3. Ensure the GeoDataFrame has the correct WGS84 CRS (EPSG:4326).
      4. Create a Folium map centered on a predefined location.
      5. Overlay GeoJSON features with tooltips showing object IDs and owners.
      6. Save the map to an HTML file.

    :return: None
    """
    # Create a SQLAlchemy engine for the Postgres database
    engine = create_engine("postgresql://postgres:ES2425GI@localhost:5432/postgres")

    # Define SQL query for retrieving properties data
    sql = '''
      SELECT
        "OBJECTID" AS objectid,
        "OWNER"    AS owner,
        geometry
      FROM public.properties_data;
    '''

    # Load the query results into a GeoDataFrame
    gdf = gpd.read_postgis(sql, engine, geom_col="geometry")

    # If no CRS is detected, set it explicitly to WGS84 (EPSG:4326)
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326, allow_override=True)

    # Initialize a Folium map centered at latitude 32.65, longitude -16.9
    m = folium.Map(location=[32.65, -16.9], zoom_start=12)

    # Add GeoJSON layer with tooltips displaying 'objectid' and 'owner' fields
    folium.GeoJson(
        gdf,
        name="Properties",
        tooltip=folium.GeoJsonTooltip(fields=["objectid", "owner"])
    ).add_to(m)

    # Save the interactive map to an HTML file
    m.save("map.html")
    print("Map has been saved to map.html.")


if __name__ == "__main__":
    main()
