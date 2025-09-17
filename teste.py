from langchain_google_genai import ChatGoogleGenerativeAI

from crewai import Agent, Task, Crew, Process, LLM



import os



os.environ["GOOGLE_API"] = 



llm = LLM(model='gemini/gemini-2.0-flash-lite', verbose=True,

          temperature=0.4, api_key=os.environ["GOOGLE_API"])



pesquisador = Agent(

    role="Pesquisador Acadêmico",

    goal="Investigar e reunir informações relevantes sobre um tópico específico.",

    backstory="Especialista em pesquisa acadêmica com vasta experiência em inovação tecnológica.",

    verbose=True,

    llm=llm

)



escritor = Agent(

    role="Redator Técnico",

    goal="Escrever um texto claro e coerente com base na pesquisa realizada.",

    backstory="Profissional da área de comunicação com foco em TI.",

    verbose=True,

    llm=llm

)



revisor = Agent(

    role="Revisor de textos",

    goal="Corrigir e melhorar o relatório escrito com base na pesquisa realizada, garantindo clareza, coerência e correção gramatical.",

    backstory="Especialista em revisão de textos com atenção aos detalhes e forte domínio da língua portuguesa.",

    verbose=True,

    llm=llm

)



tarefa_pesquisa = Task(

    description="Pesquisar sobre o impacto da inteligência artificial na educação brasileira.",

    expected_output="Um resumo com pelo menos 3 impactos relevantes escrito em português.",

    agent=pesquisador

)



tarefa_redacao = Task(

    description="Com base na pesquisa realizada, rescreva um artigo sobre o tema.",

    expected_output="Artigo técnico com introdução, desenvolvimento e conclusão em português.",

    agent=escritor

)



tarefa_revisao = Task(

    description="Revisar o artigo técnico escrito, corrigindo erros gramaticais e implementar melhorias",

    expected_output="Artigo revisado coeso e bem estruturado em português.",

    agent=revisor

)



crew = Crew(

    agents=[pesquisador, escritor, revisor],

    tasks=[tarefa_pesquisa, tarefa_redacao, tarefa_revisao],

    process=Process.sequential,

    verbose=True

)

resultado = crew.kickoff()

print(resultado)
