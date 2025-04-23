import shutil
import os
from pocketsphinx import Pocketsphinx
import pyaudio
import time

from .audio_manager import AudioManager
from .speech_recognizer import SpeechRecognizer
from .command_processor import CommandProcessor

class WakeWordDetector:
    def __init__(
        self, 
        audio_manager: AudioManager, 
        speech_recognizer: SpeechRecognizer, 
        command_processor: CommandProcessor
        ):
            self.audio_manager = audio_manager
            self.speech_recognizer = speech_recognizer
            self.command_processor = command_processor
    
    def start_wake_word_detection(self):
        print("\n=== Wake Word Detection Mode ===")
        print("Listening for 'Hey Benito'...")
        print("Press Ctrl+C to stop")
        print("-" * 30)

        # Use the exact paths found in your environment
        hmm_path = '/Users/raveen/repos/voice-client/venv/lib/python3.13/site-packages/pocketsphinx/model/en-us/en-us'

        # Create directory if it doesn't exist
        dict_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionary")
        if not os.path.exists(dict_dir):
            os.makedirs(dict_dir)
            
        # Create a custom dictionary with our wake word
        custom_dict_path = os.path.join(dict_dir, "benito_dict.dict")

        # Create minimal dictionary with just our wake word components
        try:
            with open(custom_dict_path, 'w') as f:
                # Just include our wake word components and nothing else
                f.write("HEY HH EY\n")
                f.write("BENITO B EH N IY T OW\n")
                
        except Exception as e:
            print(f"Error creating minimal dictionary: {e}")
            return

        # Create keyword file
        kws_path = os.path.join(dict_dir, "hey_benito.txt")
        try:
            with open(kws_path, 'w') as f:
                f.write("HEY BENITO /1e-20/\n")  # Very sensitive setting
        except Exception as e:
            print(f"Error creating keyword file: {e}")
            return
        
        # Initialize PocketSphinx with the correct paths
        try:
            ps = Pocketsphinx(hmm=hmm_path, dict=custom_dict_path, kws=kws_path)
            print("PocketSphinx initialized successfully!")
        except Exception as e:
            print(f"Error initializing PocketSphinx: {e}")
            return

        # Set up audio input
        p = self.audio_manager.audio
        
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("Starting wake word detection...")
        
        try:
            # Explicitly start the utterance
            ps.start_utt()
            print("Utterance started successfully")
            print("Listening... Press Ctrl+C to exit at any time.")
            
            while True:
                try:
                    # Use a small timeout to make the loop more responsive to KeyboardInterrupt
                    data = stream.read(1024, exception_on_overflow=False)
                    
                    # Process the raw audio
                    ps.process_raw(data, False, False)
                    
                    # Check if wake word was detected
                    hypothesis = ps.hypothesis()
                    
                    if hypothesis and len(hypothesis.strip()) > 0:
                        print(f"Detected: {hypothesis}")
                        
                        if "hey benito" in hypothesis.lower():
                            print("\n🔊 Wake word detected! 🔊")
                            
                            # End current utterance
                            ps.end_utt()
                            stream.stop_stream()
                            stream.close()
                            time.sleep(0.2)
                            
                            print("Closed wake word detection stream")
                            
                            # Play audio feedback for wake word detection
                            self.audio_manager.play_audio_segment(0, 995)
                            
                            # Record audio for command
                            print("Listening for command for three seconds...")
                            self.audio_manager.record_audio()
                            
                            # Play audio feedback for end of recording
                            self.audio_manager.play_audio_segment(2000, 2995)
                            
                            # Recognize speech
                            command_text = self.speech_recognizer.recognize_speech()
                            
                            # Play audio feedback that recording has been processed
                            self.audio_manager.play_audio_segment(3095, 4095)
                            
                            print('processed command: ', command_text)

                            # make request
                            self.command_processor.send_request(command_text)
                            
                            print("\nListening for 'Hey Benito' again...")
                            
                            # Start a new utterance for the next detection
                            # Open a new stream with the same PyAudio instance
                            
                            stream = p.open(
                                format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                input=True,
                                frames_per_buffer=1024
                            )
                            
                            ps.start_utt()
                            print("Ready for next detection")
                    
                except KeyboardInterrupt:
                    # Re-raise to be caught by the outer try/except
                    raise
                    
                except Exception as e:
                    print(f"Error during audio processing: {e}")
                    # Restart the utterance if there was an error
                    try:
                        ps.end_utt()
                    except:
                        pass
                    time.sleep(0.5)  # Add a small delay before restarting
                    ps.start_utt()
                    print("Utterance restarted after error")
        
        except KeyboardInterrupt:
            print("\nStopping wake word detection due to keyboard interrupt...")
        
        finally:
            # Clean up resources
            print("Cleaning up resources...")
            stream.stop_stream()
            stream.close()
            time.sleep(0.2)
            
            try:
                ps.end_utt()
            except:
                pass
            print("Wake word detection stopped successfully.")