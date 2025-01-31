import pyttsx3
import os
import time
from config.config import AUDIO_OUTPUT_DIR

class TTSGenerator:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice_settings()
        self.setup_output_directory()

    def setup_voice_settings(self):
        """Configure voice settings"""
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # Get available voices and set a female voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def setup_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(AUDIO_OUTPUT_DIR):
            os.makedirs(AUDIO_OUTPUT_DIR)

    def generate_speech(self, text, output_filename=None):
        """
        Convert text to speech and optionally save as audio file
        Returns: Path to the generated audio file if saved, None otherwise
        """
        try:
            # Generate unique filename if not provided
            if output_filename is None:
                output_filename = f"speech_{int(time.time())}.mp3"

            # The full path where we'll save the audio file
            output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)

            # Speak and save to file
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()

            return output_path

        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None

    def speak_text(self, text):
        """
        Speak the text directly without saving
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error speaking text: {str(e)}")
            return False
