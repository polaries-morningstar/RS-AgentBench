# RS-AgentBench experimental code

The Python package that runs every trial in the paper. Drop it under any
OpenAI-compatible Chat-Completions endpoint, set two environment variables,
and the runner will reproduce the per-trial outputs that live (symlinked)
under `archive/runs/`.

## Layout

```
code/
├── runner.py                          # main entry point (one trial per invocation)
├── agent.py                           # pydantic-ai agent + tool definitions
├── aggregate.py                       # roll trial metrics.json into cell-level CSV
├── baseline_pipeline.py               # spectral baselines for T1, T3, T4
├── baseline_pipeline_variants.py      # T1 variant pipelines (MNDWI / NDWI / S2WI)
├── baseline_t5_compositional.py       # T5 spectral-router upper bound
├── t5_ub_oracle.py                    # T5 label-oracle ceiling
├── t5_ub_robustness.py                # T5 spectral-router robustness sweep
├── kb_common.py / kb_index.py / kb_search.py
│                                      # hybrid (dense + lexical) KB retrieval
├── preflight_check.py                 # fresh-clone readiness audit
├── pyproject.toml                     # Python dependencies (managed by uv)
├── PROTOCOL.md                        # frozen experimental protocol
├── PROTOCOL_CHANGELOG.md              # protocol version log
├── METRICS.md                         # metric definitions
├── kb/                                # KB markdown corpus + BM25 + dense indexes
├── skills/                            # five Agent Skills SOPs (one per task)
├── prepare_tif/                       # scripts that turn public sources into the task TIFFs
└── evaluation/                        # pixel-F1 / OA implementation
```

## Calling pattern

Every backbone talks to the runner through the same OpenAI-compatible
Chat-Completions surface. Two environment variables select the endpoint:

```
OPENAI_BASE_URL   e.g. https://api.openai.com/v1
OPENAI_API_KEY    your API key
```

Run a single trial:

```bash
uv run python runner.py \
  --task water --config C3 --model qwen3-8b --sample manila_ph
```

Run all samples for a (task, config, model) combination with N repetitions:

```bash
uv run python runner.py \
  --task burn --config C7 --model deepseek-v4-pro --all --repeat 5
```

Run the spectral baseline that the paper uses for the naive-comparison
floor:

```bash
uv run python baseline_pipeline.py --task water --all
```

Aggregate per-trial `metrics.json` files into cell-level CSV after a sweep:

```bash
uv run python aggregate.py path/to/results/ > cell_means.csv
```

To target a different provider (DashScope, DeepSeek's first-party API,
Moonshot, OpenRouter, a self-hosted vLLM, etc.) point `OPENAI_BASE_URL` at
that provider's OpenAI-compatible endpoint and swap `OPENAI_API_KEY`.
The code path itself does not change; only the model identifier you pass to
`--model` differs across providers.

## Environment variables

```
OPENAI_BASE_URL          required — OpenAI-compatible endpoint URL
OPENAI_API_KEY           required — API key for that endpoint
TAVILY_API_KEY           required for C2 / C4 / C6 / C7 (WebSearch tool)
KB_SEARCH_BASE_URL       optional — remote RAG server; falls back to local
                                    hybrid search if unset
```

No other secrets are needed. Run `python preflight_check.py` after setting
the variables to confirm the dataset rasters, the KB index, and the
endpoint are all reachable.

## Dependencies

`pyproject.toml` pins the Python packages; install with:

```bash
uv sync
```

The `uv.lock` from the experiment run is not shipped to keep this directory
provider-neutral; resolving against `pyproject.toml` at a fresh time gives a
near-identical environment for the small fraction of dependencies that
matter (pydantic-ai, openai, rasterio, scikit-learn, sentence-transformers).
