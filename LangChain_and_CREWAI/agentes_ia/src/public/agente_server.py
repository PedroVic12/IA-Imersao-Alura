import os
import json
import pandas as pd
from flask import Flask, request, jsonify
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class TreinoGoku:
    def __init__(self):
        self.goku_personal_trainer = Agent(
            role="O seu papel é criar treinos, motivação e acompanhamento de exercícios físicos de Yoga, Calistenia e Karate",
            goal="""Fazer os melhores treinos possíveis com foco de no mínimo 100 push ups, 100 pull ups, 100 squads e treino de abdomem pesado de 10 minutos. 
            Cada treino tem variação de flexão, barra fixa e agachamento, você deve dar pelo menos 5 flexões diferentes por exemplo por treino para ter variação de músculo. 
            Esse é o mínimo que um guerreiro Saiyajin deve lutar. O treino tem que ter no mínimo entre 7 até 15 minutos de duração, as repetições vão de 10 a 20 dependendo da dificuldade do exercício. 
            O tempo de descanso SEMPRE SERÁ DE 30 segundos para o treino ser dinâmico. 
            Treino noob tem no mínimo 100 repetições no total, Jedi 150 e Sayajin 200 repetições podendo ser até 300""",
            backstory="""
            Seu Nome é Goku, personagem do universo de Dragon Ball Z, Você é um lutador profissional, busca energia usando seu CHI com valor mais de 8000 e aprende a dar golpes rápidos e eficazes, 
            seu treino sempre é puxado e seu segredo é treinar, comer e dormir e repetir esse ciclo. Você é conhecido por ser um lutador muito forte que pretende passar adiante seus conhecimentos de treinos e lutas para leigos.
            """,
            verbose=True,
            allow_delegation=False,
            max_iter=10,
            llm=ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.7,
                api_key="AIzaSyCZhKI6vWIAK0GkzXajc-PUjTBEO5zjoeA",
            ),
        )

        self.task1 = Task(
            description="""
            Baseado em um prompt recebido, criar 3 treinos dos níveis (noob, Jedi e Super Sayajin) e respostas diferentes:

            Prompt: {prompt}
            """,
            agent=self.goku_personal_trainer,
            expected_output="""
                Suas 3 respostas precisam ser em português no formato JSON.

                Exemplo de resposta:

                {exemplos}
            """,
        )

        self.crew = Crew(
            agents=[self.goku_personal_trainer],
            tasks=[self.task1],
            verbose=2,
        )

    def gerar_treino(self, prompt):
        result = self.crew.kickoff(
            inputs={
                "prompt": prompt,
                "exemplos": {
                    "messages": '[{"role": "user", "content": "coloque a ficha de treino aqui"}, {"role": "assistant", "content": "coloque a resposta e dicas que o personagem Goku do Dragon Ball z faria aqui"}]}'
                },
            }
        )

        return str(result)[7:]


app = Flask(__name__)


@app.route("/treino", methods=["GET"])
def obter_treino():
    prompt = "Como posso começar a treinar forte 5 dias por dias com foco em hipertrofia com calistenia por 3 meses"

    prompt_user = request.args.get("prompt", "")  # Obter o prompt da query string

    if not prompt:
        return jsonify({"erro": "Prompt ausente."}), 400

    treino_goku = TreinoGoku()
    treino_json = treino_goku.gerar_treino(prompt)

    return jsonify(treino_json), 200


if __name__ == "__main__":
    app.run(debug=True)
