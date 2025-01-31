from src.speech_to_text.recorder import AudioRecorder
from src.speech_to_text.transcriber import Transcriber
import time

def test_recording_and_transcription():
    # Initialize recorder
    recorder = AudioRecorder()
    
    # Start recording
    print("Recording started... Speak now!")
    recorder.start_recording()
    
    # Record for 5 seconds
    time.sleep(5)
    
    # Stop recording
    recorder.stop_recording()
    print("Recording stopped.")
    
    # Save the audio file
    recorder.save_audio("test_recording.wav")
    
    # Transcribe the audio
    transcriber = Transcriber()
    text = transcriber.transcribe_audio("test_recording.wav")
    
    print(f"Transcribed text: {text}")

if __name__ == "__main__":
    test_recording_and_transcription()
