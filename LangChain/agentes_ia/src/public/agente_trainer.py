import os
import pandas as pd  # Biblioteca para manipulação de Excel
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


goku_personal_trainer = Agent(
    role="O seu papel é criar treinos, motivação e acompanhamento de exercicios fiscos de Yoga, Calistenia e Karate",
    goal="Fazer as melhores treinos possiveis com foco de no minimo 100 push ups, 100 pull ups, 100 squads e treino de abdomem pesado de 10 minutos. Cada treino tem variação de flexão, barra fixa e agachamento, voce deve dar pelo menos 5 flexoes diferentes por exemplo por treino para ter variação de musculo Esse é o minimo que um guerreiro Saiyajin deve lutar. O treino tem que ter no minimo entre 7 ate 15 minutos de duração, as repticoes vao de 10 a 20 dependendo da dificuldade do exercicio. O tempo de descanso SEMPRE SERA DE 30 segundos para o treino ser dinamico. Treino noob tem no minimo 100 repeticoes no total, Jedi 150 e Sayajin 200 repeticoes podendo ser ate 300",
    backstory="""
    Seu Nome é Goku, personagem do universo de Dragon Ball Z, Você é um lutador profissional, busca energia usando seu CHI com valor mais de 8000 e aprende a dar golpes rapidos e eficazes, seu treino sempre é puxado e seu segredo é treinar,comer e domir e reptir esse ciclo. Voce é conhecido por ser um lutador muito forte que pretende passar adiante seus conhecimentos de treinos e lutas para leigos
""",
    verbose=True,
    allow_delegation=False,
    max_iter=10,
    llm=ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=1.0,
        api_key="AIzaSyCZhKI6vWIAK0GkzXajc-PUjTBEO5zjoeA",
    ),  # Utilizando a API do Gemini
)


task1 = Task(
    description="""
    Baseado em um prompt recebido, criar 3 treinos dos niveis (noob, Jedi e Super Sayajin) e respostas diferentes:
    
    Prompt: {prompt}
    """,
    agent=goku_personal_trainer,
    expected_output="""
        Suas 3 respostas precisam ser em português no formato JSON.

        Exemplo de resposta:

        {exemplos}
    """,
)


crew = Crew(
    agents=[goku_personal_trainer],
    tasks=[task1],
    verbose=2,
)


prompt_user = "Como posso começar a treinar forte 5 dias por dias com foco em hipertrofia com calistenia por 3 meses"

result = crew.kickoff(
    inputs={
        "prompt": prompt_user,
        "exemplos": {
            "messages": '[{"role": "user", "content": "coloque a ficha de treino aqui"}, {"role": "assistant", "content": "coloque a resposta e dicas que o personagem Goku do Dragon Ball z faria aqui"}]}'
        },
    }
)

print("Resultado:", result)

results_json = str(result)
# result["messages"]

print("\n\n\n", results_json[7:])
