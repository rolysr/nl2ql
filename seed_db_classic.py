from graph import GraphContractor
from metaqakb import MetaQAKnowledgeBase
from schema import DBSchemaMaker
from seeder import DBSeeder

import os
from dotenv import load_dotenv

load_dotenv()

# Ensure to first run command: docker run --name testneo4j -p7474:7474 -p7687:7687 -d -v $HOME/neo4j/data:/data -v $HOME/neo4j/logs:/logs -e NEO4J_AUTH=neo4j/testpassword docker.uclv.cu/neo4j
# That command will start a Docker Neo4J DB management system.

# Load environment variables
print("Load environment variables")
NEO4J_DB_URL = os.getenv('NEO4J_DB_URL_CLASSIC')
NEO4J_DB_USER = os.getenv('NEO4J_DB_USER')
NEO4J_DB_PASSWORD = os.getenv('NEO4J_DB_PASSWORD')
KB_PATH = os.getenv('KB_PATH')

# Init graph contractor instance to interact with Neo4J DB
print("Init graph contractor instance to interact with Neo4J DB")
gc = GraphContractor(NEO4J_DB_URL, NEO4J_DB_USER, NEO4J_DB_PASSWORD)

# Init MetaQA instance for interacting with the knowledge base
print("Init MetaQA instance for interacting with the knowledge base")
metaqa_kb = MetaQAKnowledgeBase(gc)

# Init seeder instance for filling the DB with actual data
print("Init seeder instance for filling the DB with actual data")
seeder = DBSeeder(metaqa_kb, KB_PATH)

# Seed db
print("Seeding db...")
seeder.seed_db(is_classic_metaqa=True)

# Init Schema maker
print("Init schema maker")
schema_maker = DBSchemaMaker()

# Get main data from the created DB
print("Get main data from the created DB")
entities = metaqa_kb.compute_entities()
relations = metaqa_kb.compute_relations(entities)
attributes = metaqa_kb.compute_attributes(entities, relations)

# Print DB Schema
print("The schema of the created database is:\n" +
      schema_maker.compute_schema_description(entities, relations, attributes))
