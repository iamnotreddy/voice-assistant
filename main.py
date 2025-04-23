from voice_assistant import VoiceAssistant

if __name__ == "__main__":
    # Run the application
    assistant = VoiceAssistant(record_seconds=3)
    assistant.run()