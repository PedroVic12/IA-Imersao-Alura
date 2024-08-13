import os
import pandas as pd  # Biblioteca para manipulação de Excel
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

"""
Explicação dos Componentes Adicionais

Agentes
João Pesquisador: Busca notícias nerds usando DuckDuckGo e Gemini.
Maria Escritora: Cria resumos em markdown sobre os assuntos pesquisados.
Pedro Relatório: Gera relatórios a partir de bases de dados em Excel.

Ferramentas
DuckDuckGoSearchRun: Utilizado para buscas diretas na web.
DuckDuckGoSearchResults: Utilizado para buscar notícias específicas.
GeminiSearch: Utilizado para realizar buscas na web usando a API do Gemini.

Tarefas
task1: Pesquisa de notícias nerds.
task2: Escrita de resumos em markdown.
task3: Geração de relatórios a partir de dados em Excel.

"""


class BaseAgente:
    def __init__(self, nome, papel, objetivo, backstory, tools):
        self.nome = nome
        self.agente = Agent(
            role=papel,
            goal=objetivo,
            backstory=backstory,
            verbose=False,
            allow_delegation=False,
            tools=tools,
            max_iter=10,
            llm=ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=1.0,
                api_key=GEMINI_API_KEY,
            ),  # Utilizando a API do Gemini
        )

    def genaiTexto(self, prompt):
        self.agente.llm.invoke(prompt)


class PesquisaAgente(BaseAgente):
    def __init__(self, nome, backend):
        search_tool = DuckDuckGoSearchResults(backend=backend)
        super().__init__(
            nome,
            papel=f"Agente de Pesquisa {nome}",
            objetivo="Encontrar as melhores notícias nerds",
            backstory="Você é um agente de pesquisa encarregado de buscar as últimas novidades no mundo nerd.",
            tools=[search_tool],
        )


class EscritaAgente(BaseAgente):
    def __init__(self, nome):
        search_tool = DuckDuckGoSearchRun()
        super().__init__(
            nome,
            papel=f"Agente de Escrita {nome}",
            objetivo="Escrever resumos em markdown sobre assuntos nerds",
            backstory="Você é um agente de escrita encarregado de criar resumos atraentes em markdown sobre tópicos nerds.",
            tools=[search_tool],
        )


class RelatorioAgente(BaseAgente):
    def __init__(self, nome):
        search_tool = DuckDuckGoSearchRun()
        super().__init__(
            nome,
            papel=f"Agente de Relatórios {nome}",
            objetivo="Gerar relatórios a partir de bases de dados em Excel",
            backstory="Você é um agente de automação responsável por gerar relatórios detalhados a partir de dados em Excel.",
            tools=[search_tool],
        )


def funcao_posterior(contexto):

    print("Terminei de rodar tudo!")


def funcao_segunda(contexto):
    print("Atividade 1")


class JarvisLLMGenai:
    def __init__(self):
        self.joao_pesquisador = PesquisaAgente("João", "news").agente
        self.maria_escritora = EscritaAgente("Maria").agente
        self.pedro_relatorio = RelatorioAgente("Pedro").agente
        self.tasks = self.criar_tasks()
        self.crew = Crew(
            agents=[self.joao_pesquisador, self.maria_escritora, self.pedro_relatorio],
            tasks=self.tasks,
            verbose=2,
            process=Process.sequential,
        )

    def criar_tasks(self):
        task1 = Task(
            description="Pesquisar notícias nerds. Não esqueça de fornecer a URL dos sites encontrados.",
            agent=self.joao_pesquisador,
            expected_output="""
                Sua resposta precisa ser em português no seguinte formato:

                Notícia 1: A tendência encontrada é que a IA vai se tornar cada...
                Link: https://www.site.com.br

                Notícia 2: Há um crescimento de interesse...
                Link: https://www.site2.com.br
            """,
            callback=funcao_segunda,
        )

        task2 = Task(
            description="Escrever sobre as tendências nerds em 2024.",
            agent=self.maria_escritora,
            expected_output="""
                Sua resposta precisa ser em português no seguinte formato:

                Título: Tendências em 2024 são ...
                Texto: As novidades não param de chegar....
            """,
            callback=funcao_posterior,
        )

        task3 = Task(
            description="Gerar um relatório a partir da base de dados em Excel fornecida.",
            agent=self.pedro_relatorio,
            expected_output="""
                Sua resposta precisa ser em português no seguinte formato:

                Relatório: O relatório mostra que...
            """,
            callback=funcao_posterior,
        )

        return [task1, task2, task3]

    def iniciar(self):
        result = self.crew.kickoff()
        print("\n\nResultado Final", result)

    def gerar_relatorio_excel(self, arquivo_excel):
        # Leitura da base de dados em Excel
        df = pd.read_excel(arquivo_excel)
        # Aqui você pode manipular o dataframe 'df' e gerar relatórios conforme necessário
        relatorio = df.describe()  # Exemplo simples de geração de relatório
        return relatorio


if __name__ == "__main__":
    robo = JarvisLLMGenai()
    robo.iniciar()
    # Exemplo de uso da função de gerar relatório
    # arquivo_excel = "path/to/your/excel/file.xlsx"
    # relatorio = robo.gerar_relatorio_excel(arquivo_excel)
    # print(relatorio)
