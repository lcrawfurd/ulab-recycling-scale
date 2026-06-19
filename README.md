# Which countries could safely recycle their own used lead-acid batteries?

Preliminary working figures (draft, subject to change).

**Live page:** https://lcrawfurd.github.io/ulab-recycling-scale/

Safe lead-acid battery recycling only pays at scale. We estimate annual used lead-acid battery
(ULAB) volume for 57 low- and middle-income countries, compare it with the scale a safe plant
needs, and classify what each country should do: recycle at home (conventional plant >= ~50k t/yr,
or a modular plant from ~12k), export to a bigger neighbour, or — for a few small islands — neither.

## Figures on the page
- `fig1_volume_vs_threshold.png` — countries ranked by ULAB volume vs the 12k / 24k / 50k band
- `fig6_status_map.png` — what each country should do (recycle at home / export / stuck), shown at both thresholds

## Code (`code/`)
- `regions.py` — shared contiguous-club grouping + colours (used by the exploratory club figures)
- `01_ulab_volume_vs_threshold.py` — lead generation to whole-battery ULAB tonnes; classify vs band; figure 1
- `02_regional_clubs.py`, `04_map_clubs.py` — exploratory contiguous-"club" pooling view
- `03_map.py` — exploratory viability choropleth (3 bands)
- `05_status_map.py` — status classification (home / export / pool / stuck) using border adjacency; the status map
Requires Python 3 with `pandas`, `geopandas`, `matplotlib`.

## Data (`data/`)
- `ulab_volume_by_country.csv`, `country_status.csv` — the numbers behind the page figures (`clubs.csv` is from the club exploration).
- **Not redistributed here:** `sites_vehicles.dta`, the vehicle-demand model intermediate from the published
  "Beyond hotspots" paper (script 01's input). Available from the authors / paper replication.
- **Not redistributed here:** the Natural Earth `ne_10m_admin_0_countries` shapefile used by the maps —
  download from naturalearthdata.com into `data/geo/`.

## Sources
Volume estimates: vehicle-demand model in Crawfurd, Mitchell & Hu (2026), "Beyond hotspots:
estimating population lead exposure from battery recycling", *Environmental Pollution*.
Safe-recycling scale thresholds: USAID / Dalberg *ULAB Recycling Assessment* (2024) and a
modular plant installed in Côte d'Ivoire (2024).
