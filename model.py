# get a token: https://platform.openai.com/account/api-keys

from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from graph_contractor import GraphContractor

def get_model():
    # template for the model
    template = """You are an agent capable of transforming natural language queries to queries in the query language {query_language}. Your task is: Given a database schema of type {database_type} and a query written in human natural language, return only the code to answer that query in the query language {query_language}

    The database schema is: {schema}

    The natural language query is: {query}

    The code in the query language {query_language} is:
    """

    # init promp template
    prompt = PromptTemplate(template=template, input_variables=["query_language", "database_type", "schema", "query"])

    # init llm
    llm = OpenAI()

    # init chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain