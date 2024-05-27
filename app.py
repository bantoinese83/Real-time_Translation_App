import os
import sys
import threading
from pydub import AudioSegment
from pydub.playback import play
from greeting import Greeting
from stt import SpeechToText
from translator import Translator
from tts import TextToSpeech
from voice_player import VoicePlayer
from voice_recorder import VoiceRecorder
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# Set the duration of the recording in seconds
RECORDING_DURATION = 10

# Set the sample rate
SAMPLE_RATE = 44100

# Set the output file path for the recording
OUTPUT_FILE_PATH = "data/recording.wav"

# Set the source language
SOURCE_LANGUAGE = "en"


def play_processing_sound(stop_event):
    """Define a function to play the processing sound in a loop."""
    processing_sound = AudioSegment.from_file("assets/processing_response_sound.mp3")
    while not stop_event.is_set():
        play(processing_sound)


def main():
    print("Welcome to the Multilingual Translator!")
    translator = Translator(API_KEY)
    tts = TextToSpeech(API_KEY)
    stt = SpeechToText(API_KEY)
    voice_player = VoicePlayer(tts)
    voice_recorder = VoiceRecorder(stt, RECORDING_DURATION, SAMPLE_RATE, OUTPUT_FILE_PATH)
    greeting = Greeting(voice_player, voice_recorder)
    greeting.greet()

    while True:  # Run in a loop until the user decides to quit
        try:
            # Ask for the target language and text to translate
            TARGET_LANGUAGE = greeting.ask_for_target_language()
            voice_player.speak(f"nice: {TARGET_LANGUAGE} that's a cool language!")
            print(f"Target Language: {TARGET_LANGUAGE}")
            original_text = greeting.ask_for_input_to_translate()
            voice_player.speak(f"you said: {original_text}")
            voice_player.speak(f"let me translate that for you")
            print(f"Original Text: {original_text}")

            # Create a stop event for the processing sound thread
            stop_event = threading.Event()

            # Start playing the processing sound in a separate thread
            processing_sound_thread = threading.Thread(target=play_processing_sound, args=(stop_event,), daemon=True)
            processing_sound_thread.start()

            # Translate text
            translated_text = translator.translate_text(original_text, SOURCE_LANGUAGE, TARGET_LANGUAGE)
            print(f"Translated Text: {translated_text}")

            # Stop the processing sound
            stop_event.set()
            processing_sound_thread.join()

            # Speak the translated language
            voice_player.speak(translated_text)
            voice_player.speak("I can translate more languages if you want. Just let me know!")

            # Ask the user if they want to quit
            voice_player.speak("Are you done translating? Press 'q' to quit or any other key to translate more.")
            quit_app = input("Press 'q' to quit or any other key to translate more: ")
            if quit_app.lower() == 'q':
                break

        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
