"""World choropleth coloured by proposed regional recycling 'club' (first-pass geographic grouping).
Each club labelled with pooled ULAB volume (whole-battery t/yr). Grouping == 02_regional_clubs.py."""
from pathlib import Path
import pandas as pd, geopandas as gpd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Patch

BASE = Path(__file__).resolve().parent.parent  # project/repo root (this file is in code/)
T_BE = 24_000

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
RC = {'West Africa':'#4E79A7','East Africa':'#F28E2B','Southern Africa':'#59A14F','Central Africa':'#B07AA1',
      'North Africa':'#E15759','Middle East':'#76B7B2','South Asia':'#EDC948','Southeast Asia':'#FF9DA7',
      'Central Asia':'#9C755F','Lat. Am. & Carib.':'#499894','Pacific':'#222222'}
GREY = '#E6E6E6'

def fmt(x):
    return f"{x/1e6:.1f}M" if x>=1e6 else (f"{x/1e3:.0f}k" if x>=1e3 else f"{x:.0f}")

world = gpd.read_file(BASE/"data"/"geo"/"ne_10m_admin_0_countries.shp")
df = pd.read_csv(BASE/"data"/"ulab_volume_by_country.csv")
df['region'] = df['iso3'].map(REGION)
tot = df.groupby('region')['ulab_t'].agg(total='sum', n='size')
print(tot.sort_values('total', ascending=False).assign(total=lambda d: d['total'].map('{:,.0f}'.format)).to_string())

w = world.merge(df[['iso3','region']], left_on='ISO_A3', right_on='iso3', how='left')
w['fill'] = w['region'].map(RC).fillna(GREY)
w = w[w['ISO_A3']!='ATA'].to_crs('+proj=robin')

fig, ax = plt.subplots(figsize=(13.5, 7.2))
w.plot(ax=ax, color=w['fill'].tolist(), edgecolor='white', linewidth=0.2)
ax.set_axis_off()

clubs = w[w['region'].notna()].dissolve(by='region')
for region, row in clubs.iterrows():
    pt = row.geometry.representative_point()
    ax.annotate(fmt(tot.loc[region,'total']), (pt.x, pt.y), ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white',
                path_effects=[pe.withStroke(linewidth=2.0, foreground='#333')])

order = tot.sort_values('total', ascending=False).index
handles = [Patch(facecolor=RC[r],
                 label=f"{r} — {fmt(tot.loc[r,'total'])} t/yr · {int(tot.loc[r,'n'])} countries"
                       + ("  (orphan, below 24k)" if tot.loc[r,'total'] < T_BE else ""))
           for r in order]
handles.append(Patch(facecolor=GREY, label="Not in sample (high-income, or no vehicle data)"))
ax.legend(handles=handles, loc='lower left', fontsize=7.3, frameon=False, ncol=2, bbox_to_anchor=(0.0, -0.02))
ax.set_title("Proposed regional recycling 'clubs' (first-pass geographic grouping)\n"
             "Label = pooled ULAB volume; every club clears the 50k export line except the Pacific",
             fontsize=12.5)
plt.figtext(0.5, 0.005, "Grouping is plain geography (first-pass) — could be ECOWAS/EAC/SADC blocs or distance-weighted. "
            "Volume: Beyond-hotspots model. South Africa (real SADC anchor) sits outside the LMIC sample.",
            ha='center', fontsize=7, color='#555')
plt.tight_layout()
fig.savefig(BASE/"output"/"fig4_map_clubs.png", dpi=160, bbox_inches='tight')
print("\nsaved fig4_map_clubs.png")
