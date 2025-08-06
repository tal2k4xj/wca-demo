# Assisted by watsonx Code Assistant 
import speech_recognition as sr
import sys

def audio_to_text(audio_file):
    # Create a Speech Recognition recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    # Use the Google Cloud Speech to Text API to convert the audio to text
    text = recognizer.recognize_google(audio_data)

    return text

if __name__ == "__main__":
    audio_file = sys.argv[1]
    text = audio_to_text(audio_file)
    print(text)
