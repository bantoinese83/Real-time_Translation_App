import sounddevice as sd
from scipy.io.wavfile import write


class VoiceRecorder:
    def __init__(self, stt, recording_duration=10, sample_rate=44100, output_file_path="data/recording.wav",
                 sanitizer=None):
        self.append_audio_callback = None
        self.stt = stt
        self.recording_duration = recording_duration
        self.sample_rate = sample_rate
        self.output_file_path = output_file_path
        self.sanitizer = sanitizer

    def record_and_transcribe(self):
        # Record audio from the default microphone
        recording = sd.rec(int(self.recording_duration * self.sample_rate), samplerate=self.sample_rate, channels=1)
        sd.wait()
        write(self.output_file_path, self.sample_rate, recording)

        # Sanitize the audio
        if self.sanitizer:
            self.output_file_path = self.sanitizer.sanitize(self.output_file_path)

        # Convert speech to text
        return self.stt.transcribe_audio(self.output_file_path)

    def set_append_audio_callback(self, callback):
        self.append_audio_callback = callback

    def append_audio(self, audio_data):
        if self.append_audio_callback:
            self.append_audio_callback(audio_data)
        else:
            print("Error: No append audio callback set.")
