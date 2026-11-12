"""Audio transcription with faster-whisper."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: str | None = None

    def __str__(self) -> str:
        stamp = f"[{int(self.start // 60):02d}:{int(self.start % 60):02d}]"
        who = f"{self.speaker}: " if self.speaker else ""
        return f"{stamp} {who}{self.text.strip()}"


def transcribe(audio_path: str, model_size: str = "small", language: str | None = None) -> list[Segment]:
    """Transcribe an audio/video file into timestamped segments.

    model_size: any faster-whisper size (tiny, base, small, medium, large-v3).
    """
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="auto", compute_type="auto")
    raw_segments, info = model.transcribe(
        audio_path,
        language=language,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    segments = [Segment(start=s.start, end=s.end, text=s.text) for s in raw_segments]
    print(f"Detected language '{info.language}' (p={info.language_probability:.2f}); "
          f"{len(segments)} segments")
    return segments


def to_transcript(segments: list[Segment]) -> str:
    """Render segments as a timestamped plain-text transcript."""
    return "\n".join(str(s) for s in segments)
