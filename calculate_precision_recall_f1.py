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

def get_tp_fp_fn_for_hop(hop_id):
    tp, fp, fn = 0, 0, 0
    query_response = dict()
    tests_1hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-1hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
    for test in tests_1hop:
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
        q = row['query']
        formal_query = row['generated_query']
        target_response = query_response[q]
        response = gc.make_query(formal_query)
        response = {data[list(data.keys())[0]] for data in response}
        tp += len(response & target_response)
        fp += len(response - target_response)
        fn += len(target_response - response)

    return tp, fp, fn

def get_precision_recall_f1_for_hop(hop_id):
    tp, fp, fn = get_tp_fp_fn_for_hop(hop_id)
    precision = tp / (tp + fp)
    recall = tp / (tp + fp)
    f1 = 2* (precision * recall) / (precision + recall)
    return precision, recall, f1

for i in range(3):
    precision, recall, f1 = get_precision_recall_f1_for_hop(i)
    print('For Hop {}: Precision={}, Recall={}, F1={} '.format(i, precision, recall, f1))