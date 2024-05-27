from typing import Literal
from pathlib import Path
from openai import OpenAI

VoiceType = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class TextToSpeech:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def generate_speech(self, text: str, voice: VoiceType = "alloy", output_format: str = "mp3") -> Path:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        output_file_path = Path(f"data/output.{output_format}")
        response.stream_to_file(output_file_path)
        return output_file_path
