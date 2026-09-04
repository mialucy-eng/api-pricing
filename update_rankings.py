#!/usr/bin/env python3
"""Build reproducible AI API pricing tables from LuckyAPI's public catalog."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


CATALOG_URL = "https://argolink.io/api/catalog/v1/catalog"
PROJECT_ROOT = Path(__file__).resolve().parent
SNAPSHOT_PATH = PROJECT_ROOT / "catalog-snapshot.json"
RANKINGS_PATH = PROJECT_ROOT / "RANKINGS.md"
TRACKING_PARAMS = {
    "utm_source": "github",
    "utm_medium": "repository",
    "utm_campaign": "ai_api_pricing",
}


def fetch_catalog() -> dict:
    request = Request(
        CATALOG_URL,
        headers={"User-Agent": "ai-api-pricing/1.0"},
    )
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"catalog returned HTTP {response.status}")
        return json.load(response)


def catalog_data(catalog: dict) -> tuple[list[dict], str]:
    if not isinstance(catalog, dict):
        raise ValueError("catalog must be a JSON object")
    models = catalog.get("models") or catalog.get("data") or catalog.get("items")
    if not isinstance(models, list) or not models:
        raise ValueError("catalog must contain a non-empty model list")
    if any(not isinstance(model, dict) or not model.get("id") for model in models):
        raise ValueError("every catalog model must be an object with an id")
    revision = catalog.get("revision") or catalog.get("etag") or catalog.get("version")
    if revision is None or not str(revision).strip():
        raise ValueError("catalog revision is required")
    return models, str(revision)


def money(value: float | int | None) -> str:
    if value is None:
        return "-"
    rendered = f"{float(value):.6f}".rstrip("0").rstrip(".")
    return f"${rendered}"


def tracked_url(path: str, content: str) -> str:
    query = urlencode({**TRACKING_PARAMS, "utm_content": content})
    return f"https://argolink.io{path}?{query}"


def model_link(model: dict) -> str:
    model_id = model["id"]
    url = tracked_url(f"/en/models/{quote(model_id, safe='')}", f"model_{model_id}")
    return f"[`{model_id}`]({url})"


def chat_rows(models: list[dict], field: str) -> list[str]:
    ranked = []
    for model in models:
        if model.get("category") != "chat":
            continue
        effective = model.get("pricing", {}).get("effective", {})
        value = effective.get(field)
        if value is not None:
            ranked.append((float(value), model))
    ranked.sort(key=lambda item: (item[0], item[1]["id"]))
    return [
        f"| {index} | {model_link(model)} | {model.get('provider_id', '-')} | "
        f"{money(value)} | `{model.get('endpoint', '-')}` |"
        for index, (value, model) in enumerate(ranked, start=1)
    ]


def minimum_generation_price(model: dict) -> tuple[float, str, str] | None:
    effective = model.get("pricing", {}).get("effective", {})
    candidates: list[tuple[float, str]] = []
    unit = str(effective.get("unit") or "generation")
    base = effective.get("generation_per_unit")
    if base is not None:
        candidates.append((float(base), unit))
    for tier in effective.get("tiers", []):
        price = tier.get("price")
        if price is not None:
            candidates.append((float(price), str(tier.get("label", "tier"))))
    if not candidates:
        return None
    value, label = min(candidates, key=lambda item: item[0])
    return value, label, unit


def generation_sections(models: list[dict], category: str) -> list[str]:
    grouped: dict[str, list[tuple[float, dict, str]]] = {}
    for model in models:
        if model.get("category") != category:
            continue
        minimum = minimum_generation_price(model)
        if minimum:
            value, label, unit = minimum
            grouped.setdefault(unit, []).append((value, model, label))

    lines: list[str] = []
    for unit in sorted(grouped):
        ranked = sorted(grouped[unit], key=lambda item: (item[0], item[1]["id"]))
        lines.extend(
            [
                f"### Billing unit: `{unit}`",
                "",
                "| Rank within unit | Model ID | Provider | Lowest listed price | Tier / label | Endpoint |",
                "| ---: | --- | --- | ---: | --- | --- |",
                *[
                    f"| {index} | {model_link(model)} | {model.get('provider_id', '-')} | "
                    f"{money(value)} | {label} | `{model.get('endpoint', '-')}` |"
                    for index, (value, model, label) in enumerate(ranked, start=1)
                ],
                "",
            ]
        )
    return lines


def atomic_write(path: Path, content: str) -> None:
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(content)
            temporary_path = Path(handle.name)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def build_markdown(catalog: dict, fetched_at: str) -> str:
    models, revision = catalog_data(catalog)
    providers: dict[str, int] = {}
    for model in models:
        provider = model.get("provider_id", "unknown")
        providers[provider] = providers.get(provider, 0) + 1

    lines = [
        "# AI API Price Rankings",
        "",
        f"> Snapshot generated from the [LuckyAPI public catalog]({CATALOG_URL}) at "
        f"`{fetched_at}`. Catalog revision: `{revision}`.",
        "",
        "This is a price ranking, not a quality, speed, uptime, or availability ranking. "
        "Prices and model access can change; verify the "
        f"[live pricing page]({tracked_url('/en/pricing', 'rankings_pricing')}) "
        "and your key before paid traffic.",
        "",
        f"Current snapshot: **{len(models)} models** across **{len(providers)} providers** "
        f"({', '.join(f'{name}: {count}' for name, count in sorted(providers.items()))}).",
        "",
        "## Text models ranked by input price",
        "",
        "| Rank | Model ID | Provider | USD / 1M input tokens | Endpoint |",
        "| ---: | --- | --- | ---: | --- |",
        *chat_rows(models, "input_per_million"),
        "",
        "## Text models ranked by cache-read price",
        "",
        "| Rank | Model ID | Provider | USD / 1M cached input tokens | Endpoint |",
        "| ---: | --- | --- | ---: | --- |",
        *chat_rows(models, "cached_input_per_million"),
        "",
        "## Text models ranked by output price",
        "",
        "| Rank | Model ID | Provider | USD / 1M output tokens | Endpoint |",
        "| ---: | --- | --- | ---: | --- |",
        *chat_rows(models, "output_per_million"),
        "",
        "## Image models grouped by billing unit and ranked by lowest listed tier",
        "",
        *generation_sections(models, "image"),
        "",
        "## Video models grouped by billing unit and ranked by lowest listed tier",
        "",
        *generation_sections(models, "video"),
        "",
        "## Methodology",
        "",
        "- Text tables sort the catalog's current `pricing.effective` token fields in ascending order.",
        "- Image and video tables group models by billing unit, then sort each model's lowest "
        "listed effective base or tier price. Rankings reset for every billing unit.",
        "- Missing price fields are omitted rather than guessed.",
        "- Catalog visibility does not guarantee access for every API key or group.",
        "- Vendor benchmarks and marketing claims are not used in these rankings.",
        "",
        "For a worked token-cost example and current Grok access checks, read the "
        f"[Grok API pricing guide]({tracked_url('/en/blog/grok-api-pricing', 'rankings_grok_guide')}).",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    catalog = fetch_catalog()
    models, revision = catalog_data(catalog)
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    snapshot = {
        "source": CATALOG_URL,
        "fetched_at": fetched_at,
        "revision": revision,
        "models": models,
    }
    atomic_write(
        SNAPSHOT_PATH,
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
    )
    atomic_write(RANKINGS_PATH, build_markdown(catalog, fetched_at))
    print(f"wrote {SNAPSHOT_PATH.name} and {RANKINGS_PATH.name}")


if __name__ == "__main__":
    main()
