"""
Regional aggregation ("clubbing") — could sub-threshold countries pool to viable scale?
Reads data/ulab_volume_by_country.csv (from 01_*). Groups the 57 LMICs into geographic
sub-regions, sums ULAB volume, and flags which individually-below-floor countries sit in
a region whose pooled volume clears the safe-recycling break-even (24k whole-battery t/yr).
First-pass geographic grouping — open to regrouping (ECOWAS/EAC/SADC, distance-weighted, etc.).
NB: some regions' real anchor is an out-of-sample country (esp. South Africa for Southern Africa).
"""
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent  # project/repo root (this file is in code/)
T_MOD, T_BE, T_EXP = 12_000, 24_000, 50_000

df = pd.read_csv(BASE / "data" / "ulab_volume_by_country.csv")

REGION = {
 'NGA':'West Africa','GHA':'West Africa','SEN':'West Africa','CIV':'West Africa','MLI':'West Africa',
 'BFA':'West Africa','NER':'West Africa','BEN':'West Africa','TGO':'West Africa','GIN':'West Africa',
 'LBR':'West Africa','MRT':'West Africa',
 'COD':'Central Africa','CMR':'Central Africa','TCD':'Central Africa',
 'KEN':'East Africa','TZA':'East Africa','UGA':'East Africa','RWA':'East Africa','BDI':'East Africa',
 'SDN':'East Africa','MDG':'East Africa',
 'ZMB':'Southern Africa','ZWE':'Southern Africa','MWI':'Southern Africa','MOZ':'Southern Africa',
 'AGO':'Southern Africa','NAM':'Southern Africa',
 'EGY':'North Africa','TUN':'North Africa','MAR':'North Africa',
 'JOR':'Middle East','LBN':'Middle East','SYR':'Middle East','PSE':'Middle East','YEM':'Middle East',
 'IND':'South Asia','PAK':'South Asia','BGD':'South Asia','NPL':'South Asia','BTN':'South Asia',
 'LKA':'South Asia','AFG':'South Asia',
 'VNM':'Southeast Asia','MMR':'Southeast Asia','KHM':'Southeast Asia','LAO':'Southeast Asia',
 'PHL':'Southeast Asia','TLS':'Southeast Asia',
 'UZB':'Central Asia','TJK':'Central Asia','KGZ':'Central Asia',
 'BOL':'Lat. Am. & Carib.','HND':'Lat. Am. & Carib.','NIC':'Lat. Am. & Carib.','HTI':'Lat. Am. & Carib.',
 'FSM':'Pacific',
}
EXT_ANCHOR = {'Southern Africa':'South Africa (out of sample; First Battery/Frys already operate)'}

df['region'] = df['iso3'].map(REGION)
unmapped = df[df['region'].isna()]
if len(unmapped): print("UNMAPPED:", unmapped[['country','iso3']].values.tolist())

g = (df.groupby('region')
       .agg(total=('ulab_t','sum'), n=('iso3','size'),
            n_below_floor=('ulab_t', lambda s:int((s<T_MOD).sum())),
            biggest=('ulab_t','max'))
       .reset_index().sort_values('total', ascending=False))
g['clears_breakeven'] = g['total'] >= T_BE
g.to_csv(BASE / "data" / "regional_clubs.csv", index=False)
print(g.to_string(formatters={'total':'{:,.0f}'.format,'biggest':'{:,.0f}'.format}))

df['region_total'] = df['region'].map(g.set_index('region')['total'])
below = df[df['ulab_t'] < T_MOD].copy()
below['rescued'] = below['region_total'] >= T_BE
print(f"\nBelow-floor countries: {len(below)}")
print(f"  rescued by regional club (region total >= 24k): {int(below['rescued'].sum())}")
print(f"  orphans (region also below 24k): {int((~below['rescued']).sum())}")
print(below[['country','region','ulab_t','region_total','rescued']]
        .sort_values(['region_total','ulab_t']).to_string(formatters={'ulab_t':'{:,.0f}'.format,'region_total':'{:,.0f}'.format}))

# figure
g2 = g.sort_values('total')
fig, ax = plt.subplots(figsize=(9, 5.6))
y = np.arange(len(g2))
ax.axvspan(T_MOD, T_EXP, color='grey', alpha=0.10, zorder=0)
ax.scatter(g2['total'], y, s=70, color='#4C78A8', zorder=3)
for t, lab in [(T_MOD,'modular 12k'),(T_BE,'break-even 24k'),(T_EXP,'export line 50k')]:
    ax.axvline(t, color='grey', ls='--', lw=0.8)
    ax.text(t, len(g2)-0.3, lab, rotation=90, va='top', ha='right', fontsize=7, color='grey')
ax.set_xscale('log')
ax.set_yticks(y); ax.set_yticklabels(g2['region'], fontsize=9)
ax.set_ylim(-0.7, len(g2)-0.2)
for yi, (_, r) in zip(y, g2.iterrows()):
    ax.text(r['total']*1.15, yi, f"{int(r['n'])} countries · {int(r['n_below_floor'])} below floor",
            va='center', ha='left', fontsize=7, color='#333')
ax.set_xlim(right=ax.get_xlim()[1]*6)
ax.set_xlabel("Pooled regional ULAB — tonnes of whole batteries/yr (log scale)")
ax.set_title("If they clubbed together: pooled regional ULAB vs the safe-recycling band (first-pass)", fontsize=10.5)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout()
fig.savefig(BASE / "output" / "fig2_regional_clubs.png", dpi=150, bbox_inches='tight')
print("\nSaved: output/fig2_regional_clubs.png  and  data/regional_clubs.csv")
