# Assisted by watsonx Code Assistant 
#text_to_speech.py
 
import os
import sys
import ibm_watson
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(argv):
    """
    This function takes a text file as input and uses IBM Watson's Text to Speech API to generate an audio file from the text.

    Parameters:
    argv (list): A list of command-line arguments.

    Returns:
    None
    """
    if len(argv) != 2:
        print('Usage: python text_to_speech.py <text_file>')
        sys.exit(1)

    text_file = argv[1]

    with open(text_file, 'r') as f:
        text = f.read()

    authenticator = IAMAuthenticator('API-Key')
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url('URL')

    synthesize_kwargs = {
        'text': text,
        'accept': 'audio/wav',
        'voice': 'en-US_AllisonV3Voice'
    }

    response = text_to_speech.synthesize(**synthesize_kwargs).get_result()

    with open('output.wav', 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    main(sys.argv)
