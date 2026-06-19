# Which countries could safely recycle their own used lead-acid batteries?

Preliminary working figures (draft, subject to change).

**Live page:** https://lcrawfurd.github.io/ulab-recycling-scale/

Safe lead-acid battery recycling only pays at scale. These figures estimate annual used
lead-acid battery (ULAB) volume for 57 low- and middle-income countries, compare it with the
scale a safe recycling plant needs, and ask which sub-threshold countries could reach that
scale by pooling regionally.

## Figures
- `fig1_volume_vs_threshold.png` — countries ranked by ULAB volume vs the 12k / 24k / 50k band
- `fig2_regional_clubs.png` — pooled regional volume vs the band
- `fig3_map.png` — world map coloured by individual viability
- `fig4_map_clubs.png` — world map of proposed regional "clubs"

## Code (`code/`)
- `01_ulab_volume_vs_threshold.py` — convert lead generation to whole-battery ULAB tonnes; classify vs band; figure 1
- `02_regional_clubs.py` — aggregate into regions; rescued vs orphan; figure 2
- `03_map.py` — viability choropleth; figure 3
- `04_map_clubs.py` — clubs choropleth; figure 4

Requires Python 3 with `pandas`, `geopandas`, `matplotlib`.

## Data (`data/`)
- `ulab_volume_by_country.csv`, `regional_clubs.csv` — the derived numbers behind the figures (included).
- **Not redistributed here:** `sites_vehicles.dta`, the vehicle-demand model intermediate from the
  published "Beyond hotspots" paper (script 01's input). Available from the authors / paper replication.
- **Not redistributed here:** the Natural Earth `ne_10m_admin_0_countries` shapefile used by the maps —
  download from naturalearthdata.com into `data/geo/`.

## Sources
Volume estimates: vehicle-demand model in Crawfurd, Mitchell & Hu (2026), "Beyond hotspots:
estimating population lead exposure from battery recycling", *Environmental Pollution*.
Safe-recycling scale thresholds: USAID / Dalberg *ULAB Recycling Assessment* (2024) and a
modular plant installed in Côte d'Ivoire (2024).
