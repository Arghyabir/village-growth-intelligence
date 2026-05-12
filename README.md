# Village Economic Growth Intelligence
**Kritter Software Technologies — Candidate Assignment**

---

## Project Overview

This project builds an end-to-end intelligence system to identify the **Top 100 economically growing villages in India** over the last 5 years (2019–2024), using satellite-derived signals and publicly available datasets.

---

## Folder Structure

```
kritter-assignment/
├── README.md                         ← You are here
├── requirements.txt                  ← Python dependencies
├── data/
│   ├── raw/                          ← Raw downloaded data (not committed to git)
│   └── processed/                    ← Cleaned, merged datasets
├── notebooks/
│   ├── 01_data_extraction.ipynb      ← Data sourcing & extraction
│   ├── 02_cleaning_processing.ipynb  ← Cleaning & feature engineering
│   ├── 03_scoring_ranking.ipynb      ← Scoring model & ranking
│   └── 04_visualization.ipynb        ← Maps, charts, interactive outputs
├── scripts/
│   ├── 01_extract.py                 ← Standalone extraction script
│   ├── 02_clean.py                   ← Standalone cleaning script
│   ├── 03_score.py                   ← Standalone scoring script
│   └── 04_visualize.py               ← Standalone visualization script
├── outputs/
│   ├── top_100_villages.csv          ← Final ranked output dataset
│   └── village_growth_map.html       ← Interactive Folium map
└── presentation/
    └── village_growth_intelligence.pptx
```

---

## Data Sources

| # | Dataset | Source | Use |
|---|---------|--------|-----|
| 1 | VIIRS Night-time Light (2019–2024) | [NASA Black Marble / GEE](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG) | Primary economic proxy |
| 2 | Village boundary shapefiles | [Datameet India Maps (GitHub)](https://github.com/datameet/maps) | Spatial unit of analysis |
| 3 | Census 2011 Village Directory | [Office of the Registrar General of India](https://censusindia.gov.in/) | Baseline population & infrastructure |
| 4 | PMAY-G Beneficiary Data | [pmayg.nic.in](https://pmayg.nic.in/) | Construction / housing proxy |
| 5 | MGNREGS Employment Data | [data.gov.in](https://data.gov.in/) | Rural economic activity |
| 6 | Landsat 8 NDVI | [USGS / Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) | Land use intensification |
| 7 | OpenStreetMap | [Overpass API](https://overpass-api.de/) | Road/building density change |

---

## How to Run

### 1. Set up environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run scripts in order

```bash
# Step 1: Extract data
python scripts/01_extract.py

# Step 2: Clean & process
python scripts/02_clean.py

# Step 3: Score & rank
python scripts/03_score.py

# Step 4: Visualize
python scripts/04_visualize.py
```

### 3. Or run interactively via notebooks

```bash
jupyter notebook notebooks/
```

### 4. Outputs

After running, you'll find:
- `outputs/top_100_villages.csv` — ranked list with all attributes
- `outputs/village_growth_map.html` — open in any browser for the interactive map

---

## Scoring Methodology Summary

Economic growth is measured using a **Composite Village Growth Index (CVGI)** with four signals:

| Signal | Weight | Rationale |
|--------|--------|-----------|
| Night-time Light Radiance Change (2019→2024) | 40% | Strong proxy for electrification, economic activity |
| NDVI Change (land use intensification) | 20% | Crop diversification, horticulture expansion |
| PMAY-G beneficiary density | 20% | Infrastructure investment & construction |
| MGNREGS workdays per capita | 20% | Rural wage employment signal |

Each signal is min-max normalized to [0, 1] before combining.

---

## Key Limitations

- Census 2011 is the most granular village-level dataset; some boundaries may have changed
- Night-time light data has ~500m resolution — small villages may have spillover from nearby towns
- PMAY and MGNREGS data reflects scheme enrollment, not direct economic output
- Analysis covers 2019–2024; COVID-19 (2020–21) may introduce noise in growth trends

---

## Requirements

See `requirements.txt`. Key packages:
- `pandas`, `numpy` — data processing
- `geopandas`, `shapely` — spatial operations
- `folium`, `plotly` — visualization
- `earthengine-api` — Google Earth Engine access (requires GEE account)
- `requests`, `tqdm` — data download utilities

---

## Contact

Assignment submitted by: **[Your Name]**
For queries: [INSERT EMAIL] | Subject: `Assignment Query – [Your Name]`
