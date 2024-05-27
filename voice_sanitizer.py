from pydub import AudioSegment
from pydub.effects import normalize


class VoiceSanitizer:
    def __init__(self, noise_level=-40):
        self.noise_level = noise_level

    def sanitize(self, audio_data):
        try:
            audio = AudioSegment.from_file(audio_data)
            audio = audio.low_pass_filter(3000).high_pass_filter(200)  # Reduce noise
            audio = normalize(audio)  # Normalize volume
            audio = audio.strip_silence(silence_thresh=self.noise_level)  # Trim silence

            # Export the sanitized audio to the same file
            audio.export(audio_data, format="wav")

            return audio_data
        except Exception as e:
            print(f"An error occurred while sanitizing the audio: {e}")
            return None
