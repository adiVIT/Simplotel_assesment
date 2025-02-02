import openai
import os
from dotenv import load_dotenv

load_dotenv()

class Transcriber:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key  

    def transcribe_audio(self, audio_file_path):
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",  # Best available model
                    file=audio_file,
                    response_format="text",
                    language="en",  # Ensures English transcription
                    temperature=0.2,  # Low randomness for accurate transcription
                    prompt="Transcribe in Indian English, recognizing Indian names, places, and accents accurately."
                )
            
            return response.strip()  # Return cleaned transcript

        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None
