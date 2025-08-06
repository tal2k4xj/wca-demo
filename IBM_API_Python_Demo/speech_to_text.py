 # Assisted by watsonx Code Assistant 
  
 
import os
import ibm_watson
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys

# Set up the Watson Speech-to-Text service
authenticator = IAMAuthenticator('API-Key')
speech_to_text = ibm_watson.SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('URL')

# Define the audio file to transcribe
audio_file = sys.argv[1]

# Transcribe the audio file
with open(audio_file, 'rb') as audio_file:
    transcription = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav'
    ).get_result()

# Save the transcription in a text file
with open('transcription.txt', 'w') as f:
    f.write(transcription['results'][0]['alternatives'][0]['transcript'])
