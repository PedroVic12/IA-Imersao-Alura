path = "../voices/"

from gtts import gTTS
from playsound import playsound
import os

# tive que instalar o espeak manualmente no meu sistema linux (manjaro) com:

# sudo yay -S speak e rodar ele localmente

# esse pacote é o mesmo que funciona a lib pyttsx3

# coloquei uma variante para ele funcionar com o playsound


class TextToSpeechEspeak:

    def __init__(self, lang="pt-br", voice="pt-br+f2"):
        self.lang = lang
        self.voice = voice

    def speak(self, text):
        command = f"espeak -v {self.lang}+{self.voice} '{text}'"
        os.system(command)


class TextToSpeech:

    def __init__(self, text, lang="pt-br", rate=150, speed=1):
        self.text = text
        self.lang = lang
        self.rate = rate

    def generate_audio(self, filename=f"{path}/sound.mp3"):
        tts = gTTS(self.text, lang=self.lang)
        tts.save(filename)

    def play_audio(self, filename=f"{path}/sound.mp3"):
        playsound(filename)
