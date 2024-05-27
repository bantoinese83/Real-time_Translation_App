# voice_player.py
import os
from pydub import AudioSegment
from pydub.playback import play


class VoicePlayer:
    def __init__(self, tts):
        self.tts = tts

    def speak(self, text):
        # Generate speech from the text
        output_audio_path = self.tts.generate_speech(text)

        # Play the generated speech
        audio = AudioSegment.from_file(output_audio_path, format="mp3")
        play(audio)

        # Remove the audio file after playing it
        os.remove(output_audio_path)
