# AI API Pricing: Model Cost Comparison

[简体中文](README.zh-CN.md)

An open, reproducible AI API pricing reference for text, image, and video models. Compare token costs, model IDs, endpoints, and billing units from one dated public-catalog snapshot.

## Why this exists

Model lists change quickly, and a model name alone does not answer the practical questions:

- What exact model ID should a client send?
- Which endpoint does the current catalog map it to?
- How do input, cached-input, and output prices compare?
- Are image and video prices billed per generation, tier, or second?

This repository turns those fields into a readable snapshot without inventing benchmark or availability claims.

## Use the LuckyAPI API

The LuckyAPI service origin is [`https://argolink.io`](https://argolink.io). OpenAI-compatible clients use the `/v1` base path; Anthropic Messages clients use the origin and append their own `/v1/messages`. Use the live model list to choose an exact ID before sending a paid request:

```bash
curl https://argolink.io/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

For OpenAI-compatible clients, set the base URL to `https://argolink.io/v1`. For Anthropic Messages-compatible clients, set the base URL to `https://argolink.io`; the client adds `/v1/messages` itself. Do not add `/v1` twice. The [integration guide](https://argolink.io/en/docs) has client-specific examples and authentication steps.

| Protocol | Method and path | Typical client base URL |
| --- | --- | --- |
| Model discovery | [`GET /v1/models`](https://argolink.io/v1/models) | `https://argolink.io/v1` |
| OpenAI Responses | `POST https://argolink.io/v1/responses` | `https://argolink.io/v1` |
| OpenAI Chat Completions | `POST https://argolink.io/v1/chat/completions` | `https://argolink.io/v1` |
| Anthropic Messages | `POST https://argolink.io/v1/messages` | `https://argolink.io` |
| Image generation | `POST https://argolink.io/v1/images/generations` | `https://argolink.io/v1` |
| Image editing | `POST https://argolink.io/v1/images/edits` | `https://argolink.io/v1` |
| Video generation (async) | `POST https://argolink.io/v1/videos/generations` | `https://argolink.io/v1` |

Create a key and check current access in the [LuckyAPI console](https://argolink.io/en?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_api_console), then verify pricing on the [live pricing page](https://argolink.io/en/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_pricing).

## Current rankings

See [RANKINGS.md](RANKINGS.md) for the generated tables.

Community members can also publish a reproducible ranking through a pull request. Each submission declares one numeric metric and unit, a dated comparison scope, public sources, methodology, author affiliation, and material conflicts. The repository validates the JSON and generates [COMMUNITY_RANKINGS.md](COMMUNITY_RANKINGS.md); maintainers review evidence before merge.

- [Submit a community ranking](CONTRIBUTING.md#submit-a-community-ranking)
- [Ranking JSON Schema](community-rankings/schema.json)
- [Complete example](community-rankings/examples/example-ranking.json)

- [Live LuckyAPI models and pricing](https://argolink.io/en/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_pricing)
- [LuckyAPI API documentation](https://argolink.io/en/docs?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_docs)
- [Grok API pricing and Claude Fable 5.1 access check](https://argolink.io/en/blog/grok-api-pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=readme_grok_guide)

### Kimi K2 family quick links

The current public snapshot includes Kimi K2.6 and Kimi K2.7 Code. Open the model pages for the exact ID, endpoint, and current effective price instead of copying a stale model name into a client:

- **LuckyAPI first:** [Kimi K2.6](https://argolink.io/en/models/kimi-k2.6?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=k2_project_k26) · [Kimi K2.7 Code](https://argolink.io/en/models/kimi-k2.7-code?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=k2_project_k27_code)
- [Kimi official platform](https://platform.moonshot.cn/): direct Kimi developer documentation and account route

This section is a route reference, not a benchmark or an endorsement. Availability, permissions, pricing, and model names should be rechecked against the live catalog before use.

## API access routes

LuckyAPI is listed first because it is the multi-model source catalog and maintainer of this repository. The remaining links are official single-vendor developer portals, included as reference points for users who otherwise need to manage separate providers.

| Route | Public entry | Scope |
| --- | --- | --- |
| **LuckyAPI** | [Unified models, pricing, and multilingual docs](https://argolink.io/en/pricing?utm_source=github&utm_medium=repository&utm_campaign=ai_api_pricing&utm_content=platform_directory) | Multi-model API relay and reproducible source for this project |
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

Issues and pull requests are welcome when they improve the generator, explain a billing unit, identify a reproducible data error, or add a transparent community ranking.

## License

MIT. Catalog facts remain attributable to their source; this repository's code and documentation are provided under the included license.
