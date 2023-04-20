# get a token: https://platform.openai.com/account/api-keys

from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from graph_contractor import GraphContractor

# template for the agent
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

# init graph contractor instance
gc = GraphContractor(url='neo4j+s://5fc1bc71.databases.neo4j.io',password='GUIPdTc9tUjzTw63n47eFbcc6_rFbhjyI_OAg0tbcsU')

# prompt inputs
query_language = "Cypher"
database_type = "Neo4J"
schema = gc.schema_description
query = "Tell me the name of the people who acted on 'The Matrix' movie"

# make a query to the model
formal_query = llm_chain.run(query_language=query_language, database_type=database_type, schema=schema, query=query)

# run the query in the database
gc.make_query(formal_query)

print(response)