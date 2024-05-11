import google.generativeai as genai
import PIL
import os

GEMINI_KEY = "AIzaSyDVufkW23RIvdiTrUY3_ql67cnyVTMMIq8"
genai.configure(api_key=GEMINI_KEY)


from IPython.display import display
from IPython.display import Markdown
import textwrap
import pandas as pd
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import os

GEMINI_KEY = "AIzaSyDVufkW23RIvdiTrUY3_ql67cnyVTMMIq8"
genai.configure(api_key=GEMINI_KEY)


class C3PoAssisstente:
    def __init__(self):
        pass

    def multiply(self, a: float, b: float):
        """returns a * b."""
        return a * b

    def modeloTextoGenerativo(self, txt):
        model_TextGenerator = genai.GenerativeModel("gemini-pro")

        response = model_TextGenerator.generate_content(txt)
        return response.text

    def modeloVisaoComputacional(self, img_path, prompt_cliente):
        model_VisaoComputacional = genai.GenerativeModel("gemini-pro-vision")

        imagem = PIL.Image.open(img_path)

        response = model_VisaoComputacional.generate_content(imagem)
        print("IMG= ", response.text)
        response_text = model_VisaoComputacional.generate_content(
            [prompt_cliente, imagem]
        )
        result = response_text.resolve()
        return response.text

    def chat(self):
        model = genai.GenerativeModel("gemini-pro", tools=[self.multiply])

        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(
            "se eu tenho um robo de 400 reais e quero vender para 5 clientes quanto de lucro vou ter?"
        )
        print(response.text)


def main():
    assistente = C3PoAssisstente()
    response = assistente.modeloTextoGenerativo("Ola bom dia, como esta?, ")
    print(response)


main()


class ChatbotAssistente(C3PoAssisstente):
    def __init__(self):
        super().__init__()
        try:
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty("voices")
            self.engine.setProperty("rate", 170)
            self.r = sr.Recognizer()
            self.mic = sr.Microphone()
        except:
            print("c3po sem som")

    def configurar_voz(self, voz_index=1):
        self.engine.setProperty("voice", self.voices[voz_index].id)

    def to_markdown(self, text):
        text = text.replace("•", "  *")
        return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))

    def receber_comando(self, modo):
        try:

            if modo == "1":
                return self.ouvir_comando_voz()
            elif modo == "2":
                return input("Digite seu comando: ")
            else:
                print("Escolha inválida. Por favor, tente novamente.")
                return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def ouvir_comando_voz(self):
        with self.mic as fonte:
            self.r.adjust_for_ambient_noise(fonte)
            audio = self.r.listen(fonte)
            try:
                texto = self.r.recognize_google(audio, language="pt-BR")
                return texto
            except sr.UnknownValueError:
                return "Não entendi o que você disse."
            except sr.RequestError as e:
                return f"Erro ao solicitar resultados; {e}"

    def falar_resposta(self, resposta):
        self.engine.say(resposta)
        self.engine.runAndWait()

    def iniciar_chatbot(self):
        bem_vindo = "# Bem Vindo, eu sou o C3po seu assistente pessoal #"
        print("\n" + bem_vindo + "\n###   Digite 'desligar' para encerrar    ###\n")

        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        print("Digite '1' para comando de VOZ ou '2' para comando em TEXTO:")
        modo = input("Escolha o modo de entrada (1 ou 2): ")
        while True:
            texto = self.receber_comando(modo)

            if texto is None:
                continue
            if texto.lower() == "desligar":
                break

            response = chat.send_message(texto)
            print("Gemini:", response.text, "\n")
            # self.falar_resposta(response.text)

        print("Encerrando Chat")


def main():
    assistente = C3PoAssisstente()
    chat = ChatbotAssistente()
    chat.iniciar_chatbot()


main()
