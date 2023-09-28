from graph import GraphContractor
from model import get_model
# https://towardsdatascience.com/use-chatgpt-to-query-your-neo4j-database-78680a05ec2

import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_DB_URL = os.getenv('NEO4J_DB_URL')
NEO4J_DB_USER = os.getenv('NEO4J_DB_USER')
NEO4J_DB_PASSWORD = os.getenv('NEO4J_DB_PASSWORD')

# get model
model = get_model()

# init graph contractor instance
gc = GraphContractor(url=NEO4J_DB_URL, name=NEO4J_DB_USER,password=NEO4J_DB_PASSWORD)

# prompt inputs
# query_language = "Cypher"
# database_type = "Neo4J"
# schema = gc.schema_description
# query = "Tell me the name of the people who acted on 'The Matrix' movie"

# # make a query to the model
# formal_query = model.run(query_language=query_language, database_type=database_type, schema=schema, query=query)

# # run the query in the database
# response = gc.make_query(formal_query)

# print(response)