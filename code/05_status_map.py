"""What should each country do with its ULABs? Status by volume + contiguity, shown at BOTH thresholds.

  home_conv : >= 50k         -> recycle at home (conventional plant)
  home_mod  : 12k-50k        -> recycle at home only with a modular plant (the swing tier)
  export    : < 12k, borders a country that clears the 12k modular floor -> ship to that neighbour
  pool      : < 12k, contiguous sub-12k peers together clear 12k         -> shared modular plant
  stuck     : < 12k, no viable contiguous option                         -> islands / isolated
Volume only; not a feasibility (governance/conflict) judgement. Grouping inputs from regions.py unused here.
"""
from pathlib import Path
from collections import deque
import pandas as pd, geopandas as gpd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch

BASE = Path(__file__).resolve().parent.parent
T_MOD, T_EXP = 12_000, 50_000

world = gpd.read_file(BASE / "data" / "geo" / "ne_10m_admin_0_countries.shp")
df = pd.read_csv(BASE / "data" / "ulab_volume_by_country.csv")
iso = set(df.iso3); vol = df.set_index("iso3").ulab_t.to_dict()
g = world[world.ISO_A3.isin(iso)][["ISO_A3", "geometry"]].dissolve("ISO_A3").reset_index().to_crs("ESRI:54009")
gb = g.copy(); gb["geometry"] = gb.geometry.buffer(1000)
j = gpd.sjoin(gb[["ISO_A3", "geometry"]], g[["ISO_A3", "geometry"]], predicate="intersects")
adj = {a: set() for a in g.ISO_A3}
for a, b in zip(j.ISO_A3_left, j.ISO_A3_right):
    if a != b: adj[a].add(b); adj[b].add(a)

def comp_below(s, thr):
    seen = {s}; q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen and vol[v] < thr: seen.add(v); q.append(v)
    return seen

def status(c):
    v = vol[c]
    if v >= T_EXP: return "home_conv"
    if v >= T_MOD: return "home_mod"
    if any(vol[n] >= T_MOD for n in adj[c]): return "export"
    if sum(vol[x] for x in comp_below(c, T_MOD)) >= T_MOD: return "pool"
    return "stuck"

df["status"] = df.iso3.map({c: status(c) for c in iso})
df.to_csv(BASE / "data" / "country_status.csv", index=False)

order = ["home_conv", "home_mod", "export", "pool", "stuck"]
lab = {"home_conv": "Recycle at home — conventional (≥50k)", "home_mod": "Recycle at home — modular only (12–50k)",
       "export": "Too small — export to a bigger neighbour", "pool": "Too small — pool with neighbours",
       "stuck": "Stuck — no viable option (islands)"}
COL = {"home_conv": "#2E7D32", "home_mod": "#9CCC65", "export": "#4C78A8", "pool": "#F28E2B", "stuck": "#E45756"}
for s in order: print(f"{lab[s]:48s} {int((df.status==s).sum())}")
print("\nat-home total (>=12k):", int((df.ulab_t >= T_MOD).sum()), " vs conventional-only (>=50k):", int((df.ulab_t >= T_EXP).sum()))
print("stuck:", df[df.status == "stuck"][["country", "ulab_t"]].to_dict("records"))

w = world.merge(df[["iso3", "status"]], left_on="ISO_A3", right_on="iso3", how="left")
w["fill"] = w["status"].map(COL).fillna("#E6E6E6")
w = w[w.ISO_A3 != "ATA"].to_crs("+proj=robin")
fig, ax = plt.subplots(figsize=(13.5, 7.2)); w.plot(ax=ax, color=w.fill.tolist(), edgecolor="white", linewidth=0.2); ax.set_axis_off()
handles = [Patch(facecolor=COL[s], label=f"{lab[s]} — {int((df.status==s).sum())}") for s in order]
handles.append(Patch(facecolor="#E6E6E6", label="Not in sample"))
ax.legend(handles=handles, loc="lower left", fontsize=8.5, frameon=False)
ax.set_title("What should each country do with its used batteries? (first-pass, exploratory)\n"
             "Greens = can recycle at home; light green is the tier that only works with modular kit", fontsize=12)
plt.figtext(0.5, 0.005, "Volume from the Beyond-hotspots model; thresholds Engitec modular (12k) and Dalberg-USAID (50k). "
            "A volume judgement only — not governance, conflict or transport feasibility.", ha="center", fontsize=7, color="#555")
plt.tight_layout(); fig.savefig(BASE / "output" / "fig6_status_map.png", dpi=160, bbox_inches="tight")
print("saved output/fig6_status_map.png")
