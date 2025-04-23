import json 
import requests
from .speech_synthesizer import SpeechSynthesizer

class CommandProcessor:
    def __init__(self, speech_synthesizer: SpeechSynthesizer):
        self.hello = 'hello'
        self.request_url = "http://localhost:3001/command"
        self.speech_synthesizer = speech_synthesizer
    
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
                    self.speech_synthesizer.speak_words_v2(words)
                
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    print(f'words to speak {words}')
                    self.speech_synthesizer.speak_words_v2(words)
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
                    self.speech_synthesizer.speak_words_v2(words)
                
            elif response.status_code == 404:
                if "message" in json_response:
                    words = json_response["message"]
                    self.speech_synthesizer.speak_words_v2(words)
        except:
            # If it's not JSON, print the raw text
            print(response.text)    