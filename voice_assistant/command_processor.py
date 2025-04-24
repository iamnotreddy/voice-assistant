import json 
import requests
from .speech_synthesizer import SpeechSynthesizer

class CommandProcessor:
    def __init__(self, speech_synthesizer: SpeechSynthesizer):
        self.request_url = "http://localhost:3001/command"
        self.speech_synthesizer = speech_synthesizer
        self.speaker = None  
    
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
                    self.speech_synthesizer.speak_words_v3(words)
                
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    print(f'words to speak {words}')
                    self.speech_synthesizer.speak_words_v3(words)
        except:
            # If it's not JSON, print the raw text
            print(response.text)
    
    def send_request(self, command_text):
        print(f"\nProcessing command: {command_text}")
    
        # Check if it's a speaker command first
        is_speaker_command, response = self.handle_speaker_command(command_text)

        print(f'is it a speaker command tho?{is_speaker_command}')
        
        if is_speaker_command:
            print(f"Handled locally bc its a SPEAKER COMMAND: {response}")
            self.speech_synthesizer.speak_words_v3(response)
            return
        
        # Not a speaker command, proceed with backend request
        print("Sending to backend...")
        
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
                    self.speech_synthesizer.speak_words_v3(words)
                
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    self.speech_synthesizer.speak_words_v3(words)
        except:
            # If it's not JSON, print the raw text
            print(response.text)    

    def set_speaker(self, speaker):
        """Set the speaker controller"""
        self.speaker = speaker
    
    def handle_speaker_command(self, command_text):
        """Handle local speaker commands"""
        if self.speaker is None:
            print('speaker not connected')
            return False, None
            
        command_text = command_text.lower()

        print (f'command text: {command_text}')
        
        if "speaker volume up" in command_text:
            self.speaker.volume_high()
            return True, "Volume increased"
            
        elif "speaker volume down" in command_text:
            self.speaker.volume_low()
            return True, "Volume decreased"
            
        elif "speaker pause" in command_text or "speaker stop" in command_text:
            self.speaker.pause()
            return True, "Music paused"
            
        elif "speaker play" in command_text and "music" in command_text:
            self.speaker.play_playlist()
            return True, "Playing SoulEction 217"
            
        elif "speaker play" in command_text or "speaker resume" in command_text:
            self.speaker.play()
            return True, "Music resumed"
        
        # No speaker command found
        return False, None