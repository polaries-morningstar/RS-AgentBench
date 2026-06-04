"""Expand the KB with verbatim content from authoritative open sources.

Each entry below specifies:
- target file in kb/
- the (single) source URL
- a fetch_method: 'tavily' (returns markdown), 'github_raw' (raw text),
  or 'json_to_table' (post-process JSON into a markdown table without
  authoring new prose)
- a 'title' header line we prepend (this is the only added content; it
  identifies the document inside the KB)

Constraints:
- Body content MUST be verbatim from the source (no paraphrasing)
- Only the H1 title and "Source: <url>" attribution line are author-added
- For JSON sources we render as a faithful table without re-interpreting
  the data (it's still the raw values, just laid out)

Run: python expand_kb.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
load_dotenv(ROOT.parent / ".env")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")


def tavily_extract(url: str) -> str:
    with httpx.Client(timeout=60) as c:
        r = c.post(
            "https://api.tavily.com/extract",
            json={"api_key": TAVILY_KEY, "urls": [url], "extract_depth": "basic"},
        )
        r.raise_for_status()
        d = r.json()
        results = d.get("results") or []
        if not results:
            raise RuntimeError(f"No content extracted from {url}")
        return (results[0].get("raw_content") or results[0].get("content") or "").strip()


def github_raw(url: str) -> str:
    with httpx.Client(timeout=60) as c:
        r = c.get(url)
        r.raise_for_status()
        return r.text


def render_bands_table(json_text: str) -> str:
    """Render bands.json as a markdown table (verbatim values, table layout)."""
    data = json.loads(json_text)
    out = []
    out.append("## Standard variable → satellite band mapping\n")
    out.append("Verbatim values from `output/bands.json` of the "
               "awesome-spectral-indices repository.\n")
    out.append("| Variable | Common name | Long name | "
               "Wavelength range (nm) | Sentinel-2 band | S-2 wavelength | "
               "Landsat 8/9 band | MODIS band |")
    out.append("|---|---|---|---|---|---|---|---|")
    for var, info in data.items():
        cm = info.get("common_name", "")
        ln = info.get("long_name", "")
        lo = info.get("min_wavelength", "")
        hi = info.get("max_wavelength", "")
        wr = f"{lo}-{hi}" if lo and hi else ""
        plats = info.get("platforms", {})
        s2 = plats.get("sentinel2a") or plats.get("sentinel2", {})
        l8 = plats.get("landsat8", {})
        modis = plats.get("modis", {})
        s2c = f"{s2.get('band','')} ({s2.get('wavelength','')}nm)" if s2 else ""
        l8c = f"{l8.get('band','')} ({l8.get('wavelength','')}nm)" if l8 else ""
        mod = f"{modis.get('band','')} ({modis.get('wavelength','')}nm)" if modis else ""
        s2wl = f"{s2.get('wavelength','')}" if s2 else ""
        out.append(f"| **{var}** | {cm} | {ln} | {wr} | {s2.get('band','')} | {s2wl} | {l8.get('band','')} | {modis.get('band','')} |")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# KB additions
# ---------------------------------------------------------------------------

ENTRIES = [
    {
        "target": KB / "01_domain" / "spectral_indices_band_mapping.md",
        "source_url": "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/bands.json",
        "method": "json_to_table",
        "title": "Standard Variable → Satellite Band Mapping (awesome-spectral-indices)",
    },
    {
        "target": KB / "01_domain" / "sentinel2_bands_reference.md",
        "source_url": "https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/bands/",
        "method": "tavily",
        "title": "Sentinel-2 Bands Reference",
    },
    {
        "target": KB / "02_techniques" / "sentinel2_ndwi_recipe.md",
        "source_url": "https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndwi/",
        "method": "tavily",
        "title": "NDWI Normalized Difference Water Index — Sentinel-2 Recipe",
    },
    {
        "target": KB / "02_techniques" / "sentinel2_ndvi_recipe.md",
        "source_url": "https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndvi/",
        "method": "tavily",
        "title": "Normalized Difference Vegetation Index — Sentinel-2 Recipe",
    },
    {
        "target": KB / "01_domain" / "nasa_ndvi_evi_overview.md",
        "source_url": "https://science.nasa.gov/earth/earth-observatory/measuring-vegetation-ndvi-evi/",
        "method": "tavily",
        "title": "Measuring Vegetation (NDVI & EVI) — NASA Earth Observatory",
    },
    {
        "target": KB / "01_domain" / "usgs_ndvi_phenology.md",
        "source_url": "https://www.usgs.gov/special-topics/remote-sensing-phenology/science/ndvi-foundation-remote-sensing-phenology",
        "method": "tavily",
        "title": "NDVI: The Foundation for Remote Sensing Phenology — USGS",
    },
    {
        "target": KB / "02_techniques" / "gee_change_detection_tutorial.md",
        "source_url": "https://developers.google.com/earth-engine/tutorials/community/detecting-changes-in-sentinel-1-imagery-pt-2",
        "method": "tavily",
        "title": "Detecting Changes in Sentinel Imagery — Google Earth Engine Community Tutorial",
    },
    {
        "target": KB / "02_techniques" / "sentinel2_ndbi_recipe.md",
        "source_url": "https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndbi/",
        "method": "tavily",
        "title": "NDBI Normalized Difference Built-Up Index — Sentinel-2 Recipe",
    },
    {
        "target": KB / "02_techniques" / "sentinel2_indices_indexdb.md",
        "source_url": "https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/",
        "method": "tavily",
        "title": "Sentinel-2 Spectral Indices Catalogue — Sentinel Hub IndexDB",
    },
]


def fetch_one(entry):
    method = entry["method"]
    url = entry["source_url"]
    if method == "tavily":
        return tavily_extract(url)
    if method == "github_raw":
        return github_raw(url)
    if method == "json_to_table":
        return render_bands_table(github_raw(url))
    raise ValueError(f"unknown method: {method}")


def main():
    if not TAVILY_KEY:
        print("ERROR: TAVILY_API_KEY not set in .env")
        sys.exit(1)

    for entry in ENTRIES:
        target = entry["target"]
        if target.exists():
            print(f"  [skip] {target.relative_to(KB)} already exists")
            continue
        try:
            body = fetch_one(entry)
        except Exception as e:
            print(f"  [FAIL] {target.relative_to(KB)}: {type(e).__name__}: {e}")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        header = f"# {entry['title']}\n\nSource: {entry['source_url']}\n\n---\n\n"
        target.write_text(header + body, encoding="utf-8")
        print(f"  [ok]   {target.relative_to(KB)}  ({len(body)} chars)")


if __name__ == "__main__":
    main()
