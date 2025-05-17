# ES-Project: Python GIS & Mapping Utilities

This directory contains **Python** scripts for working with geographic data in Madeira, performing tasks such as:

1. **GeoPackage → Excel** export (`load_parcels.py`)
2. **CSV (WKT) → PostGIS** import (`load_properties.py`)
3. **CSV (WKT) → Folium Map** generation (`map_viewer.py`)
4. **Automated tests** for each script (using **pytest**)

---

## Table of Contents

* [Overview](#overview)
* [Scripts](#scripts)

  * [1. `load_parcels.py`](#1-load_parcelspy)
  * [2. `load_properties.py`](#2-load_propertiespy)
  * [3. `map_viewer.py`](#3-map_viewerpy)
* [Test Classes](#test-classes)
* [Dependencies & Setup](#dependencies--setup)
* [Running Tests & Coverage](#running-tests--coverage)
* [Contributors](#contributors)

---

## Overview

These Python utilities complement the main project by performing geospatial data **transformations** and **visualisations**. They rely on:

* **GeoPandas** & **Shapely** – geometry handling and CRS transformations.
* **Pandas** – tabular data I/O (CSV / Excel).
* **Folium** – interactive HTML maps.
* **SQLAlchemy** & **PostGIS** – database integration (optional).

---

## Scripts

### 1. `load_parcels.py`

**Objective:** Export 2024 / 2023 parcel layers from a local **GeoPackage** to an Excel workbook with separate sheets.

**Workflow:**

1. Read `Parcelas_madeira.gpkg` in `data/` (layers `P_madeira_2024` & `P_madeira_2023`).
2. Convert geometries to **WKT** strings (`geometry_wkt`).
3. Drop the binary geometry column to reduce file size.
4. Write each layer to its own sheet in `Parcelas_Madeira.xlsx`.

**Output:** `data/Parcelas_Madeira.xlsx` (sheets `Parcelas_2024` & `Parcelas_2023`).

---

### 2. `load_properties.py`

**Objective:** Import a CSV containing WKT geometries into a **PostGIS** table.

**Workflow:**

1. Read `Madeira-Moodle-1.2.csv` (semicolon‑delimited).
2. Parse the `geometry` column with `shapely.wkt.loads`.
3. Build a `GeoDataFrame` (start in **EPSG 5016**, then reproject to **EPSG 4326**).
4. Use `GeoDataFrame.to_postgis()` to write to table `properties_data` (replace or append).

**Output:** PostGIS table **`properties_data`**.

---

### 3. `map_viewer.py`

**Objective:** Generate an **interactive Folium map** from a CSV that stores WKT polygons/points.

**Workflow:**

1. Read `Madeira-Moodle-2.0.csv` in `data/`.
2. Convert to a `GeoDataFrame` in **EPSG 4326**.
3. Create a Folium map centred on Madeira and add a GeoJSON layer with tool‑tips.
4. Save as `map_properties.html` in the project root.

**Output:** `map_properties.html` – open in any browser.

---

## Test Classes

We use **pytest** for each script.

| Test file                 | What it verifies                                    |
| ------------------------- | --------------------------------------------------- |
| `test_load_parcels.py`    | Excel file/sheets exist; `geometry_wkt` present.    |
| `test_load_properties.py` | CSV parsing & PostGIS write (DB calls mocked).      |
| `test_map_viewer.py`      | Generated HTML contains expected geometries/owners. |

> *Mocks are used for file I/O and database interactions when necessary.*

---

## Dependencies & Setup

1. **Python 3.8+** recommended.
2. Install libraries:

```bash
pip install geopandas shapely folium pandas openpyxl sqlalchemy psycopg2 pytest
```

| Package                   | Purpose                        |
| ------------------------- | ------------------------------ |
| `geopandas`               | Geometry & CRS transformations |
| `shapely`                 | WKT parsing                    |
| `folium`                  | Map generation                 |
| `openpyxl`                | Write Excel files              |
| `sqlalchemy` + `psycopg2` | PostGIS connectivity           |
| `pytest`                  | Test framework                 |

**File paths** – scripts expect input in `data/`. Adjust paths if your structure differs.

### PostGIS (optional)

Requires PostgreSQL with the **PostGIS** extension enabled. Update the connection string in `load_properties.py` if needed:

```python
create_engine("postgresql://postgres:ES2425GI@localhost:5432/postgres")
```

---

## Running Tests & Coverage

Run all tests:

```bash
pytest -v
```

Generate coverage (terminal):

```bash
pytest --cov=. --cov-report=term-missing --cov-branch
```

Generate HTML coverage report:

```bash
pytest --cov=. --cov-report=html
# open htmlcov/index.html in your browser
```

---

## Contributors

| Name                | Student # | GitHub                                               |
| ------------------- | --------- | ---------------------------------------------------- |
| João Pedro Marques  | 105377    | [@joaopgamarques](https://github.com/joaopgamarques) |
| José Mesquita       | 106281    | [@jlgmaIscte](https://github.com/jlgmaIscte)         |
| Bárbara Albuquerque | 106807    | [@bfaae](https://github.com/bfaae)                   |
| Jéssica Vieira      | 110812    | [@Je-ssi-ca](https://github.com/Je-ssi-ca)           |


These Python scripts are a complementary extension to our main **Java‑based** project: *ES‑Project‑TerritoryManagement*. Feel free to open issues or submit pull requests!
