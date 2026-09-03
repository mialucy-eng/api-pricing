#!/usr/bin/env python3
"""Validate community ranking submissions and build their public index."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import quote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parent
COMMUNITY_ROOT = PROJECT_ROOT / "community-rankings"
EXAMPLES_ROOT = COMMUNITY_ROOT / "examples"
SUBMISSIONS_ROOT = COMMUNITY_ROOT / "submissions"
OUTPUT_PATH = PROJECT_ROOT / "COMMUNITY_RANKINGS.md"

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")
GITHUB_RE = re.compile(r"^(?!.*--)[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
CATEGORIES = {"benchmark", "cost", "latency", "price", "quality", "other"}
DIRECTIONS = {"higher_is_better", "lower_is_better"}


class ValidationError(ValueError):
    """A submission does not satisfy the repository contract."""


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f'duplicate JSON key "{key}"')
        result[key] = value
    return result


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValidationError(f"{path}: invalid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: top-level value must be an object")
    return value


def require_keys(value: dict, required: set[str], optional: set[str], context: str) -> None:
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required - optional)
    if missing:
        raise ValidationError(f"{context}: missing fields: {', '.join(missing)}")
    if unknown:
        raise ValidationError(f"{context}: unknown fields: {', '.join(unknown)}")


def require_text(value: object, context: str, maximum: int, minimum: int = 1) -> str:
    if not isinstance(value, str) or value != value.strip():
        raise ValidationError(f"{context}: must be a trimmed string")
    if not minimum <= len(value) <= maximum:
        raise ValidationError(f"{context}: length must be {minimum}-{maximum} characters")
    if any(ord(character) < 32 and character not in "\t" for character in value):
        raise ValidationError(f"{context}: contains a control character")
    return value


def require_date(value: object, context: str) -> str:
    text = require_text(value, context, 10, 10)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{context}: must be a valid YYYY-MM-DD date") from exc
    if parsed > date.today():
        raise ValidationError(f"{context}: must not be in the future")
    return text


def require_url(value: object, context: str) -> str:
    text = require_text(value, context, 2048)
    parsed = urlsplit(text)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValidationError(f"{context}: must be a public https URL without credentials")
    if any(character.isspace() for character in text):
        raise ValidationError(f"{context}: URL must not contain whitespace")
    return text


def validate_submission(value: dict, path: Path) -> dict:
    context = str(path.relative_to(PROJECT_ROOT))
    require_keys(
        value,
        {
            "schema_version",
            "id",
            "title",
            "summary",
            "category",
            "metric",
            "scope",
            "methodology",
            "sources",
            "author",
            "conflicts",
            "entries",
        },
        set(),
        context,
    )
    if value["schema_version"] != 1:
        raise ValidationError(f"{context}.schema_version: only version 1 is supported")

    ranking_id = require_text(value["id"], f"{context}.id", 80, 3)
    if not SLUG_RE.fullmatch(ranking_id):
        raise ValidationError(f"{context}.id: use lowercase letters, numbers, and hyphens")
    if path.parent == SUBMISSIONS_ROOT and path.stem != ranking_id:
        raise ValidationError(f"{context}: filename must be {ranking_id}.json")

    require_text(value["title"], f"{context}.title", 120, 8)
    require_text(value["summary"], f"{context}.summary", 320, 20)
    category = require_text(value["category"], f"{context}.category", 24)
    if category not in CATEGORIES:
        raise ValidationError(f"{context}.category: choose one of {', '.join(sorted(CATEGORIES))}")
    require_text(value["methodology"], f"{context}.methodology", 2000, 40)

    metric = value["metric"]
    if not isinstance(metric, dict):
        raise ValidationError(f"{context}.metric: must be an object")
    require_keys(metric, {"name", "unit", "direction"}, set(), f"{context}.metric")
    require_text(metric["name"], f"{context}.metric.name", 80, 2)
    require_text(metric["unit"], f"{context}.metric.unit", 40, 1)
    direction = require_text(metric["direction"], f"{context}.metric.direction", 32)
    if direction not in DIRECTIONS:
        raise ValidationError(f"{context}.metric.direction: choose one of {', '.join(sorted(DIRECTIONS))}")

    scope = value["scope"]
    if not isinstance(scope, dict):
        raise ValidationError(f"{context}.scope: must be an object")
    require_keys(scope, {"as_of", "market", "inclusion", "exclusions"}, set(), f"{context}.scope")
    require_date(scope["as_of"], f"{context}.scope.as_of")
    require_text(scope["market"], f"{context}.scope.market", 80, 2)
    require_text(scope["inclusion"], f"{context}.scope.inclusion", 500, 20)
    require_text(scope["exclusions"], f"{context}.scope.exclusions", 500, 10)

    author = value["author"]
    if not isinstance(author, dict):
        raise ValidationError(f"{context}.author: must be an object")
    require_keys(author, {"github", "affiliation"}, set(), f"{context}.author")
    github = require_text(author["github"], f"{context}.author.github", 39)
    if not GITHUB_RE.fullmatch(github):
        raise ValidationError(f"{context}.author.github: invalid GitHub username")
    require_text(author["affiliation"], f"{context}.author.affiliation", 120, 2)

    conflicts = value["conflicts"]
    if not isinstance(conflicts, list) or len(conflicts) > 10:
        raise ValidationError(f"{context}.conflicts: must be an array with at most 10 items")
    for index, conflict in enumerate(conflicts):
        require_text(conflict, f"{context}.conflicts[{index}]", 300, 3)

    sources = value["sources"]
    if not isinstance(sources, list) or not 1 <= len(sources) <= 20:
        raise ValidationError(f"{context}.sources: must contain 1-20 public sources")
    source_urls = set()
    for index, source in enumerate(sources):
        source_context = f"{context}.sources[{index}]"
        if not isinstance(source, dict):
            raise ValidationError(f"{source_context}: must be an object")
        require_keys(source, {"label", "url", "accessed_at"}, set(), source_context)
        require_text(source["label"], f"{source_context}.label", 120, 2)
        source_url = require_url(source["url"], f"{source_context}.url")
        require_date(source["accessed_at"], f"{source_context}.accessed_at")
        if source_url in source_urls:
            raise ValidationError(f"{source_context}.url: duplicate source URL")
        source_urls.add(source_url)

    entries = value["entries"]
    if not isinstance(entries, list) or not 2 <= len(entries) <= 100:
        raise ValidationError(f"{context}.entries: must contain 2-100 comparable entries")
    entry_keys = set()
    for index, entry in enumerate(entries):
        entry_context = f"{context}.entries[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{entry_context}: must be an object")
        require_keys(entry, {"name", "provider", "value", "source_url"}, {"notes"}, entry_context)
        name = require_text(entry["name"], f"{entry_context}.name", 120, 1)
        provider = require_text(entry["provider"], f"{entry_context}.provider", 80, 1)
        if isinstance(entry["value"], bool) or not isinstance(entry["value"], (int, float)):
            raise ValidationError(f"{entry_context}.value: must be a number")
        if not float("-inf") < float(entry["value"]) < float("inf"):
            raise ValidationError(f"{entry_context}.value: must be finite")
        source_url = require_url(entry["source_url"], f"{entry_context}.source_url")
        if source_url not in source_urls:
            raise ValidationError(f"{entry_context}.source_url: must match a declared source URL")
        if "notes" in entry:
            require_text(entry["notes"], f"{entry_context}.notes", 300, 2)
        entry_key = (name.casefold(), provider.casefold())
        if entry_key in entry_keys:
            raise ValidationError(f"{entry_context}: duplicate name/provider pair")
        entry_keys.add(entry_key)

    return value


def markdown_text(value: object) -> str:
    text = html.escape(str(value), quote=False).replace("\r", " ").replace("\n", " ")
    for character in ("\\", "`", "*", "_", "|", "[", "]"):
        text = text.replace(character, f"&#{ord(character)};")
    return text


def markdown_url(value: str) -> str:
    return quote(value, safe=":/?&=#%+,-._~@;")


def format_number(value: int | float) -> str:
    return f"{float(value):.8f}".rstrip("0").rstrip(".")


def ranked_entries(submission: dict) -> list[dict]:
    multiplier = -1 if submission["metric"]["direction"] == "higher_is_better" else 1
    return sorted(
        submission["entries"],
        key=lambda entry: (
            multiplier * float(entry["value"]),
            entry["name"].casefold(),
            entry["provider"].casefold(),
        ),
    )


def render_submission(submission: dict) -> list[str]:
    source_numbers = {source["url"]: index for index, source in enumerate(submission["sources"], start=1)}
    conflicts = submission["conflicts"]
    lines = [
        f'<a id="ranking-{submission["id"]}"></a>',
        "",
        f"## {markdown_text(submission['title'])}",
        "",
        markdown_text(submission["summary"]),
        "",
        f"- **Category:** {markdown_text(submission['category'])}",
        f"- **Metric:** {markdown_text(submission['metric']['name'])} "
        f"(`{markdown_text(submission['metric']['unit'])}`, "
        f"`{markdown_text(submission['metric']['direction'])}`)",
        f"- **Scope date:** `{markdown_text(submission['scope']['as_of'])}`; "
        f"market: {markdown_text(submission['scope']['market'])}",
        f"- **Contributor:** [@{markdown_text(submission['author']['github'])}]"
        f"(https://github.com/{markdown_url(submission['author']['github'])}); "
        f"affiliation: {markdown_text(submission['author']['affiliation'])}",
        f"- **Conflicts:** {markdown_text('; '.join(conflicts) if conflicts else 'None declared')}",
        "",
        f"**Inclusion rule:** {markdown_text(submission['scope']['inclusion'])}",
        "",
        f"**Exclusions:** {markdown_text(submission['scope']['exclusions'])}",
        "",
        f"**Methodology:** {markdown_text(submission['methodology'])}",
        "",
        "| Rank | Entry | Provider | Value | Source | Notes |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    for rank, entry in enumerate(ranked_entries(submission), start=1):
        source_number = source_numbers[entry["source_url"]]
        lines.append(
            f"| {rank} | {markdown_text(entry['name'])} | {markdown_text(entry['provider'])} | "
            f"{format_number(entry['value'])} {markdown_text(submission['metric']['unit'])} | "
            f"[S{source_number}]({markdown_url(entry['source_url'])}) | "
            f"{markdown_text(entry.get('notes', '-'))} |"
        )
    lines.extend(["", "**Sources**", ""])
    for index, source in enumerate(submission["sources"], start=1):
        lines.append(
            f"- **S{index}:** [{markdown_text(source['label'])}]({markdown_url(source['url'])}), "
            f"accessed `{markdown_text(source['accessed_at'])}`"
        )
    lines.append("")
    return lines


def build_markdown(submissions: list[dict]) -> str:
    lines = [
        "# Community Rankings",
        "",
        "> Generated from reviewed JSON files under `community-rankings/submissions/`. "
        "Do not edit this file by hand.",
        "",
        "Community rankings are contributor-authored comparisons with declared scope, methodology, "
        "sources, and conflicts. Merge means the submission passed repository checks; it is not a "
        "LuckyAPI endorsement or a guarantee of quality, price, latency, availability, or future results.",
        "",
    ]
    if not submissions:
        lines.extend(
            [
                "No community ranking has been merged yet. See [Contributing](CONTRIBUTING.md) to submit "
                "the first reproducible ranking by pull request.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(["## Index", ""])
    for submission in submissions:
        lines.append(f"- [{markdown_text(submission['title'])}](#ranking-{submission['id']})")
    lines.append("")
    for submission in submissions:
        lines.extend(render_submission(submission))
    return "\n".join(lines)


def atomic_write(path: Path, content: str) -> None:
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as handle:
            handle.write(content)
            temporary_path = Path(handle.name)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def load_rankings() -> tuple[list[dict], int]:
    examples = sorted(EXAMPLES_ROOT.glob("*.json"))
    submissions = sorted(SUBMISSIONS_ROOT.glob("*.json")) if SUBMISSIONS_ROOT.exists() else []
    for path in examples:
        validate_submission(load_json(path), path)
    loaded = [validate_submission(load_json(path), path) for path in submissions]
    ids = [submission["id"] for submission in loaded]
    if len(ids) != len(set(ids)):
        raise ValidationError("community-rankings/submissions: duplicate ranking id")
    return sorted(loaded, key=lambda item: item["id"]), len(examples)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate inputs and fail if output is stale")
    args = parser.parse_args()

    try:
        submissions, example_count = load_rankings()
        rendered = build_markdown(submissions)
        if args.check:
            current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
            if current != rendered:
                raise ValidationError("COMMUNITY_RANKINGS.md is stale; run python3 community_rankings.py")
            print(f"validated {len(submissions)} submissions and {example_count} examples; output is current")
            return
        atomic_write(OUTPUT_PATH, rendered)
        print(f"wrote {OUTPUT_PATH.name} from {len(submissions)} submissions; validated {example_count} examples")
    except (OSError, ValidationError) as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    main()
