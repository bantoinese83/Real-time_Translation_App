# greeting.py
class Greeting:
    def __init__(self, voice_player, voice_recorder):
        self.voice_player = voice_player
        self.voice_recorder = voice_recorder

    def greet(self):
        greeting_text = "Welcome im P.T.B your personal translator bot!"
        self.voice_player.speak(greeting_text)

    def ask_for_target_language(self):
        prompt_text = "What language you'd like to translate to?"
        self.voice_player.speak(prompt_text)
        return self.voice_recorder.record_and_transcribe()

    def ask_for_input_to_translate(self):
        prompt_text = "Perfect! Now, please speak what you want to translate clearly into the microphone."
        self.voice_player.speak(prompt_text)
        return self.voice_recorder.record_and_transcribe()
