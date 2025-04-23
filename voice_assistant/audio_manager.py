import time
import os 
import wave
import sys
import pyaudio

class AudioManager:
    def __init__(self, audio: pyaudio.PyAudio, record_seconds, temp_file):
        self.record_seconds = record_seconds
        self.temp_file = temp_file
        self.audio = audio
        
        # Audio parameters
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000

    def record_audio(self):
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

    def play_audio_segment(self, start_ms=0, end_ms=None):
        """
        Play a specific segment of a WAV file with millisecond precision
        
        Args:
            file_path: Path to the WAV file
            start_ms: Start time in milliseconds (default: 0 = beginning of file)
            end_ms: End time in milliseconds (default: None = play to the end)
        """
        
        # Open the WAV file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(script_dir, 'audio', 'open-signal.wav')
        wf = wave.open(audio_path, 'rb')
        
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
        
        # Open a stream
        stream = self.audio.open(format=self.audio.get_format_from_width(sample_width),
                        channels=channels,
                        rate=sample_rate,
                        output=True)
        
        # Read exactly the number of frames needed
        data = wf.readframes(frames_to_play)
        stream.write(data)
        
        # Clean up
        stream.stop_stream()
        stream.close()