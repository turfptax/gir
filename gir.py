import openai
import os

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io



# Read the API key from UnderThePillow.txt
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'UnderThePillow.txt'), 'r') as f:
    api_key = f.read().strip()

# Set the API key
openai.api_key = api_key

from openai.error import RateLimitError
import time

import tempfile

def text_to_speech(text, pitch_shift=0):
    # Create an audio file using gTTS
    tts = gTTS(text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        tts.save(temp_audio_file.name)
        temp_audio_file.seek(0)
        
        # Load the audio file using Pydub
        audio = AudioSegment.from_file(temp_audio_file.name, format="mp3")

        # Apply pitch shift (if specified)
        if pitch_shift != 0:
            audio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate * (2.0 ** pitch_shift))})
            
        # Add any additional audio effects here

        # Play the audio
        play(audio)

        # Clean up the temporary file
        os.unlink(temp_audio_file.name)

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are the character Gir from Invader Zim. You will use exclamation marks and give silly answers to all questions in a light-hearted Gir way."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].message['content'].strip()

    except RateLimitError as e:
        retry_after = int(e.headers.get('Retry-After', 60))
        print(f"You have exceeded the API rate limit. Waiting for {retry_after} seconds before retrying...")
        time.sleep(retry_after)
        return chat_with_gpt(prompt)

print("Welcome to the GIR interface!")
print("Type 'quit' to exit the program.\n")


# Set the initial command
#initial_prompt = "I want you to respond to me as if you are the character 'gir' from invader zim during our entire conversation, I want you to use exclamation marks and give silly answers to all of my questions in a light hearted gir way"
#print(f"Initial command: {initial_prompt}")
#chat_with_gpt(initial_prompt)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    prompt = f"User: {user_input}\nAI:"
    response = chat_with_gpt(prompt)
    print(f"GIR: {response}\n")
    # Play the response using text_to_speech function
    text_to_speech(response, pitch_shift=0)  # Change the pitch_shift value to modify the pitch

