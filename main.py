from graph_contractor import GraphContractor
from model import get_model
# https://towardsdatascience.com/use-chatgpt-to-query-your-neo4j-database-78680a05ec2

# get model
model = get_model()

# init graph contractor instance
gc = GraphContractor(url='neo4j+s://5fc1bc71.databases.neo4j.io',password='GUIPdTc9tUjzTw63n47eFbcc6_rFbhjyI_OAg0tbcsU')

# prompt inputs
query_language = "Cypher"
database_type = "Neo4J"
schema = gc.schema_description
query = "Tell me the name of the people who acted on 'The Matrix' movie"

# make a query to the model
formal_query = model.run(query_language=query_language, database_type=database_type, schema=schema, query=query)

# run the query in the database
response = gc.make_query(formal_query)

print(response)