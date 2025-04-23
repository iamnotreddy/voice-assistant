import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()

        # File parameters
        self.temp_file = "temp_recording.wav"
    
    def recognize_speech(self):
        """
        Convert recorded audio to text using speech recognition.
        
        Returns:
            str: Recognized text
        """
        
        print("\nProcessing speech...")
        
        try:
            # Load the recorded audio file
            with sr.AudioFile(self.temp_file) as source:
                audio_data = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data)
                
                return text
                
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
            
        except sr.RequestError as e:
            return f"Could not request results from speech recognition service; {e}"