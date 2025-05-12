import os
import wave
from piper import PiperVoice
import platform

class SpeechSynthesizer:   
    def speak_words(self, text):
        # Path to models in the parent directory
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(parent_dir, "piper-models", "en_GB-semaine-medium.onnx")
        model_config_path = os.path.join(parent_dir, "piper-models", "en_GB-semaine-medium.onnx.json")
        
        # Load the Piper voice
        voice = PiperVoice.load(model_path, model_config_path)
        
        # Create a temporary WAV file
        temp_file = "temp_speech.wav"
        
        # Create and configure the WAV file
        with wave.open(temp_file, "wb") as wav_file:
            # Generate speech directly to the WAV file
            voice.synthesize(text, wav_file, length_scale=0.75)
        
        # Play the audio using current platform's built-in player
        system = platform.system().lower()
        if system == 'darwin':  # macOS
            os.system(f"afplay {temp_file}")
        elif system == 'linux':  # Linux/Raspberry Pi
            os.system(f"aplay {temp_file}")
        else:
            print(f"Unsupported OS: {system}. Cannot play audio.")