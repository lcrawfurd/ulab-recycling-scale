"""Pooled ULAB volume by contiguous club vs the safe-recycling band.

Clubs come from regions.py (land-contiguous in-sample countries, cut at narrow bridges).
Single-country "clubs" are countries with no contiguous in-sample neighbour (islands or
countries whose neighbours are outside the LMIC sample) — drawn in the standalone colour.
"""
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from regions import CLUB, CLUB_COLORS, STANDALONE

BASE = Path(__file__).resolve().parent.parent  # project/repo root (this file is in code/)
T_MOD, T_BE, T_EXP = 12_000, 24_000, 50_000

df = pd.read_csv(BASE / "data" / "ulab_volume_by_country.csv")
df["club"] = df["iso3"].map(CLUB)
if df["club"].isna().any():
    print("UNMAPPED:", df.loc[df["club"].isna(), "iso3"].tolist())

g = df.groupby("club").agg(total=("ulab_t", "sum"), n=("iso3", "size")).reset_index()
g["is_club"] = g["n"] > 1
g = g.sort_values("total").reset_index(drop=True)
g.to_csv(BASE / "data" / "clubs.csv", index=False)
print(g.sort_values("total", ascending=False).to_string(formatters={"total": "{:,.0f}".format}))

fig, ax = plt.subplots(figsize=(8.6, 8.2))
y = np.arange(len(g))
ax.axvspan(T_MOD, T_EXP, color="grey", alpha=0.10, zorder=0)
ax.scatter(g["total"], y, c=[CLUB_COLORS.get(c, STANDALONE) for c in g["club"]], s=46, zorder=3)
for t, lab in [(T_MOD, "modular 12k"), (T_BE, "break-even 24k"), (T_EXP, "export line 50k")]:
    ax.axvline(t, color="grey", ls="--", lw=0.8)
    ax.text(t, len(g) - 0.3, lab, rotation=90, va="top", ha="right", fontsize=7, color="grey")
ax.set_xscale("log")
ax.set_yticks(y)
ax.set_yticklabels([f"{c}  ({int(n)})" if isc else c for c, n, isc in zip(g["club"], g["n"], g["is_club"])],
                   fontsize=8)
ax.set_ylim(-1, len(g) + 2)
ax.set_xlabel("Pooled ULAB volume — tonnes of whole batteries/yr (log scale)")
ax.set_title("Contiguous clubs vs the safe-recycling band (first-pass, exploratory)", fontsize=11)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.text(0.02, 0.02,
        "Coloured = multi-country contiguous club (n countries).  Grey = stands alone, no contiguous\n"
        "in-sample neighbour.  Band: Engitec modular (12k) / Dalberg-USAID break-even (24k) & line (50k).",
        transform=ax.transAxes, fontsize=7, color="#444", va="bottom")
plt.tight_layout()
fig.savefig(BASE / "output" / "fig2_regional_clubs.png", dpi=150, bbox_inches="tight")
print("saved output/fig2_regional_clubs.png and data/clubs.csv")
