def ttsSimples():
    from TTS.api import TTS

    # Inicialize o TTS com um modelo pré-treinado
    tts = TTS(
        model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False
    )

    # Texto a ser convertido para voz
    text = "Hello, this is a text to speech test."

    # Converte o texto em um arquivo de áudio
    tts.tts_to_file(text=text, file_path="output.wav")


from google.cloud import texttospeech

# Inicializa o cliente TTS
client = texttospeech.TextToSpeechClient(
    # Credenciais de autenticação
    credentials=credentials
)

# Configura o texto e a voz
synthesis_input = texttospeech.SynthesisInput(
    text="Olá, este é um teste de conversão de texto para fala."
)

voice = texttospeech.VoiceSelectionParams(
    language_code="pt-BR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Converte texto em fala
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Salva o áudio em um arquivo
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
