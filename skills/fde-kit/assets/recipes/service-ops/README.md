# Service operations: synthetic practice only

This is invented data and policy, not a contest task or a submission answer.

Goal: summarize valid request costs, order actionable requests, and find the written processing rule.
Input records are 1-based excluding the CSV header (not physical line numbers for multiline fields).

- Nine records: six valid, three requiring correction (negative age, unknown severity, NaN amount).
- Ops total: 20.40; sales total: 20.20. The missing sales amount is not zero.
- Automatic queue: 003, 001, 002, 005, 006, 009; review rows: 004, 007, 008.
- For the query `긴급 요청 처리 기준`, the evidence must include the exact 24-hour threshold from docs/operations.md.

Run from this directory, using the installed skill:

```bash
python .agents/skills/fde-kit/scripts/recipes.py table requests.csv --config table.json --out outputs/table
python .agents/skills/fde-kit/scripts/recipes.py decide requests.csv --config decision.json --out outputs/decide
python .agents/skills/fde-kit/scripts/recipes.py search docs --query "긴급 요청 처리 기준" --out outputs/search
python check_delivery.py table
python check_delivery.py decide
python check_delivery.py search
```

Output directories must be new. For a revised run choose a new directory and update your acceptance checker and task contract to that run. Do not interpret an earlier run as current output.

`check_delivery.py` checks this sample's explicit expectations without importing recipe code.
For a real task, replace these expectations with task-specific, independently calculated checks. A passing sample is not proof that your new business rules are correct.
