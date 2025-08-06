# Assisted by watsonx Code Assistant 
import os
import sys
from google.cloud import texttospeech
from google.oauth2 import service_account

# Set up the Google Cloud Text-to-Speech API client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
client = texttospeech.TextToSpeechClient()

# Define the text to be spoken
text = open(sys.argv[1], 'r').read()

# Define the voice and audio file format
voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Wavenet-A',
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    sample_rate_hertz=22050
)

# Synthesize the text to speech
response = client.synthesize_speech(input=texttospeech.SynthesisInput(text=text),
                                    voice=voice,
                                    audio_config=audio_config)

# Write the audio file
with open('output.wav', 'wb') as out:
    out.write(response.audio_content)

print('Audio file output.wav generated successfully.')
