from graph_contractor import GraphContractor
from generation import generate_tests
from model import get_model
import pandas as pd


# init graph contractor and get main schema components
gc = GraphContractor(url='neo4j+s://5fc1bc71.databases.neo4j.io',password='GUIPdTc9tUjzTw63n47eFbcc6_rFbhjyI_OAg0tbcsU')
entities = gc.entities
relations = gc.relations
attributes = gc.attributes

# generate tests
tests = generate_tests(entities, relations, attributes)

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

# prompt inputs
query_language = "Cypher"
database_type = "Neo4J"
schema = gc.schema_description

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
    if response == target_response:
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