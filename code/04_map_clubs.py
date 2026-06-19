"""World choropleth coloured by contiguous recycling 'club'; standalone countries in one colour.

Grouping from regions.py. Multi-country clubs are labelled with pooled ULAB volume at their centroid.
"""
from pathlib import Path
import pandas as pd, geopandas as gpd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Patch
from regions import CLUB, CLUB_COLORS, STANDALONE, NOT_IN_SAMPLE, HUB_OUT_OF_SAMPLE

BASE = Path(__file__).resolve().parent.parent  # project/repo root (this file is in code/)

def fmt(x):
    return f"{x/1e6:.1f}M" if x >= 1e6 else (f"{x/1e3:.0f}k" if x >= 1e3 else f"{x:.0f}")

world = gpd.read_file(BASE / "data" / "geo" / "ne_10m_admin_0_countries.shp")
df = pd.read_csv(BASE / "data" / "ulab_volume_by_country.csv")
df["club"] = df["iso3"].map(CLUB)
tot = df.groupby("club")["ulab_t"].agg(total="sum", n="size")

w = world.merge(df[["iso3", "club"]], left_on="ISO_A3", right_on="iso3", how="left")
w["fill"] = w["club"].map(lambda c: CLUB_COLORS.get(c, STANDALONE) if isinstance(c, str) else NOT_IN_SAMPLE)
w = w[w["ISO_A3"] != "ATA"].to_crs("+proj=robin")

fig, ax = plt.subplots(figsize=(13.5, 7.4))
w.plot(ax=ax, color=w["fill"].tolist(), edgecolor="white", linewidth=0.2)
ax.set_axis_off()

clubs = w[w["club"].isin(CLUB_COLORS)].dissolve(by="club")
for club, row in clubs.iterrows():
    pt = row.geometry.representative_point()
    ax.annotate(fmt(tot.loc[club, "total"]), (pt.x, pt.y), ha="center", va="center", fontsize=8.5,
                fontweight="bold", color="white", path_effects=[pe.withStroke(linewidth=2.0, foreground="#333")])

order = [c for c in tot.sort_values("total", ascending=False).index if c in CLUB_COLORS]
handles = [Patch(facecolor=CLUB_COLORS[c],
                 label=f"{c} — {fmt(tot.loc[c,'total'])} ({int(tot.loc[c,'n'])})"
                       + (f"  → hub {HUB_OUT_OF_SAMPLE[c]}" if c in HUB_OUT_OF_SAMPLE else ""))
           for c in order]
handles.append(Patch(facecolor=STANDALONE, label="Stands alone — no contiguous in-sample club"))
handles.append(Patch(facecolor=NOT_IN_SAMPLE, label="Not in sample"))
ax.legend(handles=handles, loc="lower left", fontsize=7.2, frameon=False, ncol=2, bbox_to_anchor=(0.0, -0.02))
ax.set_title("Contiguous recycling 'clubs' (first-pass): pooled ULAB volume by bloc", fontsize=12)
plt.figtext(0.5, 0.005,
            "Clubs = land-contiguous in-sample countries, cut at narrow bridges. Grey = stands alone "
            "(islands, or neighbours outside the LMIC sample). Volume: Beyond-hotspots model.",
            ha="center", fontsize=7, color="#555")
plt.tight_layout()
fig.savefig(BASE / "output" / "fig4_map_clubs.png", dpi=160, bbox_inches="tight")
print("saved output/fig4_map_clubs.png")
