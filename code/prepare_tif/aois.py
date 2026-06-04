"""Curated global AOIs for RS-AgentBench TIFF tasks (T1/T2/T4).

Each AOI is a (lon, lat) anchor point. We crop a 1024×1024 px tile @ 10 m
(10.24 km × 10.24 km) centred on this point, in the Sentinel-2 scene's
native UTM CRS.

Selection criteria:
- 5 continents × 2 each (10 total)
- Coastal / riverine — guarantees water + vegetation + built present
- Sentinel-2 L2A coverage in 2024-2025 with cloud-free scenes
- Diverse biomes (alpine, temperate, tropical, arid, Mediterranean)
"""

# (lon, lat, name, region, biome, expected_diversity_note)
AOIS: list[tuple[float, float, str, str, str, str]] = [
    # Europe (2)
    (6.60, 46.40, "lake_geneva_ch", "europe", "alpine_temperate",
     "Lac Léman + Lausanne suburbs + alpine forest"),
    (10.00, 53.55, "hamburg_de", "europe", "temperate_oceanic",
     "Elbe estuary + port + farmland + suburbs"),

    # Asia (2)
    (121.50, 31.20, "yangtze_delta_cn", "asia", "subtropical_humid",
     "Yangtze river + Shanghai-Suzhou + agricultural plain"),
    (120.98, 14.60, "manila_ph", "asia", "tropical",
     "Manila Bay + tropical urban + mangrove fringe"),

    # Americas (2 — both N. America after the v2 swap; Iguassu dropped)
    (-115.62, 33.30, "salton_sea_usa", "n_america", "arid_endorheic",
     "Salton Sea east shore + Imperial Valley irrigated agriculture + Sonoran desert"),
    (-112.07, 33.45, "phoenix_usa", "n_america", "arid_urban",
     "Phoenix metro + Sonoran desert + suburban dry vegetation"),

    # Africa (2)
    (18.45, -33.92, "cape_town_za", "africa", "mediterranean",
     "Table Bay + city + Table Mountain + fynbos"),
    (31.20, 30.10, "nile_delta_eg", "africa", "arid_irrigated",
     "Nile river + irrigated cropland + desert margin"),

    # Oceania (2 — Auckland added in v2 swap)
    (151.20, -33.85, "sydney_au", "oceania", "temperate_oceanic",
     "Sydney harbour + city + bushland"),
    (174.76, -36.85, "auckland_nz", "oceania", "temperate_oceanic",
     "Hauraki Gulf + Auckland city + Waitakere bushland"),
]


def get_aois() -> list[dict]:
    """Return AOIs as a list of dicts (for JSON serialization)."""
    return [
        {
            "id": f"aoi_{i:02d}",
            "lon": lon, "lat": lat,
            "name": name, "region": region, "biome": biome, "note": note,
        }
        for i, (lon, lat, name, region, biome, note) in enumerate(AOIS, 1)
    ]


if __name__ == "__main__":
    import json
    print(json.dumps(get_aois(), indent=2, ensure_ascii=False))
