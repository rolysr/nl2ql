# get a token: https://platform.openai.com/account/api-keys

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain

def get_model():
    # template for the model
    template = """
You are an agent capable of transforming natural language queries to queries in the query language {query_language}. Your task is: Given a database schema of type {database_type} and a query written in human natural language, return only the code to answer that query in the query language {query_language}. Remember to respect the sense of the relations.

The database schema is: {schema}

The natural language query is: {query}

The code in the query language {query_language} is:

""".strip()

    # init promp template
    prompt = PromptTemplate(template=template, input_variables=["query_language", "database_type", "schema", "query"])

    # init llm
    llm = ChatOpenAI(temperature=0.3, model='gpt-3.5-turbo')

    # init chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain