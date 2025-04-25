# import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import os
import json
import wave

class SpeechRecognizer:
    def __init__(self):

        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(parent_dir, "vosk-model", "vosk-model-small-en-us-0.15")
        
        # Initialize recognizer
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

        # File parameters
        self.temp_file = "temp_recording.wav"
    
    def recognize_speech(self):
        
        print("\nProcessing speech with Vosk (offline)...")
        
        try:
            wf = wave.open(self.temp_file, "rb")
            
            # Check audio format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                print("Audio file must be WAV format mono PCM.")
                return "Audio format error"
            
            # Process audio
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                self.recognizer.AcceptWaveform(data)
            
            result = json.loads(self.recognizer.FinalResult())
            return result["text"]
        
        except Exception as e:
            return f"Recognition error: {e}"

        