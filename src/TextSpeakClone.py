from elevenlabs import Voice, VoiceSettings, play, stream
from elevenlabs.client import ElevenLabs


class TextToSpeakIA:
    def __init__(self):
        self.client = ElevenLabs(
            api_key="0c76ddcdc2d1aace04fda8e819f8b1ac",  # Defaults to ELEVEN_API_KEY
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
    tts = TextToSpeakIA()
    # tts.speak(
    #    "alo alo galera do cauboi alo alo galera do piao, esta chegando sexta feira sua lindaaaa, vem ni mim"
    # )


main()
