"""CLI pipeline: audio file -> transcript -> minutes (.md + .json).

Usage:
    python -m src.pipeline meeting.m4a [--model small] [--language en]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minutes import generate_minutes, render_markdown  # noqa: E402
from transcribe import to_transcript, transcribe  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate meeting minutes from a recording.")
    parser.add_argument("audio", help="Path to the audio/video recording")
    parser.add_argument("--model", default="small", help="faster-whisper model size")
    parser.add_argument("--language", default=None, help="Force a language code, e.g. en")
    parser.add_argument("--llm-model", default=None, help="LLM model override")
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"File not found: {args.audio}", file=sys.stderr)
        return 1

    print("Transcribing...")
    segments = transcribe(args.audio, model_size=args.model, language=args.language)
    transcript = to_transcript(segments)

    base, _ = os.path.splitext(args.audio)
    transcript_path = f"{base}.transcript.txt"
    with open(transcript_path, "w", encoding="utf-8") as fh:
        fh.write(transcript + "\n")

    print("Summarizing...")
    minutes = generate_minutes(transcript, model=args.llm_model)

    md_path = f"{base}.minutes.md"
    json_path = f"{base}.minutes.json"
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(minutes))
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(minutes, fh, indent=2)

    print(f"Wrote {transcript_path}, {md_path}, {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
