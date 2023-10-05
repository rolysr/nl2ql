from graph import GraphContractor
from generation.metaqa import generate_metaqa_tests
from metaqakb import MetaQAKnowledgeBase
from model import get_model
import pandas as pd

import os
from dotenv import load_dotenv
from query_utils import QueryUtils

from schema import DBSchemaMaker

load_dotenv()

NEO4J_DB_URL = os.getenv('NEO4J_DB_URL')
NEO4J_DB_USER = os.getenv('NEO4J_DB_USER')
NEO4J_DB_PASSWORD = os.getenv('NEO4J_DB_PASSWORD')
KB_PATH = os.getenv('KB_PATH')
TESTS_PATH = os.getenv('TESTS_PATH')

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

# prompt inputs
query_language = "Cypher"
database_type = "Neo4J"
schema = schema_maker.compute_schema_description(entities, relations, attributes)

# generate tests
print("Generate tests")
tests = generate_metaqa_tests(TESTS_PATH, entities, relations, attributes)
print("Load {} tests".format(len(tests)))
tests = tests[39122:39132]

# set metrics and evaluation sets
number_of_tests = len(tests)
exact_translations = []
successful_compilations = [] 
correct_responses = []
mismatch_translation = []
unsuccessful_compilations = []
wrong_responses = []

# get the model
model = get_model()

# update metrics for each test case
test_index = 1
for test in tests:
    print("Checking test: ", str(test_index))
    test_index += 1

    # get natural language query and target formal query
    query, target_formal_query = test

    # make the natural language query to the model
    formal_query = model.run(query_language=query_language, database_type=database_type, schema=schema, query=query)

    # check for exact translation
    if formal_query == target_formal_query:
        exact_translations.append(test)
    else:
        mismatch_translation.append(test)

    # run the formal query in the database
    try:
        response = gc.make_query(formal_query)
        successful_compilations.append(test)
    except: # in case of no compilation, continue
        unsuccessful_compilations.append(test)
        wrong_responses.append(test)
        continue

    # run the target formal query
    try:
        target_response = gc.make_query(target_formal_query)
    except:
        raise Exception("The target formal queries can not fail during compile time!!! Fix them")

    # check responses match
    if QueryUtils.equal_simple_query_results(response, target_response):
        correct_responses.append(test)
    else:
        wrong_responses.append(test)

# prepare metrics and generate results .csv files
number_of_exact_translations = len(exact_translations)
number_of_successful_compilations = len(successful_compilations)
number_of_correct_responses = len(correct_responses)

exact_translations_avg = (number_of_exact_translations/number_of_tests)*100
successful_compilations_avg = (number_of_successful_compilations/number_of_tests)*100
correct_responses_avg = (number_of_correct_responses/number_of_tests)*100

global_metrics_results = pd.DataFrame(data={
    "number_of_tests": [number_of_tests],
    "number_of_exact_translations": [number_of_exact_translations],
    "number_of_successful_compilations": [number_of_successful_compilations],
    "number_of_correct_responses": [number_of_correct_responses],
    "exact_translations_avg": [exact_translations_avg],
    "successful_compilations_avg": [successful_compilations_avg],
    "correct_responses_avg": [correct_responses_avg]
})

# save global metric to csv
global_metrics_results.to_csv("./results/global_metrics_results.csv")

# store specific cases into csvs
exact_translations = pd.DataFrame(exact_translations, columns=["query", "target_query"]).to_csv("./results/exact_translations.csv")
successful_compilations = pd.DataFrame(successful_compilations, columns=["query", "target_query"]).to_csv("./results/successful_compilations.csv")
correct_responses = pd.DataFrame(correct_responses, columns=["query", "target_query"]).to_csv("./results/correct_responses.csv")
mismatch_translation = pd.DataFrame(mismatch_translation, columns=["query", "target_query"]).to_csv("./results/mismatch_translation.csv")
unsuccessful_compilations = pd.DataFrame(unsuccessful_compilations, columns=["query", "target_query"]).to_csv("./results/unsuccessful_compilations.csv")
wrong_responses = pd.DataFrame(wrong_responses, columns=["query", "target_query"]).to_csv("./results/wrong_responses.csv")