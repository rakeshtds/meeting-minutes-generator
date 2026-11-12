# Meeting Minutes Generator

Upload a meeting recording and get polished minutes — summary, decisions and action items with owners — from Whisper transcription plus LLM summarization.

## Features

- Transcription with faster-whisper (word-level language detection, VAD filtering)
- Optional speaker diarization hooks (segments carry speaker labels when a diarization model is configured)
- LLM summarization into a fixed minutes template: attendees, agenda, summary, decisions, action items (task / owner / due), open questions
- Structured JSON intermediate, rendered to clean Markdown minutes
- CLI pipeline: one command from audio file to finished minutes
- Runs fully offline for transcription; the LLM step works with any OpenAI-compatible API or a local endpoint

## Architecture

`pipeline.py` orchestrates: audio → `transcribe.py` (faster-whisper, timestamped segments) → transcript text → `minutes.py` (LLM prompt with structured JSON output) → Markdown renderer → `minutes.md` + `minutes.json` written next to the audio file.

## Tech Stack

Python 3.11 · faster-whisper · OpenAI-compatible LLM API · Docker (optional)

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...          # or point OPENAI_BASE_URL at a local model
# optional Docker:
docker build -t minutes .
```

## Usage

```bash
python -m src.pipeline meeting.m4a --model small --language en
# outputs: meeting.minutes.md and meeting.minutes.json

docker run --rm -v "$PWD:/data" -e OPENAI_API_KEY minutes /data/meeting.m4a
```

## Example Output

See `sample/minutes_example.md` for a complete rendered example.

## Project Structure

```
src/transcribe.py   faster-whisper transcription with segment formatting
src/minutes.py      LLM prompt, structured output parsing, Markdown renderer
src/pipeline.py     CLI: audio -> transcript -> minutes
Dockerfile          Container image with ffmpeg + Python deps
sample/             Example rendered minutes
```

## Roadmap

- Built-in diarization via pyannote
- Calendar integration to pre-fill attendees and agenda
- Summary email / Slack posting step

---

An original implementation built for portfolio purposes. Sample data is synthetic.
