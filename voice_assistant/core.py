import os 
import time
from .audio_manager import AudioManager
from .speech_recognizer import SpeechRecognizer
from .speech_synthesizer import SpeechSynthesizer
from .wake_word_detector import WakeWordDetector
from .command_processor import CommandProcessor
import pyaudio

class VoiceAssistant:
    def __init__(self, record_seconds = 5):
        self.record_seconds = record_seconds
        
        # Initialize PyAudio
        self.audio: pyaudio.PyAudio = pyaudio.PyAudio()

        # File parameters
        self.temp_file = "temp_recording.wav"

        # instantiate subclasses
        self.audio_manager = AudioManager(self.audio, self.record_seconds, self.temp_file)
        self.speech_recognizer = SpeechRecognizer()
        self.speech_synthesizer = SpeechSynthesizer()
        self.command_processor = CommandProcessor(self.speech_synthesizer)
        self.wake_word_detector = WakeWordDetector(self.audio_manager, self.speech_recognizer, self.command_processor)  

    def run(self):
        """Run the main application loop."""
        try:
            while True:
                # Clear the terminal
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print("\n=== Benito Voice Assistant ===")
                print("Enter 's' to start test recording (5 seconds)")
                print("Enter 'w' for testing wake word listening mode")
                print("Enter 'r' to make mock request")
                print("Enter 'q' to quit")
                print("-" * 30)
                
                # Use input() instead of keyboard library
                choice = input("> ").strip().lower()
                
                if choice == 's':
                    # audio feedback to start recording
                    self.audio_manager.play_audio_segment(0, 995)
                    
                    # # Record audio
                    self.audio_manager.record_audio()
                    
                    # audio feedback to end recording
                    self.audio_manager.play_audio_segment(2000, 2995)
                    
                    # Recognize speech
                    text = self.speech_recognizer.recognize_speech()


                    # audio feedback that recording has been processed
                    self.audio_manager.play_audio_segment(3095, 4095)

                    # re-play the prompt
                    self.speech_synthesizer.speak_words(text)
                                        
                    # Display results
                    print("\n" + "=" * 50)
                    print("RECOGNIZED TEXT:")
                    print("-" * 50)
                    print(text)
                    print("=" * 50)
                    
                    # input("\nPress Enter to continue...")
                
                elif choice == 'w':
                    self.wake_word_detector.start_wake_word_detection()
                
                elif choice == 'r':
                    print("Enter mock command")
                    
                    user_command_prompt = input()

                    self.command_processor.send_mock_request(user_command_prompt)

                    input("Press Enter to continue...")
                    
                elif choice == 'q':
                    print("\nExiting...")
                    break
                
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        self.audio.terminate()
        
        # Remove temporary file if it exists
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)