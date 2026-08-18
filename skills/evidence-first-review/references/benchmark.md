# Benchmark protocol

Use this protocol to compare review instructions, not model quality.

## Trial setup

Run every case with the same model, reasoning effort, packet, repository instructions, tool access, time limit, and output-token limit. Use a fresh context for each case. Randomize case order separately for each approach.

The reviewer receives only the packet and its assigned skill. Do not expose `evals/answers.json`, another reviewer's output, prior adjudication, or the expected defect class. Store raw outputs outside the repository and do not retain reasoning traces.

Use `review-agent` as the baseline. Use `evidence-first-review` for discovery cases and `verify-repair-seam` for repair cases.

Keep both focused lane cases and cross-boundary cases where isolated tests pass but the composed outcome fails. Use different domains for development and holdout cases.

## Adjudication

After every run finishes, compare its reported findings with the answer key. Record one JSONL object per approach and case:

```json
{
  "approach": "review-agent",
  "case_id": "D-VALUE-DEV",
  "detected_finding_ids": ["F-D-VALUE-DEV-1"],
  "false_positives": 0,
  "input_tokens": 1200,
  "output_tokens": 240,
  "elapsed_ms": 18000
}
```

Use `null` for `elapsed_ms` when the runner does not provide measured wall time. Do not estimate it.

Count a finding only when it identifies the same violated invariant and supported failure as the answer. A different valid defect is a false positive for this fixed corpus until a second adjudicator adds it to the answer key. For every discovery result, record `selected_lanes` exactly as reported by the reviewer. Do not infer missing lane selections or token counts.

Allow one skill revision using development cases. Do not rerun development until it passes by memorization. Run holdout cases once after the revision is frozen.

## Scoring

Run:

```sh
python3 scripts/score_benchmark.py \
  --corpus evals/corpus.json \
  --answers evals/answers.json \
  --results /path/to/adjudicated-results.jsonl \
  --split holdout
```

The scorer weights P0, P1, P2, and P3 findings as 8, 5, 3, and 1. It also scores routing against each answer's `required_lanes`, `acceptable_lanes`, and `critical_lanes`. A critical lane has routing weight 5; every other required lane has weight 1.

It reports weighted finding recall, finding precision, defect-class coverage, routing recall, routing precision, total tokens, cost per true finding, elapsed time, and the holdout gates.

Discovery routing requires 100 percent critical-lane recall, at least 90 percent weighted required-lane recall, and at least 75 percent routing precision. Discovery findings also require at least 25 percent more weighted recall and no more than a five-point precision loss, or equal recall at no more than 60 percent of baseline token cost. Repair verification must match or improve recall and precision at no more than 60 percent of baseline token cost.

Do not replace an existing review process when either holdout gate fails. Report the missed defect classes and revise the skill in a separate change.
