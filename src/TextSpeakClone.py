from elevenlabs import Voice, VoiceSettings, play, stream
from elevenlabs.client import ElevenLabs

import requests
import json


# The 'requests' and 'json' libraries are imported. 
# 'requests' is used to send HTTP requests, while 'json' is used for parsing the JSON data that we receive from the API.
API_KEY = "0c76ddcdc2d1aace04fda8e819f8b1ac"
# docs

def checkVoices():
    # An API key is defined here. You'd normally get this from the service you're accessing. It's a form of authentication.
    url = "https://api.elevenlabs.io/v1/voices"

    headers = {
      "Accept": "application/json",
      "xi-api-key": API_KEY,
      "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    # The JSON response from the API is parsed using the built-in .json() method from the 'requests' library. 
    # This transforms the JSON data into a Python dictionary for further processing.
    data = response.json()

    # A loop is created to iterate over each 'voice' in the 'voices' list from the parsed data. 
    # The 'voices' list consists of dictionaries, each representing a unique voice provided by the API.
    for voice in data['voices']:
      # For each 'voice', the 'name' and 'voice_id' are printed out. 
      # These keys in the voice dictionary contain values that provide information about the specific voice.
      print(f"Vozes Disponiveis: {voice['name']}; id = {voice['voice_id']}")

def textToSpeachEleven(texto):

    # Define constants for the script
    CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
    VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # ID of the voice model to use
    TEXT_TO_SPEAK = texto
    OUTPUT_PATH = "./output.mp3"  # Path to save the output audio file

    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": TEXT_TO_SPEAK,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
    else:
        # Print the error message if the request was not successful
        print(response.text)


#POO

class TextToSpeakIA:
    def __init__(self):
        self.client = ElevenLabs(
            api_key=API_KEY,  # Defaults to ELEVEN_API_KEY
        )

    def speak(self, text: str, id=1):

        if id == 1:
            audio = self.client.generate(
                text=text, voice="George", model="eleven_multilingual_v2"
            )
        elif id == 2:
            audio = self.client.generate(
                text=text,
                voice=Voice(
                    voice_id="7u8qsX4HQsSHJ0f8xsQZ",
                    settings=VoiceSettings(
                        stability=0.77,
                        similarity_boost=0.5,
                        style=0.0,
                        use_speaker_boost=True,
                    ),
                ),
            )
        try:
            # stream(audio)
            play(audio)
            print("audio enviado!")

        except Exception as e:
            print("falha ao executar a voz c3po", e)

    def cloneVoice(self):

        voice = self.client.clone(
            name="PV",
            description="Voz de um jovem programador carioca",  # Optional
            files=[
                "/home/pedrov/Documentos/GitHub/IA-Imersao-Alura/src/c3po-assistentePessoal/audio/PTT-20240510-WA0007.mp3",
            ],
        )

        audio = self.client.generate(
            text="Ola mundo! sou uma voz clonada!!!", voice=voice
        )

        play(audio)


def main():

    checkVoices()
    tts = TextToSpeakIA()
    tts.speak(
        "alo alo galera do cauboi alo alo galera do piao, esta chegando sexta feira sua lindaaaa, vem ni mim"
     )


main()
