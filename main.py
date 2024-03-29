from graph import GraphContractor
from metaqakb import MetaQAKnowledgeBase
from model import get_model
from langchain.callbacks import get_openai_callback
# https://towardsdatascience.com/use-chatgpt-to-query-your-neo4j-database-78680a05ec2

import os
from dotenv import load_dotenv

from schema import DBSchemaMaker

load_dotenv()

# Load environment variables
print("Load environment variables")
NEO4J_DB_URL = os.getenv('NEO4J_DB_URL')
NEO4J_DB_USER = os.getenv('NEO4J_DB_USER')
NEO4J_DB_PASSWORD = os.getenv('NEO4J_DB_PASSWORD')
KB_PATH = os.getenv('KB_PATH')

# Init graph contractor instance to interact with Neo4J DB
print("Init graph contractor instance to interact with Neo4J DB")
gc = GraphContractor(NEO4J_DB_URL, NEO4J_DB_USER, NEO4J_DB_PASSWORD)

# Init MetaQA instance for interacting with the knowledge base
print("Init MetaQA instance for interacting with the knowledge base")
metaqa_kb = MetaQAKnowledgeBase(gc)

# Init Schema maker
print("Init schema maker")
schema_maker = DBSchemaMaker()

# Get main data from the created DB
print("Get main data from the created DB")
entities = metaqa_kb.compute_entities()
relations = metaqa_kb.compute_relations(entities)
attributes = metaqa_kb.compute_attributes(entities, relations)
schema = schema_maker.compute_schema_description(
    entities, relations, attributes)

# Print DB Schema
print("The schema of the created database is:\n" + schema)

model_name = "gpt-3.5-turbo"
model_type = "chat"
model = get_model(model_type, model_name)

# prompt inputs
query_language = "Cypher"
database_type = "Neo4J"
query = "where does Stephen Furst acts in?"

# make a query to the model
with get_openai_callback() as cb:
    formal_query = model.run(query_language=query_language,
                             database_type=database_type, schema=schema, query=query)
    print(formal_query)

# run the query in the database
response = gc.make_query(formal_query)
print(cb.total_cost)
print(response)
