# Assisted by watsonx Code Assistant 
#routing.py
 
import os
import sys

def main():
    """
    Main function for routing user input to appropriate processing functions.

    Parameters:
    user_input (str): User input file name.

    Returns:
    None
    """
    user_input = input("Enter the file name: ")
    file_extension = user_input.split('.')[-1]

    if file_extension == 'wav':
        os.system(f"python speech_to_text.py {user_input}")
    elif file_extension == 'txt':
        os.system(f"python text_to_speech.py {user_input}")
    else:
        print("Invalid file type. Please enter a .wav or .txt file.")

if __name__ == "__main__":
    main()
