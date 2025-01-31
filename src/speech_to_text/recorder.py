import pyaudio
import wave
import threading
import time

class AudioRecorder:
    def __init__(self):
        self.audio_format = pyaudio.paFloat32
        self.channels = 1
        self.sample_rate = 16000
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        threading.Thread(target=self._record).start()

    def stop_recording(self):
        self.is_recording = False

    def _record(self):
        stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

    def save_audio(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
