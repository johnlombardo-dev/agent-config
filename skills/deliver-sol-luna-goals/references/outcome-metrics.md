# Outcome metrics

Use this only for unusually long goals or when the user requests workflow-cost analysis.

This reference owns the optional reporting schema only. It does not change dispatch validity, precedence, verification requirements, or completion criteria in the parent `SKILL.md`.

Record one compact entry per accepted, rejected, or stopped assignment:

```text
<id> | <research|shaping|implementation|verification> | <state fingerprint>
Outcome: <landed|completed-no-change|useful-no-go|failed|aborted|superseded>
Evidence: <artifact, check, commit, or decision pointer>
Rework: <none or concise cause>
```

When reliable telemetry is available, also record elapsed time and separately reported input, cached-input, reasoning, and output tokens. Never estimate unavailable token classes from prose length.

Compare tokens and elapsed time by phase and outcome. Report useful prerequisite or `NO-GO` work separately from failed or abandoned work. Useful secondary measures include review corrections, repeated checks without state change, context-pack size, files or tests produced, and commits landed.
