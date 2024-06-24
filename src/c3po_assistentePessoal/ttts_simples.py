path = "../voices/"

from gtts import gTTS
from playsound import playsound
import os
import pyttsx3

# tive que instalar o espeak manualmente no meu sistema linux (manjaro) com:

# sudo yay -S speak e rodar ele localmente

# esse pacote é o mesmo que funciona a lib pyttsx3

# coloquei uma variante para ele funcionar com o playsound


class TextToSpeechEspeak:

    def __init__(self, lang="pt-br", voice="pt-br+f2"):
        self.lang = lang
        self.voice = voice
        self.engine = pyttsx3.init("espeak")  # Usando espeak para Linux
        self.engine.setProperty("voice", self.engine.getProperty("voices")[1].id)
        self.listar_vozes()

    def falar(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def listar_vozes(self):
        vozes = self.engine.getProperty("voices")
        for voz in vozes:
            # print("Id: ", voz.id)
            # print("Nome: ", voz.name)
            # print("Lang: ", voz.languages)

            # se for pt-br
            if "pt-br" in voz.languages:
                print("Usando voz pt-br")
                self.engine.setProperty("voice", voz.id)
                print("Voz em portugues configurada")
                break

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
