import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

class Transcriber:
    def __init__(self):
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        aai.settings.api_key = self.api_key

    def transcribe_audio(self, audio_file_path):
        try:
            # Create a transcriber
            transcriber = aai.Transcriber()
            
            # Start transcription
            transcript = transcriber.transcribe(audio_file_path)
            
            # Return the transcribed text
            return transcript.text
            
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None
