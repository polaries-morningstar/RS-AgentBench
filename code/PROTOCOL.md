# RS-AgentBench Protocol (v1.3)

This document records the experimental protocol used for the
RS-AgentBench sweep reported in the paper. The protocol was
pre-registered at freeze; once frozen, the items in §3–§9 do not
change without bumping the protocol version and re-running the
affected cells.

If a bug is discovered after freeze, the choice is binary:
- **(a)** Document the bug as a known issue, leave the protocol
  untouched, report results as-is.
- **(b)** Bump the protocol version, throw out the affected runs,
  re-run from scratch.

Iterating prompts or parameters mid-experiment to "improve"
results is **not allowed**. That is variance fishing and we have
committed to producing pre-registered evidence.

---

## 1. Scope and version

- **Version**: v1.3
- **Frozen commit**: see the release archive
  (`paper/archive/code/`); this PROTOCOL.md, the runner / agent /
  KB code, and the task / skill manifests at that commit constitute
  the freeze.
- **Tasks** (canonical naming):

| Code | Task type                    | Dataset                                              | Input format                                                  | Eval                |
|------|------------------------------|------------------------------------------------------|---------------------------------------------------------------|---------------------|
| T1   | `water_extraction`           | Sentinel-2 + WorldCover v200                         | 1024×1024 × 10-band uint16                                    | binary pixel F1     |
| T2   | `change_detection`           | OSCD test split                                      | native H×W × 10-band uint16 (variable; query via rasterio)    | binary pixel F1     |
| T3   | `land_classification`        | Sentinel-2 + WorldCover (4 classes)                  | 1024×1024 × 10-band uint16                                    | multi-class OA      |
| T4   | `burn_scar_detection`        | CaBuAr / CHABUD test split (Sentinel-2)              | 512×512 × 10-band uint16 dual-time                            | binary pixel F1     |
| T5   | `compositional_spatial_query`| Sentinel-2 + WorldCover (target / reference / within) | 1024×1024 × 10-band uint16 + natural-language query           | binary pixel F1     |

T2 is intentionally variable-shape (OSCD city crops range
241×385 to 824×716). The runner reads `shape: [H, W]` from
`samples_v1.json` and enforces output shape per sample. T4 is
dual-time (`image_A.tif` = pre-fire, `image_B.tif` = post-fire)
at fixed 512×512 (the CaBuAr / CHABUD corpus is pre-patched). T5
uses a deterministic ground-truth construction from WorldCover
oracle labels and a fixed 6-class × 6-distance grammar with the
`within` operator. Input format for all five tasks is multi-band
Sentinel-2 GeoTIFF with 10 channels in this fixed order: `B02,
B03, B04, B08, B05, B06, B07, B8A, B11, B12`.

- **Knowledge conditions** (full 2³ factorial over `{KB, WS, SK}`):

| Code | KB (RAG) | WS (web) | SK (skill) |
|------|:--------:|:--------:|:----------:|
| C0   |    —     |    —     |     —      |
| C1   |    ✓     |    —     |     —      |
| C2   |    —     |    ✓     |     —      |
| C3   |    —     |    —     |     ✓      |
| C4   |    ✓     |    ✓     |     —      |
| C5   |    ✓     |    —     |     ✓      |
| C6   |    ✓     |    ✓     |     ✓      |
| C7   |    —     |    ✓     |     ✓      |

The full 2³ factorial supports the channel-decomposition analysis
in §5 of the paper (KB, WS, SK main effects and pairwise / triple
interactions) directly from the data rather than from inference
over isolated cells.

- **Model routing**: a single OpenAI-compatible Chat-Completions
  endpoint. The runner reads `OPENAI_BASE_URL` and
  `OPENAI_API_KEY` from the environment and uses the same
  `openai.AsyncOpenAI` client for every backbone. No mixed routing
  within or across cells.

- **Model panel** (seven open-weight backbones, total / active
  parameters):

| Family                | Model ID            | Active | Total  |
|-----------------------|---------------------|-------:|-------:|
| Alibaba Qwen 3        | `qwen3-8b`          | 8 B    | 8 B    |
| Alibaba Qwen 3        | `qwen3-14b`         | 14 B   | 14 B   |
| Alibaba Qwen 3.6      | `qwen3.6-27b`       | 27 B   | 27 B   |
| Alibaba Qwen 3.6 MoE  | `qwen3.6-35b-a3b`   | 3 B    | 35 B   |
| DeepSeek V4 MoE       | `deepseek-v4-flash` | 13 B   | 284 B  |
| Moonshot K2 MoE       | `kimi-k2.6`         | 32 B   | 1 T    |
| DeepSeek V4 MoE       | `deepseek-v4-pro`   | 49 B   | 1.6 T  |

All seven models are open-weight; closed-weight families are
out of scope because they cannot be placed on the active /
total parameter axis (see paper §7).

---

## 2. Research questions (pre-registered)

- **RQ1**: Which of the eight knowledge configurations (C0–C7)
  yields the highest pixel-level task quality on each task,
  controlling for backbone?
- **RQ2**: Are the three knowledge sources (KB / WS / SK)
  complementary or redundant? Tested via:
  - **Main effects**: average lift attributable to each modality,
    marginalising over the others.
  - **Pairwise interactions**: e.g. does (C5 − C3) − (C1 − C0) = 0
    (KB and SK independent), > 0 (synergistic), or < 0
    (antagonistic)?
  - **Redundancy of KB vs WS**: C4 vs max(C1, C2).
  - **Ceiling**: does C7 / C6 (full stack) beat C3 (SK alone) by
    enough to justify the extra knowledge cost?
- **RQ3**: Which failure modes occur, and how does each
  knowledge channel shift the failure-mode distribution? Reported
  via the 11-class manual rubric in `data/failure_labels/`.
- **RQ4**: How do the main effects and interaction terms change
  with backbone parameter scale and family? Tested across the
  seven-backbone panel.

A finding "no significant effect" is a valid result and is
reported as such. Negative results are pre-registered as
acceptable.

---

## 3. Tool surface (FROZEN)

The agent is given **at most** the following tools:

| Tool                       | Always on | Conditional on                              |
|----------------------------|-----------|---------------------------------------------|
| `RunPython(code, timeout)` | yes       | —                                           |
| `SubmitAnswer(notes)`      | yes       | —                                           |
| `SearchDocs(query)`        | no        | `show_kb=True`   (C1, C4, C5, C6)           |
| `WebSearch(query)`         | no        | `show_ws=True`   (C2, C4, C6, C7)           |
| `Skill(skill_name)`        | no        | `show_skill=True` (C3, C5, C6, C7)          |

Conditional tools are hidden via the pydantic-ai `prepare=`
callback so their schema is invisible to the model in
configurations where they are not allowed. Verified at freeze:
in C0 the model schema contains only `RunPython` and
`SubmitAnswer`; in any combination cell, exactly the conditional
tools listed above are present.

**Tool docstring policy** (frozen): each conditional tool's
docstring + `runner.build_prompt` hint explicitly tells the agent
the tool can be called **multiple times with targeted queries**.
The exact wording is committed at the freeze commit and not
changed mid-sweep.

`WebSearch` is implemented against the **Tavily API**
(`https://api.tavily.com/search`, `search_depth=basic`,
`max_results=5`). The API key is loaded from `TAVILY_API_KEY`.
Each WebSearch call consumes 1 against the agent's tool-call
budget.

`SearchDocs` is implemented as a hybrid retriever (dense
`Qwen3-Embedding-0.6B` + BM25 → RRF → cross-encoder
`Qwen3-Reranker-0.6B`, top-5 returned with score ≥ 0.30). The
KB index is captured in `kb/_meta.json` and packaged with the
release archive.

`Skill` returns the contents of `skills/<task-skill>/SKILL.md`.
The SKILL doc format follows the Agent Skills pattern of a header
naming the skill plus a body containing inputs/outputs contract,
workflow, starting-point recipe, scene-aware adjustments,
self-checks, and common pitfalls. The author explicitly invites
combining multiple adjustments and deviating from defaults when
the data warrants.

No other tools (`Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`,
etc.) are exposed for any configuration.

---

## 4. Resource limits (FROZEN)

| Limit                                  | Value                          |
|----------------------------------------|--------------------------------|
| Productive tool calls per run          | 30                             |
| Pydantic-AI hard ceiling               | 45 (buffer for SubmitAnswer retries and budget-exhausted refusals) |
| Wall clock per run                     | 600 s                          |
| Per-`RunPython` timeout (default / max)| 60 s / 180 s                   |
| Per-`RunPython` output truncation      | 10 000 chars                   |
| WebSearch results per call             | top-5                          |
| API retries on transient errors        | 10 (exponential back-off; see §9) |

The 30-call limit is the **productive** budget, including the
terminal `SubmitAnswer`. The 45-call pydantic ceiling is a safety
net so SubmitAnswer-rejected attempts and budget-exhausted
refusals do not terminate the run abruptly.

---

## 5. Determinism (FROZEN)

The runner sets two LLM sampling parameters explicitly:

- **`temperature = 0.6`** for every backbone in the panel. Some
  OpenAI-compatible endpoints clamp or ignore the field; the
  explicit setting documents intent.
- **`seed = 42`** for the LLM-sampling step.

In addition:

- **`RunPython` subprocess prelude**: pins `random.seed(0)`,
  `np.random.seed(0)`, `cv2.setRNGSeed(0)`, `PYTHONHASHSEED=0`.
  This eliminates randomness from CV libraries (k-means init,
  RANSAC, etc.).
- **Python interpreter**: `workspace/.venv` from the project's
  `uv.lock` at freeze.
- **Routing**: every run goes through one OpenAI-compatible
  endpoint pair (`OPENAI_BASE_URL`, `OPENAI_API_KEY`). No router
  switching mid-sweep.
- **Reasoning models**: SKUs that emit `reasoning_content`
  (qwen3-*, kimi-k2.6, deepseek-v4-flash, deepseek-v4-pro, any
  model whose name matches `thinking`, `r1`, or `/r1`) require
  the field to be echoed on subsequent assistant messages. The
  runner sets `OpenAIModelProfile(supports_thinking=True,
  thinking_always_enabled=True,
  openai_chat_thinking_field='reasoning_content',
  openai_chat_send_back_thinking_parts='field')` for these.
- **Kimi / Moonshot SKUs** additionally require
  `extra_body.thinking = {"type": "enabled", "budget_tokens":
  16000}` to enable the reasoning channel; the runner sets this
  per-trial for any model name starting with `kimi-` or
  `moonshot-`.

Variance from the residual stochastic floor is absorbed at the
protocol level via multiple repetitions per sample (§6) and
scene-level paired bootstrap CIs (§8).

---

## 6. Sampling protocol (FROZEN)

- **n_samples** per task: **10**
- **n_reps** per (sample, condition, backbone): **5**
- **Trials per cell** (backbone × condition × task): **50**

The 10 samples per task are **fixed** at the freeze commit:

- **T1 / T3**: 10 global Sentinel-2 AOIs (`lake_geneva_ch,
  hamburg_de, yangtze_delta_cn, manila_ph, salton_sea_usa,
  phoenix_usa, cape_town_za, nile_delta_eg, sydney_au,
  auckland_nz`). Selected for biome, latitude, and density
  diversity. Manifest: `datasets_tif/{water,landcover}/samples_v1.json`.
- **T2**: 10 OSCD test-split city pairs from
  `blanchon/OSCD_MSI` (test parquet, rows 0–9). Channels are
  reordered to the canonical 10-band layout; sizes are native
  city crops (no resampling). Manifest:
  `datasets_tif/change/samples_v1.json` with per-sample
  `shape: [H, W]`.
- **T4**: 10 CaBuAr / CHABUD pre/post Sentinel-2 patches from
  `DarthReca/california_burned_areas`
  (`raw/patched/chabud_test.h5`). Selected UIDs that have both
  `pre_fire` and `post_fire` arrays present, stratified by
  burn percentage. Channels are reordered from the 12-band raw
  layout to the canonical 10-band layout. Per-scene ground-truth
  provenance (CaBuAr / CHABUD) is recorded alongside each sample.
  Manifest: `datasets_tif/burn/samples_v1.json`.
- **T5**: 10 (target, reference, distance) tuples paired with
  10 globally-distributed AOIs (the AOI list of T1 / T3 plus
  T5-specific renderings). Tuples are distinct in (target,
  reference, K) and rendered through a frozen
  natural-language template. Manifest:
  `tasks/query.json` plus the rendered samples in
  `datasets_tif/query/samples_v1.json`.

If a sample's ground truth is later proved corrupt, it is
replaced by the next sample available; the full sweep is **not**
restarted for individual sample replacements.

**Perturbation**: TIFF-format tasks (T1–T4) **do not apply data
perturbation**. Sentinel-2's natural scene-to-scene diversity
provides the variation we would otherwise inject. Perturbation
logic in the runner (PNG-only) is dormant code retained for
legacy compatibility but never triggered for the v1.3 sweep. T5
queries are rendered through a frozen template that no model has
been trained against; the template itself is not perturbed.

---

## 7. Status taxonomy (FROZEN)

| Status                | Definition                                                                                |
|-----------------------|-------------------------------------------------------------------------------------------|
| `submitted`           | Agent called `SubmitAnswer` AND `artifacts/output.png` exists with valid format and shape. |
| `submitted_no_output` | Agent called `SubmitAnswer` but no/invalid output. Primary metric = 0.                    |
| `stopped_no_submit`   | Agent ended without calling `SubmitAnswer`. Lenient evaluation if output exists, else 0.  |
| `limit_reached`       | Hit 30-call productive ceiling. Same lenient rule.                                         |
| `timeout`             | Hit the 600 s per-run time cap. Same lenient rule.                                          |
| `error`               | API / infra failure persisting through all retries. Run is dropped; cell loses one trial. |

We **never** silently re-roll a successful or near-successful
run to "improve" it. The first valid run for a (sample, rep) is
the only one used.

---

## 8. Metrics reported (FROZEN)

For each cell (backbone × condition × task):

- **Primary**: F1 (T1, T2, T4, T5) or OA (T3). Mean and
  scene-level paired-bootstrap 95 % CI (B = 2,000 with NumPy
  seed 42).
- **Per-trial standard deviation** and **per-rep mean standard
  deviation**: both reported. Per-trial captures sample-to-sample
  variance; per-rep mean captures cell stability.
- **Efficiency**: median tool calls and median estimated output
  tokens, the two provider-agnostic effort axes used in the paper.
- **Behavioural**: SubmitAnswer rate, `SearchDocs` call rate
  (KB-on cells), `WebSearch` call rate (WS-on cells), `Skill`
  load rate (SK-on cells).

**Statistical comparisons**: scene-level paired bootstrap on
the per-task SK contrast (B = 2,000). Multiple-comparisons
control via Benjamini–Hochberg FDR < 0.05 across the 28
perception cells (T1, T2, T4, T5 × 7 backbones). Effect sizes
reported as raw ΔF1 with bootstrap CIs.

`aggregate.py` (frozen at the freeze commit) implements all of
the above and emits a Markdown table and a parquet.

---

## 9. Failure handling (FROZEN)

| Event                                 | Action                                                                                       |
|---------------------------------------|----------------------------------------------------------------------------------------------|
| Provider 5xx / connection error       | Retry up to 10 attempts with exponential back-off (base 30 s, cap 600 s). On final failure, mark `error`. |
| `429` rate limit                      | Same retry policy with a longer base (60 s).                                                  |
| Tavily 5xx / timeout                  | Tool returns an error string to the agent; the agent may try a different query. The call still consumes 1 from the budget. |
| `RunPython` timeout                   | Returned to the agent as text; the agent may retry with simpler code.                         |
| `RunPython` raises uncaught exception | Returned as stderr text; the agent is responsible for recovery.                               |
| Agent calls non-existent tool         | Pydantic-AI returns the validation error; counts as 1 tool call.                              |
| Output file missing on `submitted`    | Status `submitted_no_output`; primary metric = 0.                                              |
| Bug discovered post-freeze            | See §1. Choose (a) document, or (b) bump version and rerun.                                   |

Trials that fail to produce a valid mask under the lenient
evaluation are reported with primary metric = 0 in the
all-trials parquet rather than dropped, since these failures are
themselves a load-bearing part of the analysis.

---

## 10. Experiment matrix (FROZEN at v1.3)

The full sweep covers seven backbones × eight knowledge
configurations × five tasks = **280 cells** with 50 trials per
cell = **14,002 scored trials** (with 12 cells on
`qwen3.6-35b-a3b` running at N = 20–49 due to budget-exhausted
trials on the C7 full-stack configuration; cell-count audit is
in Appendix A of the paper).

Knowledge channels (KB / WS / SK) are isolated and crossed in
the 2³ factorial; backbone scale spans 8 B dense to 1.6 T MoE;
tasks span four established RS task families (water extraction,
bi-temporal change detection, land-cover classification,
burn-scar mapping) plus one new compositional spatial query
(T5) defined in §4 of the paper.

---

## 11. Pre-flight tests

### 11.1 Pipeline smoke test (per task)

For each task, run **1 sample × 1 rep × C0** and verify:
- Output file exists at expected path with expected dtype and shape.
- Evaluation script returns a sensible primary metric.
- No traceback in `runner.py`.

### 11.2 Determinism check (per backbone)

For each backbone, send the **same** 5 chat-completion requests
(same prompt, `temperature = 0.6`, `seed = 42`). Record SHA-256
of each response. A backbone with < 3/5 identical responses is
flagged "high stochastic floor" in the per-cell footnote.

### 11.3 Tavily smoke test

Send 5 representative queries to Tavily, confirm 200 OK
responses with non-empty results.

### 11.4 KB / RAG sanity

The KB index has its own sanity protocol (`kb_index.py`
manifest, embedding / reranker pinning). The freeze captures
`kb/_meta.json` SHA.

---

## 12. Reproducibility artefacts (committed at freeze)

- `agent.py`, `runner.py`, `kb_search.py`, `kb_index.py`,
  `aggregate.py`, `preflight_check.py` at freeze commit
- `kb/_meta.json` SHA + embedding model commit hash
- `tasks/{water,change,landcover,burn,query}.json` (frozen task configs)
- `datasets_tif/{water,change,landcover,burn,query}/samples_v1.json`
  (frozen 10-sample manifests)
- `skills/{water-extraction,change-detection,land-cover,burn-scar-detection,compositional-spatial-query}/SKILL.md`
  at freeze
- `workspace/.venv` lockfile (`uv.lock`)
- `PROTOCOL.md` (this file) at freeze commit
- `.env.example` documenting required env vars:
  `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `TAVILY_API_KEY`
- Optional: `KB_SEARCH_BASE_URL` for the remote RAG service.

A consumer reproducing the experiment must be able to:
1. Check out the freeze commit.
2. Provide the required keys via `.env`.
3. Run `uv sync`.
4. Run `python kb_index.py` and verify `_meta.json` SHA matches.
5. Run `runner.py` against any (model, configuration, task,
   sample) cell using only the OpenAI-compatible env-var pair.
6. Run `python aggregate.py` against the produced trial
   directory to recover the result tables.
7. Reproduce the summary numbers within the documented
   stochastic-floor band.

---

## 13. Anti-pattern checklist

The author commits **not** to do any of the following during the
experiment:

- ❌ Changing the system prompt mid-sweep "to nudge the agent
  toward better behaviour"
- ❌ Adding a new tool mid-sweep
- ❌ Changing KB retrieval parameters mid-sweep
- ❌ Switching Tavily for another web-search provider mid-sweep
- ❌ Re-rolling a "bad" run for the same (sample, rep) because
  the F1 was disappointing
- ❌ Cherry-picking samples that "obviously work better" after
  looking at preliminary results
- ❌ Reporting only the runs where the desired hypothesis held
- ❌ Switching the OpenAI-compatible endpoint for a single
  backbone mid-sweep
- ❌ Showing the agent the scoring formula or any reward function
- ❌ Including any GT-derived signal in the agent's prompt or
  tool returns

If any of these happen, the affected sweep restarts from scratch
under a bumped protocol version.
