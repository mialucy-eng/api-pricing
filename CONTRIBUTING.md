# Contributing

Contributions should improve reproducibility or reader understanding.

## Good contributions

- Fix a parsing error with a link to the public catalog field that reproduces it.
- Improve the explanation of a billing unit without changing the source value.
- Add a deterministic table or filter that can be regenerated from public data.
- Improve English or Simplified Chinese documentation.

## Boundaries

- Do not add API keys, account data, private analytics, customer data, or screenshots of authenticated pages.
- Do not add vendor benchmarks, rankings, uptime, or performance claims without a reproducible source and clearly separate methodology.
- Do not describe catalog visibility as a guarantee that every key can call a model.
- Do not manually edit generated values in `RANKINGS.md` or `catalog-snapshot.json`; update the generator and rerun it.

Before opening a pull request, run:

```bash
python3 update_rankings.py
python3 -m json.tool catalog-snapshot.json >/dev/null
```
