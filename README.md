# Map From CSV Script

This Python script generates an interactive HTML map from a semicolon-delimited CSV file containing WKT geometries. It does **not** require a database—just local files and a standard Python environment.

---

## Features

- **Reads** a CSV (`Madeira-Moodle-2.0.csv`) from the `data/` folder (assumed to be at `<project_root>/data`).
- **Parses** WKT geometry strings (stored in a `geometry` column) into shapely objects.
- **Builds** a GeoDataFrame (using GeoPandas) with an EPSG:4326 coordinate reference system.
- **Generates** an interactive map using Folium, placing each geometry as a GeoJSON layer.
- **Saves** the map to `map_properties.html` in the project root. Open it in your browser to explore.

---

## Requirements

1. **Python 3.8+**  
2. **Libraries** (install via `pip install [package]`):
   - [pandas](https://pandas.pydata.org/)  
   - [geopandas](https://geopandas.org/)  
   - [folium](https://python-visualization.github.io/folium/)  
   - [shapely](https://shapely.readthedocs.io/)  

3. **CSV File**  
   - Must be located at `<project_root>/data/Madeira-Moodle-2.0.csv`.
   - Delimiter: `;` (semicolon).
   - Columns:
     - A **`geometry`** column containing valid WKT polygons or multipolygons.
     - (Optionally) **`OBJECTID`**, **`OWNER`**, etc., which appear in tooltips.

4. **Coordinate System**  
   - If already in **EPSG:4326** (WGS-84 lat/lon), no reprojection is needed.
   - If data is in **EPSG:5016**, uncomment the reprojection line in the script to convert to EPSG:4326.

---

## Installation & Setup

1. **Clone** or download this repository.
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
