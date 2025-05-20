# Python Voice Assistant
I built a voice assistant built for a Raspberry Pi with offline wake-word detection, speech recognition, and text-to-speech

## Features
- **Offline Operation** - wake word detection with PocketSphinx, speech recognition with Vosk, and text-to-speech with Piper TTS 
- **Smart Speaker Integration** - control a Denon home speakers via telnet commands (play/pause, volume control, media selection)
- **Weather Updates** - local forecasts through OpenWeather API integration
- **AI Assistance** - send complex queries to Cohere's language models through a simple Flask backend

## Motivation
I wanted the convenience of a voice assistant without the privacy concerns of an always-on microphone sending data to the cloud. I also find Alexa to be lacking with certain types of queries, so wanted an integration with a ChatGPT-like service. 
Finding out I could control my 10 year old Denon speaker via telnet was an added bonus 😎

## Architecture
The system consists of two main components:

1. **Core Voice Assistant** (this repo)
   - Handles wake word detection, speech processing, and speaker control
   - Optimized specifically for Raspberry Pi 
   - Manages all audio I/O and device interactions

2. **Flask Backend** (separate [repo](https://github.com/iamnotreddy/voice-backend))
   - Processes general AI queries via the Cohere API
   - Fetches and parses weather data into 
     
## Setup

```bash
# Clone the repository
git clone https://github.com/iamnotreddy/voice-assistant.git
cd voice-assistant

# Install dependencies 
pip install -r requirements-rpi.txt

# Download piper voice models and config
https://github.com/rhasspy/piper/blob/master/VOICES.md

# Download offline vosk model
https://alphacephei.com/vosk/models

# Run the assistant
python main.py
press "w" to trigger wake word mode
```

## Notes
- This project runs entirely on your local network with the exception of API calls for weather data and complex AI queries. No audio is stored or sent to the cloud for processing unless you specifically ask a question that requires the Cohere API.
- The system is designed specifically for a Raspberry Pi. If you're developing locally on OS X, keep in mind that piper-tts was developed specifically for the Pi's ARM architecture and doesn't support Apple Silicon. You'll need to create a wheel for the package - this [thread](https://github.com/rhasspy/piper/issues/217) is somewhat helpful 
