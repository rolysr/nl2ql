from generation.metaqa import generate_metaqa_tests
from graph import GraphContractor
from generation.metaqa import generate_metaqa_tests
from metaqakb import MetaQAKnowledgeBase
from model import get_model
import time

import os
from dotenv import load_dotenv
from schema import DBSchemaMaker
from utils import put_results_on_files, update_metrics_tests
import logging

# Create a logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('output.log')

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(handler)

load_dotenv()

NEO4J_DB_URL = os.getenv('NEO4J_DB_URL_CLASSIC')
NEO4J_DB_USER = os.getenv('NEO4J_DB_USER')
NEO4J_DB_PASSWORD = os.getenv('NEO4J_DB_PASSWORD')
KB_PATH = os.getenv('KB_PATH')
TESTS_PATH = os.getenv('TESTS_PATH')

# Init graph contractor instance to interact with Neo4J DB
logger.info("Init graph contractor instance to interact with Neo4J DB")
gc = GraphContractor(NEO4J_DB_URL, NEO4J_DB_USER, NEO4J_DB_PASSWORD)

# Init MetaQA instance for interacting with the knowledge base
logger.info("Init MetaQA instance for interacting with the knowledge base")
metaqa_kb = MetaQAKnowledgeBase(gc)

# Init Schema maker
logger.info("Init schema maker")
schema_maker = DBSchemaMaker()

# Get main data from the created DB
logger.info("Get main data from the created DB")
entities = metaqa_kb.compute_entities()
relations = metaqa_kb.compute_relations(entities)
attributes = metaqa_kb.compute_attributes(entities, relations)

# prompt inputs
query_language = "Cypher"
database_type = "Neo4J"
schema = schema_maker.compute_schema_description(
    entities, relations, attributes)

#Load the datasets
tests_1hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-1hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
logger.info(len(tests_1hop))

tests_2hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-2hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
logger.info(len(tests_2hop))

tests_3hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-3hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
logger.info(len(tests_3hop))

tests = [tests_1hop, tests_2hop, tests_3hop]

# get the model
model_name = "gpt-4"
model_type = "chat"
model = get_model(model_type, model_name)

for i in range(len(tests)):
    logger.info("Analyzing hop{}".format(i+1))
    hop_tests = tests[i]
    # set metrics and evaluation sets
    number_of_tests = len(hop_tests)
    successful_compilations = []
    correct_responses = []
    unsuccessful_compilations = []
    wrong_responses = []
    experiment_total_cost = 0

    # update metrics for each test case
    start_time = time.time()
    experiment_total_cost = update_metrics_tests(model=model, tests=hop_tests, query_language=query_language, database_type=database_type, schema=schema, gc=gc, successful_compilations=successful_compilations, unsuccessful_compilations=unsuccessful_compilations, correct_responses=correct_responses, wrong_responses=wrong_responses, logger=logger)
    end_time = time.time() - start_time
    
    # print results
    put_results_on_files(hop_index=i, model_name=model_name, successful_compilations=successful_compilations, correct_responses=correct_responses, unsuccessful_compilations=unsuccessful_compilations, wrong_responses=wrong_responses, number_of_tests=number_of_tests, experiment_total_cost=experiment_total_cost, end_time=end_time)