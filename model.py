# get a token: https://platform.openai.com/account/api-keys

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain import LLMChain


def get_model():
    # template for the model
    template = """
You are an agent capable of transforming natural language queries to queries in the query language {query_language}. Your task is: Given a database schema of type {database_type} and a query written in human natural language, return only the code to answer that query in the query language {query_language}. Remember to respect the sense of the relations.

The database schema is: {schema}

The natural language query is: {query}

The code in the query language {query_language} is:

""".strip()

    # Init prompt template
    prompt = ChatPromptTemplate.from_template(template=template)

    # Init llm
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.3)

    # Init chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain
