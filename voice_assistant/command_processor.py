import json 
import requests
from .speech_synthesizer import SpeechSynthesizer

class CommandProcessor:
    def __init__(self, speech_synthesizer: SpeechSynthesizer):
        self.request_url = "http://localhost:3001/command"
        self.speech_synthesizer = speech_synthesizer
        self.speaker = None  
    
    def set_speaker(self, speaker):
        """Set the speaker controller"""
        self.speaker = speaker

    def process_command(self, command_text, check_speaker_commands=True):
        """
        Shared helper function to process commands
        Args:
            command_text: The text command to process
            check_speaker_commands: Whether to check for speaker commands first
        Returns:
            tuple of (response object, json response data)
        """
        print(f"\nProcessing command: {command_text}")
        
        # Check if it's a speaker command if requested
        if check_speaker_commands:
            is_speaker_command, response = self.handle_speaker_command(command_text)
            
            print(f'is it a speaker command? {is_speaker_command}')
            
            if is_speaker_command:
                print(f"Handled locally as SPEAKER COMMAND: {response}")
                self.speech_synthesizer.speak_words(response)
                return None, {"locally_handled": True, "response": response}
        
        # Not a speaker command or check was skipped, proceed with backend request
        print(f"Sending to backend: {command_text}")
        
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
            
            words = None
            if response.status_code == 200:
                if "response_type" in json_response:
                    if json_response["response_type"] == "weather":
                        words = json_response["answer"]["summary"]
                    elif json_response["response_type"] == "ai":
                        words = json_response["answer"]
                    
                    print(f'words to speak: {words}')
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    print(f'words to speak: {words}')
            
            if words:
                self.speech_synthesizer.speak_words(words)
                
            return response, json_response
        except:
            # If it's not JSON, print the raw text
            print(response.text)
            return response, None
    
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