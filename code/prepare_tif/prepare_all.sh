#!/usr/bin/env bash
# Prepare all RS-AgentBench v1.2 datasets in one shot.
#
# Sources are all PUBLIC and ANONYMOUS — no API keys required:
#   - Sentinel-2 L2A + ESA WorldCover  via Microsoft Planetary Computer
#   - OSCD bi-temporal multispectral   via HF blanchon/OSCD_MSI
#   - CaBuAr ChaBuD-test (burned area) via HF DarthReca/california_burned_areas
#
# Idempotent: each step is skipped if its outputs already exist. Safe to
# re-run after a partial failure.
#
# Usage:
#   cd benchmark
#   ./prepare_tif/prepare_all.sh
#
# After this finishes you can launch experiments directly:
#   ./sweep_model.sh <model> 5

set -euo pipefail

# Always run from benchmark/ so relative paths resolve consistently.
cd "$(dirname "$0")/.."

ROOT="$(pwd)"
DATA="$ROOT/datasets_tif"

step_header() {
    echo
    echo "=========================================================="
    echo "  $1"
    echo "=========================================================="
}

# ---------- Pre-flight checks ----------------------------------------------
step_header "0/4  Pre-flight checks"

if ! command -v uv >/dev/null 2>&1; then
    echo "ERROR: \`uv\` is not on PATH — install it first (https://docs.astral.sh/uv/)" >&2
    exit 1
fi

if [ ! -f pyproject.toml ]; then
    echo "ERROR: must run from benchmark/ directory" >&2
    exit 1
fi

if [ ! -d .venv ]; then
    echo "  .venv missing — running \`uv sync\`..."
    uv sync
fi

echo "  ✓ uv present, .venv present, cwd = $ROOT"

# ---------- 1. Sentinel-2 + WorldCover (T1 water, T3 landcover) -----------
step_header "1/4  Sentinel-2 + WorldCover (T1 water, T3 landcover)"
echo "      ~100 MB download via Microsoft Planetary Computer (anonymous)"

# `fetch.py` writes to datasets_tif/shared/<aoi>/{input.tif, worldcover.tif}.
# Consider it done when all 10 AOIs have both files.
EXPECTED_AOIS=(auckland_nz cape_town_za hamburg_de lake_geneva_ch manila_ph \
               nile_delta_eg phoenix_usa salton_sea_usa sydney_au yangtze_delta_cn)
need_fetch=0
for aoi in "${EXPECTED_AOIS[@]}"; do
    if [ ! -f "$DATA/shared/$aoi/input.tif" ] || [ ! -f "$DATA/shared/$aoi/worldcover.tif" ]; then
        need_fetch=1
        break
    fi
done

if [ "$need_fetch" -eq 0 ]; then
    echo "  ✓ all 10 AOIs already cached in datasets_tif/shared/, skipping"
else
    echo "  → running prepare_tif/fetch.py (this is the slowest step)"
    uv run python prepare_tif/fetch.py
fi

# Per-task GT derivation is local + fast — always idempotent-cheap, so we
# only skip when the final manifest exists with 10 entries.
need_derive=1
for task in water landcover; do
    if [ -f "$DATA/$task/samples_v1.json" ]; then
        n=$(uv run python -c "import json; print(len(json.load(open('$DATA/$task/samples_v1.json'))))")
        if [ "$n" -eq 10 ]; then
            continue
        fi
    fi
    need_derive=0  # any missing → must re-derive
    break
done

if [ "$need_derive" -eq 1 ]; then
    echo "  ✓ T1/T3 GT already derived, skipping derive_gt.py"
else
    echo "  → deriving T1/T3 GT from WorldCover rasters"
    uv run python prepare_tif/derive_gt.py
fi

# ---------- 2. OSCD test parquet → T2 change ------------------------------
step_header "2/4  OSCD test parquet (T2 change_detection)"
echo "      ~120 MB download via HuggingFace Hub (anonymous)"

OSCD_PARQUET="$DATA/oscd_raw/data/test-00000-of-00001.parquet"
if [ ! -f "$OSCD_PARQUET" ]; then
    echo "  → downloading OSCD test parquet from HF blanchon/OSCD_MSI"
    uv run python <<'PY'
import shutil
from pathlib import Path
from huggingface_hub import hf_hub_download

dest_dir = Path("datasets_tif/oscd_raw/data")
dest_dir.mkdir(parents=True, exist_ok=True)
src = Path(hf_hub_download(
    "blanchon/OSCD_MSI",
    "data/test-00000-of-00001.parquet",
    repo_type="dataset",
))
dest = dest_dir / "test-00000-of-00001.parquet"
if dest.exists():
    print(f"  already at {dest}")
else:
    # copyfile (not symlink) so the file survives HF cache pruning
    shutil.copyfile(src, dest)
    print(f"  copied to {dest}")
PY
else
    echo "  ✓ OSCD parquet already present at $OSCD_PARQUET"
fi

# Convert parquet → 10-band TIFF pairs + binary mask PNG.
if [ -f "$DATA/change/samples_v1.json" ]; then
    n=$(uv run python -c "import json; print(len(json.load(open('$DATA/change/samples_v1.json'))))")
    if [ "$n" -eq 10 ]; then
        echo "  ✓ T2 change samples already derived (n=$n), skipping fetch_oscd_to_tif.py"
    else
        echo "  → re-running fetch_oscd_to_tif.py (manifest had n=$n, expected 10)"
        uv run python prepare_tif/fetch_oscd_to_tif.py
    fi
else
    echo "  → running prepare_tif/fetch_oscd_to_tif.py"
    uv run python prepare_tif/fetch_oscd_to_tif.py
fi

# ---------- 3. CaBuAr ChaBuD-test → T4 burn -------------------------------
step_header "3/4  CaBuAr ChaBuD-test (T4 burn_scar_detection)"
echo "      ~636 MB HDF5 download via HuggingFace Hub (anonymous; cached)"

if [ -f "$DATA/burn/samples_v1.json" ]; then
    n=$(uv run python -c "import json; print(len(json.load(open('$DATA/burn/samples_v1.json'))))")
    if [ "$n" -eq 10 ]; then
        echo "  ✓ T4 burn samples already derived (n=$n), skipping fetch_burn_to_tif.py"
    else
        echo "  → re-running fetch_burn_to_tif.py (manifest had n=$n, expected 10)"
        uv run python prepare_tif/fetch_burn_to_tif.py
    fi
else
    echo "  → running prepare_tif/fetch_burn_to_tif.py"
    uv run python prepare_tif/fetch_burn_to_tif.py
fi

# ---------- 4. Final verification -----------------------------------------
step_header "4/4  Final verification"

uv run python <<'PY'
import json
from pathlib import Path

ROOT = Path("datasets_tif")
expected = {
    "water":     {"binary": True,  "shared_input": True},
    "landcover": {"binary": False, "shared_input": True},
    "change":    {"binary": True,  "dual_time": True},
    "burn":      {"binary": True,  "dual_time": True},
}

ok = True
for task, spec in expected.items():
    manifest = ROOT / task / "samples_v1.json"
    if not manifest.exists():
        print(f"  ❌ {task:10s}  manifest missing: {manifest}")
        ok = False
        continue
    samples = json.loads(manifest.read_text())
    if len(samples) != 10:
        print(f"  ❌ {task:10s}  manifest has n={len(samples)} (expected 10)")
        ok = False
        continue
    # Verify the first sample's files actually exist on disk
    s = samples[0]
    if spec.get("dual_time"):
        files = [s["image_a"], s["image_b"], s["label"]]
    else:
        files = [s["image"], s["label"]]
    missing = [f for f in files if not (ROOT / task / f).exists()]
    if missing:
        print(f"  ❌ {task:10s}  files missing for {s['id']}: {missing}")
        ok = False
        continue
    print(f"  ✓ {task:10s}  n=10 samples, first id = {s['id']}")

if not ok:
    raise SystemExit("One or more tasks did not pass verification — see above.")
print()
print("All 4 tasks ready. You can now launch experiments:")
print("  ./sweep_model.sh <model> 5")
PY

echo
echo "=========================================================="
echo "  Done. datasets_tif/ size:"
echo "=========================================================="
du -sh datasets_tif/water datasets_tif/landcover datasets_tif/change datasets_tif/burn datasets_tif/shared 2>/dev/null
