from pathlib import Path

from scripts.utils import format_time
import whisper
from dotenv import load_dotenv

whisper_model = whisper.load_model("base")
load_dotenv()


def generate_cc(audio_path, language="en"):
    result = whisper_model.transcribe(audio_path, language=language)
    segments = result['segments']

    cc_lines = []
    for i, segment in enumerate(segments):
        start = segment['start']
        end = segment['end']
        text = segment['text']
        if text.strip():
            cc_lines.append(f"{i + 1}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")

    cc_file_path = Path(audio_path).with_suffix(".srt")
    with open(cc_file_path, "w", encoding="utf-8") as cc_file:
        cc_file.writelines(cc_lines)

    return str(cc_file_path)
