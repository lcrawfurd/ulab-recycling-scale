"""World choropleth: estimated ULAB volume vs safe-recycling band, 57 LMICs (first-pass)."""
from pathlib import Path
import pandas as pd, geopandas as gpd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch

BASE = Path(__file__).resolve().parent.parent  # project/repo root (this file is in code/)
world = gpd.read_file(BASE / "data" / "geo" / "ne_10m_admin_0_countries.shp")
df = pd.read_csv(BASE / "data" / "ulab_volume_by_country.csv")

B = ["below modular floor (export)", "uncertain middle (12k-50k)", "above export line (domestic plausible)"]
COL = {B[0]: "#4C78A8", B[1]: "#E45756", B[2]: "#54A24B"}
GREY = "#E6E6E6"

w = world.merge(df[["iso3", "band", "ulab_t"]], left_on="ISO_A3", right_on="iso3", how="left")
w["fill"] = w["band"].map(COL).fillna(GREY)
w = w[w["ISO_A3"] != "ATA"]
try:
    w = w.to_crs("+proj=robin")
except Exception as e:
    print("robin failed, using 4326:", e)

fig, ax = plt.subplots(figsize=(13, 6.6))
w.plot(ax=ax, color=w["fill"].tolist(), edgecolor="white", linewidth=0.2)
ax.set_axis_off()
ax.set_title("Can a country safely recycle its own used batteries at home?\n"
             "Estimated annual ULAB volume vs safe-recycling scale, 57 LMICs (first-pass, exploratory)",
             fontsize=12.5)
leg = [Patch(facecolor=COL[B[0]], label="Below modular floor (<12k t/yr) — needs export or regional pooling"),
       Patch(facecolor=COL[B[1]], label="Uncertain middle (12k–50k t/yr)"),
       Patch(facecolor=COL[B[2]], label="Above export line (>50k t/yr) — domestic plant plausible"),
       Patch(facecolor=GREY, label="Not in sample (high-income, or no vehicle data e.g. Ethiopia)")]
ax.legend(handles=leg, loc="lower left", fontsize=8, frameon=False, bbox_to_anchor=(0.0, 0.0))
plt.figtext(0.5, 0.01,
            "Volume: Beyond-hotspots vehicle-demand model (all-source, whole-battery tonnes). "
            "Thresholds: Engitec modular (12k) / Dalberg–USAID break-even (24k) & export line (50k).",
            ha="center", fontsize=7, color="#555")
plt.tight_layout()
fig.savefig(BASE / "output" / "fig3_map.png", dpi=160, bbox_inches="tight")
print("saved fig3_map.png; countries coloured by band:", int(w["band"].notna().sum()))
