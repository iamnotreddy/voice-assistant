import os
import time
import pyaudio
import wave
import speech_recognition as sr
import sys
import wave
import pyttsx3 
from pocketsphinx import get_model_path, Pocketsphinx
import shutil
import requests
import json
from gtts import gTTS
import os

class MacVoiceRecorder:
    """
    A simple voice recorder for macOS that records audio for a fixed duration
    and converts it to text using speech recognition.
    """
    
    def __init__(self, record_seconds=5):
        """
        Initialize the voice recorder.
        
        Args:
            record_seconds (int): Number of seconds to record
        """
        # Audio parameters
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.record_seconds = record_seconds
        
        # File parameters
        self.temp_file = "temp_recording.wav"
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()

        # base url
        self.request_url = "http://localhost:3001/command"
        
    def record_audio(self, test=False):
        """Record audio for a fixed duration and save to a temporary file."""
        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
        # Open stream
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print("=" * 50)
        print("🎤 RECORDING STARTED - SPEAK NOW 🎤")
        print(f"Recording for {self.record_seconds} seconds...")
        print("=" * 50)
        
        # Record data
        frames = []
        start_time = time.time()
        
        # Show a simple counter/progress bar
        for i in range(self.record_seconds):
            # Calculate seconds elapsed and remaining
            elapsed = time.time() - start_time
            remaining = max(0, self.record_seconds - elapsed)
            
            # Collect data for this second
            second_frames = []
            second_start = time.time()
            while time.time() - second_start < 1.0:
                data = stream.read(self.chunk)
                second_frames.append(data)
            
            frames.extend(second_frames)
            
            # Update progress indication (overwrite the line)
            bars = "█" * (i + 1) + "▒" * (self.record_seconds - i - 1)
            seconds_text = f"{i+1}/{self.record_seconds}s"
            print(f"\r{bars} {seconds_text}", end="")
            sys.stdout.flush()
        
        print("\n\nFinished recording!")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        # Save the audio file
        wf = wave.open(self.temp_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    
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
    
    def play_opening_signal(self):
        wf = wave.open('open-signal.wav', 'rb')

        # Get audio parameters
        sample_rate = wf.getframerate()
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()

        # Calculate frames for exact millisecond duration
        duration_ms = 900  # Can be any number of milliseconds
        frames_to_play = int((sample_rate * duration_ms) / 1000)

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open a stream
        stream = p.open(format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=sample_rate,
            output=True)
        
        data = wf.readframes(frames_to_play)

        stream.write(data)
        
        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    def play_audio_segment(self, start_ms=0, end_ms=None):
        """
        Play a specific segment of a WAV file with millisecond precision
        
        Args:
            file_path: Path to the WAV file
            start_ms: Start time in milliseconds (default: 0 = beginning of file)
            end_ms: End time in milliseconds (default: None = play to the end)
        """

        print('inside method')
        
        # Open the WAV file
        wf = wave.open('open-signal.wav', 'rb')
        
        # Get audio parameters
        sample_rate = wf.getframerate()
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        

        # Calculate start frame
        start_frame = int((sample_rate * start_ms) / 1000)
        
        # Calculate number of frames to play
        if end_ms is not None:
            # If end time is specified, calculate duration
            duration_ms = end_ms - start_ms
            frames_to_play = int((sample_rate * duration_ms) / 1000)
        else:
            # If no end time, play to the end of file
            frames_to_play = wf.getnframes() - start_frame
        
        # Skip to the start position
        wf.setpos(start_frame)
        
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # Open a stream
        stream = p.open(format=p.get_format_from_width(sample_width),
                        channels=channels,
                        rate=sample_rate,
                        output=True)
        
        # Read exactly the number of frames needed
        data = wf.readframes(frames_to_play)
        stream.write(data)
        
        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def cleanup(self):
        """Clean up resources."""
        self.audio.terminate()
        
        # Remove temporary file if it exists
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

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
   
    def send_mock_request(self, command_text):
        print(f"\nmaking mock request for command {command_text}")

        headers = {"Content-Type": "application/json"}
        data = {"command": command_text}
        json_data = json.dumps(data)  
                            
        response = requests.post(self.request_url, data=json_data, headers=headers)

        print("\n===== RESPONSE STATUS =====")
        print(response.status_code)
        
        print("\n===== RESPONSE CONTENT =====")
        try:
            # Try to parse as JSON and print with nice formatting
            json_response = response.json()
            print(json.dumps(json_response, indent=4))

            if response.status_code == 200:
                if "summary" in json_response:
                    words = json_response["summary"]
                    print(f'words to speak {words}')
                    self.speak_words_v2(words)
                
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    print(f'words to speak {words}')
                    self.speak_words_v2(words)
        except:
            # If it's not JSON, print the raw text
            print(response.text)
    
    def send_request(self, command_text):
        print(f"\nmaking real request for command {command_text}")
        
        headers = {"Content-Type": "application/json"}
        data = {"command": command_text}
        json_data = json.dumps(data)  
                            
        response = requests.post(self.request_url, data=json_data, headers=headers)

        try:
            # Try to parse as JSON and print with nice formatting
            json_response = response.json()
            print(json.dumps(json_response, indent=4))

            if response.status_code == 200:
                if "summary" in json_response:
                    words = json_response["summary"]
                    self.speak_words_v2(words)
                
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    self.speak_words_v2(words)
        except:
            # If it's not JSON, print the raw text
            print(response.text)    

    def start_wake_word_detection(self):

        print("\n=== Wake Word Detection Mode ===")
        print("Listening for 'Hey Benito'...")
        print("Press Ctrl+C to stop")
        print("-" * 30)

        # Use the exact paths found in your environment
        hmm_path = '/Users/raveen/repos/voice-client/venv/lib/python3.13/site-packages/pocketsphinx/model/en-us/en-us'
        dict_path = '/Users/raveen/repos/voice-client/venv/lib/python3.13/site-packages/pocketsphinx/model/en-us/cmudict-en-us.dict'
        
        # Create a custom dictionary with our wake word
        custom_dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benito_dict.dict")
        
        # Copy the original dictionary and add our words
        shutil.copy2(dict_path, custom_dict_path)
        
        # Check if the words already exist in the dictionary
        with open(custom_dict_path, 'r') as f:
            dict_content = f.read()
        
        # Add the wake word entries if they don't exist
        with open(custom_dict_path, 'a') as f:
            if 'HEY' not in dict_content:
                f.write('\nHEY HH EY\n')
            if 'BENITO' not in dict_content:
                f.write('\nBENITO B EH N IY T OW\n')
        
        # Create keyword file
        kws_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hey_benito.txt")
        with open(kws_path, 'w') as f:
            f.write("HEY BENITO /1e-15/\n")
        
        print(f"Using keyword file: {kws_path}")
        print(f"Using hmm path: {hmm_path}")
        print(f"Using custom dict path: {custom_dict_path}")
        
        # Initialize PocketSphinx with the correct paths
        try:
            ps = Pocketsphinx(hmm=hmm_path, dict=custom_dict_path, kws=kws_path)
            print("PocketSphinx initialized successfully!")
        except Exception as e:
            print(f"Error initializing PocketSphinx: {e}")
            return

        # Set up audio input
        p = pyaudio.PyAudio()
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
                            
                            # Play audio feedback for wake word detection
                            self.play_audio_segment(0, 995)
                            
                            # Record audio for command
                            print("Listening for command for three seconds...")
                            self.record_audio()
                            
                            # Play audio feedback for end of recording
                            self.play_audio_segment(2000, 2995)
                            
                            # Recognize speech
                            command_text = self.recognize_speech()
                            
                            # Play audio feedback that recording has been processed
                            self.play_audio_segment(3095, 4095)
                            
                            print('processed command: ', command_text)

                            # make request
                            self.send_request(command_text)
                            
                            print("\nListening for 'Hey Benito' again...")
                            
                            # Start a new utterance for the next detection
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
            p.terminate()
            try:
                ps.end_utt()
            except:
                pass
            print("Wake word detection stopped successfully.")
              
    def run(self):
        """Run the main application loop."""
        try:
            while True:
                # Clear the terminal
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print("\n=== Simple Voice Recorder ===")
                print("Enter 's' to start recording (5 seconds)")
                print("Enter 't' for testing without microphone input")
                print("Enter 'w' for testing wake word listening mode")
                print("Enter 'r' to make mock request")
                print("Enter 'q' to quit")
                print("-" * 30)
                
                # Use input() instead of keyboard library
                choice = input("> ").strip().lower()
                
                if choice == 's':
                    # audio feedback to start recording
                    self.play_audio_segment(0, 995)
                    
                    # # Record audio
                    self.record_audio()
                    
                    # audio feedback to end recording
                    self.play_audio_segment(2000, 2995)
                    
                    # Recognize speech
                    text = self.recognize_speech()

                    # audio feedback that recording has been processed
                    self.play_audio_segment(3095, 4095)

                    # re-play the prompt
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                                        
                    # Display results
                    print("\n" + "=" * 50)
                    print("RECOGNIZED TEXT:")
                    print("-" * 50)
                    print(text)
                    print("=" * 50)
                    
                    # input("\nPress Enter to continue...")
                
                elif choice == 'w':
                    self.start_wake_word_detection()

                elif choice == 't':
                    print("\nTesting without microphone input...")
                    print("Simulating speech recognition...")
                    time.sleep(2)
                    print("No actual recording will be done in this mode.")
                    input("\nPress Enter to continue...")
                
                elif choice == 'r':
                    print("Enter mock command")
                    
                    user_command_prompt = input()

                    self.send_mock_request(user_command_prompt)

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


if __name__ == "__main__":
    # Run the application
    recorder = MacVoiceRecorder(record_seconds=3)
    recorder.run()