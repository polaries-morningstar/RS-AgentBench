# RS-AgentBench failure-mode labelling rubric (11 classes)

Each failed trial in Pool B receives a single primary label from the 11
mutually exclusive classes below. Labelling is performed by manual review of
the per-trial digest (model / task / configuration / sample header, tool-call
sequence, final assistant text, code previews) under the fixed decision order
listed at the bottom of this file.

## Class definitions

1. **band_index** — agent indexed the wrong Sentinel-2 band (e.g. used B02 as
   NIR, or confused B01 with B04). Diagnose from a `RunPython` code preview
   showing `band=` or `read(N)` with the wrong `N` for the index being
   computed.

2. **ndvi_threshold** — agent computed the correct spectral index
   (NDVI / MNDWI / NDBI / NBR) but used a textbook-wrong threshold value (e.g.
   NDWI > 0.5 instead of NDWI > 0). Separated from `band_index`: threshold
   trials have correct band selection but a wrong cutoff.

3. **crs_ignored** — coordinate-system / projection mismatch between input
   raster and ground truth or buffer geometry. Signals: "CRS mismatch",
   "EPSG", "projection" in the trace, or a code path that never calls
   `reproject` / `to_crs` despite mixed-CRS inputs.

4. **wrong_input** — agent read the wrong file (`FileNotFoundError`, opened
   `image_A.png` when the task required `image_B.png`, or never read the
   input raster).

5. **skill_not_invoked** — configuration is C3 / C5 / C6 / C7 (SK enabled),
   but the tool-call list contains no `Skill(...)` invocation. The agent
   bypassed the available skill SOP and wrote ad-hoc code.

6. **hallucinated_fn** — agent imported or called a function or class that
   does not exist (e.g. `from rasterio.utils import segment_water`,
   `cv2.WaterDetector`). Signals: `AttributeError`, `NameError`, or
   "has no attribute". Submission-protocol confusion around `SubmitAnswer`
   is **not** a hallucination — label such cases as `skill_not_invoked` or
   `other` by context.

7. **timeout_stall** — agent ran out of rounds, time, or retry budget
   without committing to a code plan. Signals: `retry_count >= 5`, error
   text containing "timeout" or "max_rounds", or many consecutive empty /
   nearly identical tool calls.

8. **malformed_output** — agent produced an output mask with the wrong shape,
   dtype, or value range (not binary `{0, 255}`). Signals: "shape mismatch",
   `primary_metric = null` with `submitted = True`, or the agent's final
   code never persisted an image.

9. **class_confusion** — for land-cover / change-detection tasks, the agent
   labelled the wrong semantic class (e.g. labelled built-up as water).
   Signals: high bare-baseline cells with low F1 despite valid code and
   correct band / CRS; class names mentioned in the final text don't match
   the task spec.

10. **compositional_plan** — T5 only: agent misinterpreted the
    `(target, reference, K)` tuple. Signals: computed only the target mask
    without the buffer, swapped target and reference, or mis-parsed the
    distance unit.

11. **other** — anything else, including genuinely uncertain cases between
    two classes and multi-cause failures where no single dominant cause is
    identifiable.

## Decision order

If multiple classes plausibly apply, take the **first** applicable in the
above 1–11 order (`band_index` dominates `ndvi_threshold` dominates
`crs_ignored` … dominates `other`). This keeps labels reproducible across
labelling sessions.

## Output format

Each labelled trial yields a single record:

```json
{
  "trial_id": 17,
  "model": "qwen3-14b",
  "task": "landcover",
  "cfg": "C3",
  "sample": "phoenix_usa",
  "submitted": true,
  "primary_metric": 0.0083,
  "label": "skill_not_invoked",
  "confidence": "high",
  "notes": "C3 cfg but no Skill() call; ad-hoc Otsu on NDVI"
}
```

`confidence ∈ {high, medium, low}`; `notes` is a free-text one-line rationale
(≤120 chars). `trial_id` is the global 0–349 index in `labels_pool.json`.

The full set of 350 trial labels is in `labels_pool.json` in this directory.
