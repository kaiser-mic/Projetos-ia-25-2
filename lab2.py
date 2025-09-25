from langchain_google_genai import ChatGoogleGenerativeAI

from crewai import Agent, Task, Crew, Process, LLM
from api_key import *



import os



os.environ["GOOGLE_API"] = api_key



llm = LLM(model='gemini/gemini-2.0-flash-lite', verbose=True,

          temperature=0.4, api_key=os.environ["GOOGLE_API"])


#agentes que vao cumprir os papeis que serao necessarios nas tarefas abaixo
vitima = Agent(

    role="vitima",

    goal="Denunciar um crime sofrido por ela ou outra pessoa.",

    backstory="Especializada em comunicao com boa oratoria.",

    verbose=True,

    llm=llm

)



policial = Agent(

    role="Policial",

    goal="Escrever um texto claro e coerente com base na denuncia realizada.",

    backstory="Profissional da área de comunicação com foco em crimes.",

    verbose=True,

    llm=llm

)



escrivao = Agent(

    role="escrivao da policia",

    goal="formalizar a denuncia e melhorar o relatório escrito com base na denuncia realizada, garantindo clareza, coerência e correção gramatical.",

    backstory="Especialista em revisão de textos e especialista em crimes com atenção aos detalhes e forte domínio da língua portuguesa.",

    verbose=True,

    llm=llm

)


#tasks que usarao os agentes para cumprir seus objetivos
tarefa_denuncia = Task(

    description="denunciar um homicidio sofrido pelo tio.",

    expected_output="UDescricao do que aconteceu com a vitima.",

    agent=vitima

)



tarefa_redacao = Task(

    description="Com base na denuncia realizada, escreva um resumo sobre o tema.",

    expected_output="resumo da denuncia indicando todos fatos ocorridos e informacoes necessarias em português.",

    agent=policial

)



tarefa_escrivao = Task(

    description="formalizar o resumo da denuncia escrito, corrigindo erros gramaticais e implementar melhorias",

    expected_output="denuncia formalizada, coeso e bem estruturado em português.",

    agent=escrivao

)


#instancia do sistema multiagente utilizando crewAI
crew = Crew(

    agents=[vitima, policial, escrivao],

    tasks=[tarefa_denuncia, tarefa_redacao, tarefa_escrivao],

    process=Process.sequential,

    verbose=True

)
#lancamento do sistema multiagente
resultado = crew.kickoff()

print(resultado)
