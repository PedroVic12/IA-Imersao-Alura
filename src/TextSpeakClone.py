from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs


class TextToSpeakIA:
    def __init__(self):
        self.client = ElevenLabs(
            api_key="36cade3cad57317addce70ccf7d443e7",  # Defaults to ELEVEN_API_KEY
        )

    def speak(self, text: str, id=1):
        if id == 1:
            audio = self.client.generate(
                text=text, voice="Josh", model="eleven_multilingual_v2"
            )
        elif id == 2:
            audio = self.client.generate(
                text=text,
                voice=Voice(
                    voice_id="7u8qsX4HQsSHJ0f8xsQZ",
                    settings=VoiceSettings(
                        stability=0.71,
                        similarity_boost=0.5,
                        style=0.0,
                        use_speaker_boost=True,
                    ),
                ),
            )

        play(audio)

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
    tts = TextToSpeakIA()
    tts.speak("alo alo galera do cauboi alo alo galera do piao")


# main()
