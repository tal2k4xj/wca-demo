# Assisted by watsonx Code Assistant 
import sys
import subprocess

def routing(user_input):
    """
    This function routes user input to the appropriate processing function based on the file type.

    Parameters:
    user_input (str): The user input file path.

    Returns:
    None
    """
    if user_input.endswith('.wav'):
        subprocess.call(['python', 'speech_to_text.py', user_input])
    elif user_input.endswith('.txt'):
        subprocess.call(['python', 'text_to_speech.py', user_input])
    else:
        print('Invalid file type. Please provide a .wav or .txt file.')

if __name__ == "__main__":
    user_input = sys.argv[1]
    routing(user_input)
