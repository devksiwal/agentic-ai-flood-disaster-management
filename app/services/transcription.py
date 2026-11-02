
from dataclasses import dataclass
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass
class TranscriptionResult:
    original_transcript: str
    detected_language: str
    language_probability: float


class TranscriptionService:
    def __init__(self, model_size: str = "base"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str | Path) -> TranscriptionResult:
        path = Path(audio_path)

        if not path.is_file():
            raise FileNotFoundError("Audio file was not found.")

        segments, info = self.model.transcribe(
            str(path),
            task="transcribe",
            beam_size=5,
            vad_filter=True,
        )

        transcript = " ".join(
            segment.text.strip() for segment in segments
        ).strip()

        if not transcript:
            raise ValueError(
                "No speech could be transcribed from this recording."
            )

        return TranscriptionResult(
            original_transcript=transcript,
            detected_language=info.language,
            language_probability=info.language_probability,
        )
