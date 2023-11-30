import os
from dotenv import load_dotenv
import pandas as pd
from generation.metaqa import generate_metaqa_tests
from graph import GraphContractor

load_dotenv()

NEO4J_DB_URL = os.getenv('NEO4J_DB_URL_CLASSIC')
NEO4J_DB_USER = os.getenv('NEO4J_DB_USER')
NEO4J_DB_PASSWORD = os.getenv('NEO4J_DB_PASSWORD')
KB_PATH = os.getenv('KB_PATH')
TESTS_PATH = os.getenv('TESTS_PATH')

# Init graph contractor instance to interact with Neo4J DB
gc = GraphContractor(NEO4J_DB_URL, NEO4J_DB_USER, NEO4J_DB_PASSWORD)

def put_results_on_files(hop_index, model_name, successful_compilations_wrong_answers, unsuccessful_compilations_wrong_answers, precision, recall, f1):
    number_of_successful_compilations_wrong_answers = len(successful_compilations_wrong_answers)
    number_of_unsuccessful_compilations_wrong_answers = len(unsuccessful_compilations_wrong_answers)

    PATH_RESULTS_PREFIX = 'results/classic_metaqa/{}/hop{}'.format(
        model_name, hop_index)

    stats_prf1 = pd.DataFrame(data={
        "precision": [precision],
        "recall": [recall],
        "f1_score": [f1]
    })

    try:
        os.mkdir('results')
    except:
        pass
    try:
        os.mkdir('results/classic_metaqa')
    except:
        pass
    try:
        os.mkdir('results/classic_metaqa/{}'.format(model_name))
    except:
        pass
    try:
        os.mkdir('results/classic_metaqa/{}/hop{}'.format(model_name, hop_index))
    except:
        pass

    # store specific cases into csvs
    successful_compilations_wrong_answers = pd.DataFrame(successful_compilations_wrong_answers, columns=[
        "query", "target_query", "generated_query"]).to_csv(PATH_RESULTS_PREFIX + "/successful_compilations_wrong_answers.csv")
    unsuccessful_compilations_wrong_answers = pd.DataFrame(unsuccessful_compilations_wrong_answers, columns=[
        "query", "target_query", "generated_query"]).to_csv(PATH_RESULTS_PREFIX + "/unsuccessful_compilations_wrong_answers.csv")
    stats_prf1 = pd.DataFrame(stats_prf1, columns=[
        "precision", "recall", "f1_score"]).to_csv(PATH_RESULTS_PREFIX + "/stats_prf1.csv")

def get_tp_fp_fn_for_hop(hop_id):
    tp, fp, fn = 0, 0, 0
    successful_compulations_wrong_answers, unsuccessful_compilations_wrong_answers = [], []
    query_response = dict()
    tests_hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-{}hop/ntm/qa_test.txt".format(hop_id+1), entities=[], relations=[], attributes=[], is_classic_metaqa=True)
    for test in tests_hop:
        query, response = test
        query_response[query] = set(response.split('|'))

    results_base_path = './results/classic_metaqa/gpt-4/hop'

    # For correct responses
    df = pd.read_csv(results_base_path + '{}/correct_responses.csv'.format(i))
    for index, row in df.iterrows():
        result_query = row['query']
        tp += len(query_response[result_query])

    # For wrong responses
    df = pd.read_csv(results_base_path + '{}/wrong_responses.csv'.format(i))
    for index, row in df.iterrows():
        print('Processing row {} from hop{}'.format(index, hop_id))
        q = row['query']
        formal_query = row['generated_query']
        target_response = query_response[q]
        try:
            response = gc.make_query(formal_query)
            response = {data[list(data.keys())[0]] for data in response}
            tp += len(response & target_response)
            fp += len(response - target_response)
            fn += len(target_response - response)
            successful_compulations_wrong_answers.append((q, response, target_response))
        except:
            fn += len(target_response)
            unsuccessful_compilations_wrong_answers.append((q, formal_query, target_response))

    return tp, fp, fn, unsuccessful_compilations_wrong_answers, successful_compulations_wrong_answers

def get_precision_recall_f1_for_hop(hop_id):
    tp, fp, fn, ucwa, scwa = get_tp_fp_fn_for_hop(hop_id)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2* (precision * recall) / (precision + recall)
    return precision, recall, f1, ucwa, scwa, tp, fp, fn

for i in range(3):
    precision, recall, f1, ucwa, scwa, tp, fp, fn = get_precision_recall_f1_for_hop(i)
    print('For Hop {}: Precision={}, Recall={}, F1={}, Unsuccessful Compilations={}, True Positives={}, False Positive={}, False Negative={}'.format(i, precision, recall, f1, len(ucwa), tp, fp, fn))
    put_results_on_files(i, 'gpt-4', scwa, ucwa, precision, recall, f1)