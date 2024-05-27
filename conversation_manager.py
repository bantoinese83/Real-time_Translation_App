import threading
from enum import Enum


class ConversationState(Enum):
    LISTENING = 1
    SPEAKING = 2
    WAITING = 3


class ConversationManager:
    def __init__(self, voice_player, voice_recorder):
        self.input_event = threading.Event()
        self.voice_player = voice_player
        self.voice_recorder = voice_recorder
        self.state = ConversationState.WAITING

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def handle_user_input(self, user_input):
        if self.state == ConversationState.LISTENING:
            # Process the user's input
            self.voice_recorder.record_and_transcribe(user_input)
            self.state = ConversationState.SPEAKING
        elif self.state == ConversationState.SPEAKING:
            # Wait for the bot to finish speaking
            self.state = ConversationState.WAITING

    def handle_conversation(self):
        while True:
            if self.state == ConversationState.SPEAKING:
                # Bot speaks
                self.voice_player.speak("Hello! Tell me something and I will translate it for you.")
                self.state = ConversationState.LISTENING
            elif self.state == ConversationState.LISTENING:
                # Bot listens and waits for the user to speak
                pass
            elif self.state == ConversationState.WAITING:
                # Bot is waiting for the user to respond
                print("Bot is waiting for user input...")
                self.voice_player.speak("Please say something...")
                self.state = ConversationState.LISTENING
                self.input_event.wait()
