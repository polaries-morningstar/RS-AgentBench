# RS-AgentBench artefact bundle

Reproduction artefact for the paper *Knowledge Channels for LLM Agents on
Remote-Sensing Tasks: A Factorial Study Across Model Scale and Task*. This
repository contains the experimental code, the aggregated per-trial outputs
(scores, effort metrics, and statistical tables), the failure-mode labels,
the task specifications, and the figure-generation scripts — everything
needed to reproduce the numerical results and the figures of the paper. A
copy of the paper (`paper.pdf`) is included.

## Repository layout

```
.
├── README.md                # this file
├── paper.pdf                # the paper (SIGSPATIAL '26)
├── code/                    # experiment code (single OpenAI-compatible call path)
│   ├── README.md                    # invocation guide + env-var contract
│   ├── runner.py / agent.py         # trial entry point + pydantic-ai agent
│   ├── aggregate.py                 # cell-level rollup of per-trial JSON
│   ├── baseline_pipeline*.py / t5_ub_*.py     # spectral baselines / T5 ceilings
│   ├── kb_common.py / kb_index.py / kb_search.py
│   ├── preflight_check.py / pyproject.toml
│   ├── PROTOCOL.md / PROTOCOL_CHANGELOG.md / METRICS.md
│   ├── kb/                          # KB markdown corpus + BM25 + dense indexes
│   ├── skills/                      # five Agent Skills SOPs (one per task)
│   ├── prepare_tif/                 # public-source → task TIFF derivation
│   └── evaluation/                  # pixel-F1 / OA implementation
├── data/                    # aggregated experiment outputs
│   ├── all_trials.parquet           # 14,002 per-trial F1 / OA scores (canonical per-trial record)
│   ├── cell_means.csv               # per-(model, cfg, task) mean F1
│   ├── cost_trials.parquet          # per-trial tool-call + token + wall-clock
│   ├── cost_cells.csv               # per-cell aggregated effort metrics
│   ├── factorial_anova.csv          # 2^3 ANOVA decomposition per (model, task)
│   ├── naive_compare.csv            # spectral-router baseline vs agents
│   ├── pairwise_contrasts.csv       # pairwise channel contrasts with bootstrap CIs
│   ├── pareto_frontier.csv          # F1 vs token-cost Pareto points
│   ├── scaling_curve.csv            # panel-pooled F1 vs active / total parameters
│   ├── sk_forest.csv                # per-(model, task) SK main-effect contrasts
│   ├── skill_invocation_rate.csv    # per-(model, cfg) Skill() invocation rate
│   ├── t5_query_tuples.json         # the ten T5 (target, reference, radius) tuples + queries
│   └── failure_labels/
│       ├── RUBRIC.md                # 11-class labelling rubric
│       └── labels_pool.json         # 350 manually labelled failed trials
├── tasks/                   # task specifications (RS-AgentBench v1.3)
│   ├── water.json                   # T1 water extraction
│   ├── change.json                  # T2 bi-temporal change detection
│   ├── landcover.json               # T3 four-class land cover
│   ├── burn.json                    # T4 burn-scar detection
│   └── query.json                   # T5 compositional spatial query
└── figs_src/                # matplotlib scripts for every figure
    ├── _style.py                    # shared plot style + MODEL_ORDER / TASK_ORDER
    ├── F_scaling.py / F3_heatmap.py / F5_failure_modes.py / ...
    └── ...                          # one script per figure in the paper
```

## Not included here (too large for git)

Two artefacts are intentionally **not** committed because of size:

- **Raw per-trial archives** (`runs/`, ~82 GB): each trial's `agent_log.json`
  transcript, `metrics.json`, predicted output mask, and config. The
  **canonical per-trial record is `data/all_trials.parquet`** (14,002 rows of
  per-trial F1/OA scores) together with `data/cost_trials.parquet` (per-trial
  tool-call / token / wall-clock effort). Raw transcripts can be regenerated
  with `code/runner.py` — LLM sampling is stochastic, so they will not be
  bit-identical — or are available from the authors on request.
- **Task-input rasters** (`datasets_tif/`, GeoTIFFs): derived from publicly
  available Sentinel-2 L1C / surface-reflectance imagery (Copernicus), OSCD,
  CaBuAr/CHABUD, and WorldCover v200 (ESA) ground truth. They can be rebuilt
  from those public sources via `code/prepare_tif/` following the per-task
  specifications in `tasks/`.

## How the data was produced

Each of the 14,002 scored trials runs an LLM agent against one
(scene, task) input under one knowledge-channel configuration. The agent
executes a ReAct tool-use loop with a sandboxed Python tool, file primitives,
and the configuration-gated knowledge tools (KB, WS, SK). The agent
output is a binary mask (T1, T2, T4, T5) or a four-class land-cover map
(T3), scored against a public ground-truth raster by pixel F1 or overall
accuracy. The full protocol is in §4 of the paper; the seven backbones, five
tasks, and 2³ knowledge-channel factorial are documented in Table 2.

## Running new trials against the same harness

The runner in `code/` talks to any OpenAI-compatible Chat-Completions
endpoint — there is one calling pattern across every backbone. Set:

```
OPENAI_BASE_URL   # any OpenAI-compatible endpoint
OPENAI_API_KEY    # API key for that endpoint
TAVILY_API_KEY    # required for C2 / C4 / C6 / C7 (WebSearch tool)
```

Then:

```bash
cd code
uv sync
uv run python runner.py --task water --config C3 --model qwen3-8b --all --repeat 5
uv run python aggregate.py path/to/results/ > my_cell_means.csv
```

See `code/README.md` for the full invocation guide, the env-var contract,
and notes on switching providers (DashScope, DeepSeek, Moonshot,
OpenRouter, self-hosted vLLM — all share the same code path).

## Reproducing the figures

The scripts in `figs_src/` read the tables in `data/`. To regenerate
all figures:

```bash
cd figs_src
python -m pip install matplotlib numpy pandas pyarrow scipy
for f in F*.py; do python "$f"; done
```

Each script writes a `.pdf` (vector) and `.png` (300 DPI). The scripts are
deterministic given the data files in `data/`. Note: some scripts reference a
`DATA` path near the top — point it at this repository's `data/` directory
before running.

## Failure-mode labels

The 350-trial failure pool (`data/failure_labels/labels_pool.json`) is a
stratified subsample of the 14,002 scored trials, drawn at 50 trials per
backbone from cells with primary metric below 0.10 or unsubmitted. Each trial
received a single primary label from the 11-category schema documented in
`data/failure_labels/RUBRIC.md` under a fixed decision order. Labelling was
performed manually by reviewing each trial's tool-call sequence, final
assistant text, and code previews.

## License

The data, labels, and scripts in this bundle are released under the CC BY 4.0
licence. The task input rasters are derived from publicly available Sentinel-2
L1C and surface-reflectance imagery (Copernicus / USGS) and from WorldCover
v200 (ESA) ground-truth labels; please honour the upstream licence terms when
redistributing the rasters.
