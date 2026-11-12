"""LLM summarization of a transcript into structured minutes + Markdown."""
from __future__ import annotations

import json
import os

MINUTES_SCHEMA_HINT = """{
  "title": "string",
  "date": "string or null",
  "attendees": ["string"],
  "agenda": ["string"],
  "summary": "3-6 sentence executive summary",
  "decisions": ["string"],
  "action_items": [{"task": "string", "owner": "string or null", "due": "string or null"}],
  "open_questions": ["string"]
}"""

PROMPT = """You are a meticulous meeting secretary. From the transcript below,
produce meeting minutes as a single JSON object with exactly this shape:
{schema}

Rules: only include facts stated in the transcript; mark unknown owners/dates
as null instead of guessing; action items must be commitments someone made,
not general discussion. Transcript:

{transcript}
"""


def generate_minutes(transcript: str, model: str | None = None) -> dict:
    """Call an OpenAI-compatible LLM and parse the structured minutes JSON."""
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "not-needed-for-local"),
        base_url=os.environ.get("OPENAI_BASE_URL") or None,
    )
    response = client.chat.completions.create(
        model=model or os.environ.get("MINUTES_LLM_MODEL", "gpt-4o-mini"),
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": PROMPT.format(schema=MINUTES_SCHEMA_HINT, transcript=transcript)}],
        temperature=0.2,
    )
    return json.loads(response.choices[0].message.content)


def render_markdown(minutes: dict) -> str:
    """Render the structured minutes dict to a clean Markdown document."""
    lines = [f"# {minutes.get('title') or 'Meeting Minutes'}", ""]
    if minutes.get("date"):
        lines += [f"**Date:** {minutes['date']}", ""]
    if minutes.get("attendees"):
        lines += ["**Attendees:** " + ", ".join(minutes["attendees"]), ""]
    if minutes.get("agenda"):
        lines += ["## Agenda", ""] + [f"- {a}" for a in minutes["agenda"]] + [""]
    lines += ["## Summary", "", minutes.get("summary", ""), ""]
    if minutes.get("decisions"):
        lines += ["## Decisions", ""] + [f"- {d}" for d in minutes["decisions"]] + [""]
    if minutes.get("action_items"):
        lines += ["## Action Items", "", "| Task | Owner | Due |", "| --- | --- | --- |"]
        for item in minutes["action_items"]:
            lines.append(f"| {item.get('task', '')} | {item.get('owner') or '—'} | {item.get('due') or '—'} |")
        lines.append("")
    if minutes.get("open_questions"):
        lines += ["## Open Questions", ""] + [f"- {q}" for q in minutes["open_questions"]] + [""]
    return "\n".join(lines).rstrip() + "\n"
