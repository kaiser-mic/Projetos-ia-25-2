from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process, LLM
from api_key import *

import os

os.environ["GOOGLE_API"] = api_key

llm = LLM(model='gemini/gemini-2.0-flash-lite', verbose=True, temperatura=0.4,
           api_key = os.environ["GOOGLE_API"])

pesquisador = Agent(role="pesquisador academico", goal="investigar profundamente um tema proposto", backstory="especialista em pesquisas educacionais e inovacao tecnologica"
                    , verbose=True, llm= llm)

escritor = Agent(role="redator tecnico", goal="escrever um texto claro e coerente com base na pesquisa realizada", backstory="profissional da area da comunicacao com foco na area de ti",
                 verbose=True, llm= llm)

revisor = Agent(role=" revisor de textos", goal="corrigir erros e melhorar a clareza e a fluide do conteudo", backstory="experiente em revisao e padronizacao de textos",
                verbose=True, llm= llm)

tarefa_pesquisa = Task(description="Pesquisar os principais impactos da inteligencia artificial na educacoa brasileira", expected_output="um resumo com pelo menos 3 impactos relevantes escrito em pt-br",
                       agent = pesquisador)

tarefa_redacao = Task(description="Com base na pesquisa anterior excreva um artigo sobre o tema", expected_output="um artigo tecnico com intruducao, desenvolvimento e conclusao em pt-br",
                       agent=escritor)

tarefa_revisao = Task(description="revisar o artigo, corrigir erros e implementar melhorias", expected_output="artigo revisado, coeso e bem estruturado em pt-br", agent=revisor)

crew = Crew(agents=[pesquisador, escritor, revisor],
        tasks=[tarefa_pesquisa, tarefa_redacao, tarefa_revisao],
        process= Process.sequential,
        verbose=True)

resultado = crew.kickoff()

print(resultado)