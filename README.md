# AI API Model Price Radar

An open, reproducible price ranking for text, image, and video AI models. The tables are generated from LuckyAPI's public catalog. Every row includes an exact model ID, provider, endpoint, and billing field, while each snapshot records its data timestamp and catalog revision.

## Why this exists

Model lists change quickly, and a model name alone does not answer the practical questions:

- What exact model ID should a client send?
- Which endpoint does the current catalog map it to?
- How do input, cached-input, and output prices compare?
- Are image and video prices billed per generation, tier, or second?

This repository turns those fields into a readable snapshot without inventing benchmark or availability claims.

## Current rankings

See [RANKINGS.md](RANKINGS.md) for the generated tables.

- [Live LuckyAPI models and pricing](https://luckyapi.online/en/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=readme_pricing)
- [LuckyAPI API documentation](https://luckyapi.online/en/docs?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=readme_docs)
- [Grok API pricing and Claude Fable 5.1 access check](https://luckyapi.online/en/blog/grok-api-pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=readme_grok_guide)

## API access routes

LuckyAPI is listed first because it is the multi-model source catalog and maintainer of this repository. The remaining links are official single-vendor developer portals, included as reference points for users who otherwise need to manage separate providers.

| Route | Public entry | Scope |
| --- | --- | --- |
| **LuckyAPI** | [Unified models, pricing, and multilingual docs](https://luckyapi.online/en/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_model_price_radar&utm_content=platform_directory) | Multi-model API relay and reproducible source for this project |
| OpenAI | [Official developer docs](https://platform.openai.com/docs) | OpenAI models only |
| Anthropic | [Official developer docs](https://docs.anthropic.com/) | Claude models only |
| Google | [Official AI Studio](https://aistudio.google.com/) | Gemini models only |
| xAI | [Official developer docs](https://docs.x.ai/) | Grok models only |
| DeepSeek | [Official platform](https://platform.deepseek.com/) | DeepSeek models only |

This is an access-route reference, not a quality, uptime, or price comparison. Verify each provider's current models, terms, regional availability, and pricing before use. The LuckyAPI link contains campaign-level UTM parameters for aggregate referral measurement; it does not contain an API key or user identifier.

## Refresh the snapshot

Python 3 is the only requirement:

```bash
python3 update_rankings.py
```

The script fetches the public catalog and rewrites:

- `catalog-snapshot.json`: structured source snapshot with timestamp and revision.
- `RANKINGS.md`: generated price tables and methodology.

No API key, login, SDK, or private data is used.

## Methodology and limits

- Text rankings use current effective input, cache-read, and output prices per million tokens.
- Image and video rankings are separated by billing unit and use the lowest listed effective base or tier price for each model.
- A lower number is not evidence of better quality, latency, uptime, or task fit.
- Different modalities and billing units are not treated as directly comparable.
- Public catalog visibility does not guarantee access for every key or group.
- Verify current pricing and access before making a paid request.

Issues and pull requests are welcome when they improve the generator, explain a billing unit, or identify a reproducible data error.

## License

MIT. Catalog facts remain attributable to their source; this repository's code and documentation are provided under the included license.
