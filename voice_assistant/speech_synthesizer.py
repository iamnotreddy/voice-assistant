import pyttsx3 
from gtts import gTTS
import os
import wave
from piper import PiperVoice

class SpeechSynthesizer:
    def speak_words(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
    def speak_words_v2(self, text):
        tts = gTTS(text=text, lang='en', tld="co.uk", slow=False)
    
        # Save to a temporary file
        temp_file = "temp_speech.mp3"
        tts.save(temp_file)
        
        # Use Mac's built-in audio player
        os.system(f"afplay {temp_file}")
    
    def speak_words_v3(self, text):
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
        
        # Play the audio using Mac's built-in player
        os.system(f"afplay {temp_file}")