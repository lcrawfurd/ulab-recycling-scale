"""
ULAB recycling-viability blog — per-country ULAB volume vs safe-recycling threshold band.

Numerator source: "Beyond hotspots: estimating population lead exposure from battery
recycling" (Crawfurd, Mitchell, Hu, Environmental Pollution 2026), vehicle-demand model.
Intermediate file sites_vehicles.dta, variable `totallead` = annual lead-acid battery
lead generated per country (tonnes of lead/yr). It is already grossed up to ALL sources:
the .do divides vehicle-derived lead by lab_veh_share = 0.75 (vehicles assumed 75% of LABs),
so the residual ~25% (solar / telecom / standby / industrial) is included by assumption.

Conversion to whole-battery ULAB tonnes (to match Dalberg/USAID/Engitec thresholds, which
are quoted in whole used batteries):  ULAB_t = totallead / 0.65  (lead = 65% of battery weight).

Threshold band (whole-battery tonnes/yr):
  12,000  Engitec CX Smart modular plant, Cote d'Ivoire (Sept 2024) — modular lower bound
  24,000  safe smelter break-even (Dalberg/USAID ULAB Recycling Assessment, July 2024)
  50,000  Dalberg/USAID "export if national output is below this" screening line

Source dataset: sites_vehicles.dta — the vehicle-demand model intermediate from the published
"Beyond hotspots" paper (not redistributed in this repo). Expected at data/sites_vehicles_source.dta.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent  # project/repo root (this file is in code/)
LEADCONTENT = 0.65
T_MOD, T_BE, T_EXP = 12_000, 24_000, 50_000  # whole-battery tonnes/yr

# --- load + convert ---------------------------------------------------------
df = pd.read_stata(BASE / "data" / "sites_vehicles_source.dta")
df = df[["country", "countrycode", "year_cardata", "totallead"]].rename(columns={"countrycode": "iso3", "totallead": "lead_t"})
df = df[df["lead_t"] > 0].copy()
# Egypt appears twice (one IRF-measured car count, one WHO-fallback = whovehicles - commercial).
# Keep one row per ISO3, preferring the row with a measured IRF car-year over the fallback.
df["_has_year"] = df["year_cardata"].notna()
df = (df.sort_values(["iso3", "_has_year"], ascending=[True, False])
        .drop_duplicates("iso3", keep="first")
        .drop(columns="_has_year"))
df["ulab_t"] = df["lead_t"] / LEADCONTENT
df = df.sort_values("ulab_t").reset_index(drop=True)

def band(x):
    if x < T_MOD:  return "below modular floor (export)"
    if x < T_EXP:  return "uncertain middle (12k-50k)"
    return "above export line (domestic plausible)"
df["band"] = df["ulab_t"].apply(band)

df.to_csv(BASE / "data" / "ulab_volume_by_country.csv", index=False)

# --- summary ----------------------------------------------------------------
print(f"N countries with positive volume: {len(df)}")
print("\nBand counts (whole-battery tonnes/yr):")
for b in ["below modular floor (export)", "uncertain middle (12k-50k)", "above export line (domestic plausible)"]:
    n = (df["band"] == b).sum()
    print(f"  {b:42s} {n:3d}  ({n/len(df)*100:4.1f}%)")

print("\nValidation / anchors (ULAB whole-battery t/yr):")
for c in ["India", "Nigeria", "Egypt, Arab Rep", "Malawi", "Bangladesh", "Kenya", "Ghana",
          "Senegal", "Ethiopia", "Pakistan", "Congo, Dem Rep", "Tanzania", "Uganda", "Zambia"]:
    r = df[df["country"] == c]
    if len(r):
        print(f"  {c:20s} {r['ulab_t'].values[0]:>12,.0f}   [{r['band'].values[0]}]")
    else:
        print(f"  {c:20s} (not in sample)")

print("\nFull country list (low->high):")
print("  " + ", ".join(df["country"].tolist()))

# --- first-pass figure ------------------------------------------------------
colors = {
    "below modular floor (export)": "#4C78A8",
    "uncertain middle (12k-50k)": "#E45756",
    "above export line (domestic plausible)": "#54A24B",
}
fig, ax = plt.subplots(figsize=(8.2, 13))
y = np.arange(len(df))
ax.axvspan(T_MOD, T_EXP, color="grey", alpha=0.10, zorder=0)
ax.scatter(df["ulab_t"], y, c=df["band"].map(colors), s=30, zorder=3)
for t, lab in [(T_MOD, "Engitec modular  12k"), (T_BE, "break-even  24k"), (T_EXP, "export line  50k")]:
    ax.axvline(t, color="grey", ls="--", lw=0.8, zorder=1)
    ax.text(t, len(df) + 0.5, lab, rotation=90, va="bottom", ha="center", fontsize=7, color="grey")
ax.set_xscale("log")
ax.set_yticks(y)
ax.set_yticklabels(df["country"], fontsize=6.5)
ax.set_ylim(-1, len(df) + 4)
ax.set_xlabel("Estimated ULAB generated per year — tonnes of whole batteries (log scale)")
ax.set_title("First-pass (exploratory): most LMICs fall below safe-recycling scale", fontsize=11)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
n_below = (df["band"] == "below modular floor (export)").sum()
n_mid = (df["band"] == "uncertain middle (12k-50k)").sum()
n_above = (df["band"] == "above export line (domestic plausible)").sum()
ax.text(0.02, 0.02,
        f"below 12k: {n_below}    middle 12-50k: {n_mid}    above 50k: {n_above}\n"
        "Numerator: Beyond-hotspots vehicle-demand model (all-source). Bands: Dalberg/USAID + Engitec.",
        transform=ax.transAxes, fontsize=7, color="#333", va="bottom")
plt.tight_layout()
fig.savefig(BASE / "output" / "fig1_volume_vs_threshold.png", dpi=150, bbox_inches="tight")
print("\nSaved: output/fig1_volume_vs_threshold.png  and  data/ulab_volume_by_country.csv")
