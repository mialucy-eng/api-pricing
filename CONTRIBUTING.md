# Contributing

[简体中文](CONTRIBUTING.zh-CN.md)

Contributions should improve reproducibility or reader understanding. Pull requests are welcome from anyone; a merged community ranking remains the contributor's comparison and is not a LuckyAPI endorsement.

## Good contributions

- Fix a parsing error with a link to the public catalog field that reproduces it.
- Improve the explanation of a billing unit without changing the source value.
- Add a deterministic table or filter that can be regenerated from public data.
- Improve English or Simplified Chinese documentation.
- Submit a comparable ranking with dated public evidence and a reproducible method.

## Submit a community ranking

1. Fork this repository and create a branch.
2. Copy `community-rankings/examples/example-ranking.json` to `community-rankings/submissions/<id>.json`. The filename must equal the JSON `id`.
3. Replace every example value. Use one numeric metric, one unit, one collection scope, and at least two comparable entries.
4. Declare your GitHub username, affiliation, and any provider, employer, sponsorship, referral, or other material conflict. Use an empty `conflicts` array only when none applies.
5. Cite public HTTPS sources with access dates. Each entry's `source_url` must match one URL in `sources`.
6. Run the builder and checks:

```bash
python3 community_rankings.py
python3 community_rankings.py --check
python3 -m json.tool community-rankings/submissions/<id>.json >/dev/null
```

7. Commit the new JSON file and generated `COMMUNITY_RANKINGS.md`, then open a pull request using the repository template.

The generator calculates rank from each numeric value and the declared `higher_is_better` or `lower_is_better` direction. Do not type rank numbers into the source file. Maintainers may ask for narrower scope, stronger sources, or a reproduction note before merge.

## Ranking acceptance rules

- Compare like with like: one metric, unit, market, time window, workload, and measurement method.
- Explain inclusion and exclusion rules before presenting results.
- Prefer vendor documentation, public machine-readable catalogs, published datasets, or a repository containing the exact harness and raw aggregate results.
- Attribute third-party measurements. Do not present a vendor's marketing statement as an independent test.
- Keep conclusions within the evidence. Price does not prove quality; a benchmark score does not prove production reliability.
- Use new submission IDs for materially different scopes. Update an existing file only when refreshing the same method and scope.
- Keep the data reviewable. Submissions with more than 100 entries should publish a smaller summary here and link to a reproducible public dataset.

## Boundaries

- Do not add API keys, account data, private analytics, customer data, cookies, or screenshots of authenticated pages.
- Do not add hidden referral links, undisclosed sponsorship, fabricated results, copied prose, or scraped personal data.
- Do not describe catalog visibility as a guarantee that every key can call a model.
- Do not manually edit generated values in `RANKINGS.md` or `catalog-snapshot.json`; update the relevant generator and rerun it.
- Do not manually edit `COMMUNITY_RANKINGS.md`; update a submission and run `python3 community_rankings.py`.

For changes to the built-in LuckyAPI price tables, run:

```bash
python3 update_rankings.py
python3 -m json.tool catalog-snapshot.json >/dev/null
```
