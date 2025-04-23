import pyttsx3 
from gtts import gTTS
import os

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