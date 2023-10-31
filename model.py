# get a token: https://platform.openai.com/account/api-keys

from langchain.prompts import PromptTemplate
from langchain import LLMChain
from langchain import OpenAI


def get_model():
    # template for the model
    template = """
You are an agent capable of transforming natural language queries to queries in the query language {query_language}. Your task is: Given a database schema of type {database_type} and a query written in human natural language, return only the code to answer that query in the query language {query_language} and respect the relations directions.

The database schema is: {schema}

The natural language query is: {query}

The code in the query language {query_language} is:

""".strip()

    # Init prompt template
    prompt = PromptTemplate(template=template, input_variables=["query_language", "database_type", "schema", "query"])

    # Init llm
    llm = OpenAI(temperature=0.7)

    # Init chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain
