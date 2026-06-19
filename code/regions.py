"""Canonical contiguous-club grouping + colours for the ULAB recycling-scale figures.

Shared by 02_regional_clubs.py and 04_map_clubs.py so the bar chart and the map can never drift.

A "club" is a set of land-contiguous in-sample countries, cut at the narrow trans-regional
bridges (e.g. Myanmar between South and Southeast Asia; the Chad-Sudan and Egypt-Gaza seams)
so chains don't span a continent. Countries with no contiguous in-sample neighbour stand alone
(islands, or countries whose neighbours are all outside the 57-country LMIC sample).
"""

CLUB = {
    # West & Sahel (ECOWAS + Cameroon + Chad)
    'NGA': 'West & Sahel', 'NER': 'West & Sahel', 'BEN': 'West & Sahel', 'TGO': 'West & Sahel',
    'GHA': 'West & Sahel', 'BFA': 'West & Sahel', 'MLI': 'West & Sahel', 'SEN': 'West & Sahel',
    'MRT': 'West & Sahel', 'GIN': 'West & Sahel', 'LBR': 'West & Sahel', 'CIV': 'West & Sahel',
    'CMR': 'West & Sahel', 'TCD': 'West & Sahel',
    # Nile
    'EGY': 'Nile', 'SDN': 'Nile',
    # Levant
    'JOR': 'Levant', 'LBN': 'Levant', 'SYR': 'Levant', 'PSE': 'Levant',
    # East Africa (EAC core + DRC)
    'KEN': 'East Africa (EAC+DRC)', 'TZA': 'East Africa (EAC+DRC)', 'UGA': 'East Africa (EAC+DRC)',
    'RWA': 'East Africa (EAC+DRC)', 'BDI': 'East Africa (EAC+DRC)', 'COD': 'East Africa (EAC+DRC)',
    # Southern Africa
    'ZMB': 'Southern Africa', 'ZWE': 'Southern Africa', 'MWI': 'Southern Africa',
    'MOZ': 'Southern Africa', 'AGO': 'Southern Africa', 'NAM': 'Southern Africa',
    # South Asia
    'IND': 'South Asia', 'PAK': 'South Asia', 'BGD': 'South Asia', 'NPL': 'South Asia',
    'BTN': 'South Asia', 'AFG': 'South Asia',
    # Southeast Asia
    'VNM': 'Southeast Asia', 'MMR': 'Southeast Asia', 'LAO': 'Southeast Asia', 'KHM': 'Southeast Asia',
    # Central Asia
    'UZB': 'Central Asia', 'TJK': 'Central Asia', 'KGZ': 'Central Asia',
    # Central America
    'HND': 'Central America', 'NIC': 'Central America',
    # Stand alone — no contiguous in-sample neighbour
    'MAR': 'Morocco', 'TUN': 'Tunisia', 'YEM': 'Yemen', 'BOL': 'Bolivia', 'LKA': 'Sri Lanka',
    'PHL': 'Philippines', 'MDG': 'Madagascar', 'HTI': 'Haiti', 'FSM': 'Micronesia', 'TLS': 'Timor-Leste',
}

# Colours for the multi-country contiguous clubs. Any club not listed here is a single country
# that stands alone and is drawn in STANDALONE.
CLUB_COLORS = {
    'West & Sahel': '#4E79A7', 'East Africa (EAC+DRC)': '#F28E2B', 'Southern Africa': '#59A14F',
    'Nile': '#B07AA1', 'Levant': '#E15759', 'South Asia': '#EDC948', 'Southeast Asia': '#FF9DA7',
    'Central Asia': '#9C755F', 'Central America': '#76B7B2',
}
STANDALONE = '#BAB0AC'   # countries with no contiguous in-sample club
NOT_IN_SAMPLE = '#E6E6E6'

# Clubs whose realistic recycling hub is a non-LMIC neighbour outside the 57-country sample.
HUB_OUT_OF_SAMPLE = {'Southern Africa': 'South Africa', 'Central America': 'Mexico'}
