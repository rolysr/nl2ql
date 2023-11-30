import pandas as pd


def get_query_types():
    query_types = {"hop0": dict(), "hop1": dict(), "hop2": dict()}
    type_of_query = dict()
    query_types_base_path = './metaqa_data/hop_reasoning/metaqa-'
    for i in range(3):
        with open(query_types_base_path + '{}hop/qa_test_qtype.txt'.format(i+1), 'r') as qtype_file:
            lines_qtype = qtype_file.readlines()
            with open(query_types_base_path + '{}hop/ntm/qa_test.txt'.format(i+1), 'r') as q_file:
                lines_q = q_file.readlines()
                if len(lines_q) != len(lines_qtype):
                    print("Test set length error")
                    return
                for j in range(len(lines_q)):
                    query_text = lines_q[j].strip().split('\t')[0]
                    query_type = lines_qtype[j]
                    type_of_query[query_text] = query_type
                    if query_type not in query_types['hop{}'.format(i)].keys():
                        query_types['hop{}'.format(i)][query_type] = 0
                    query_types['hop{}'.format(i)][query_type] += 1
    
    return query_types, type_of_query

def get_corrects_query_types(type_of_query):
    corrects_query_type = dict()
    results_base_path = './results/classic_metaqa/gpt-4/hop'
    for i in range(3):
        df = pd.read_csv(results_base_path + '{}/correct_responses.csv'.format(i))
        for value in df['query']:
            query_type = type_of_query[value]
            if query_type not in corrects_query_type.keys():
                corrects_query_type[query_type] = 0
            corrects_query_type[query_type] += 1
    return corrects_query_type

query_types, type_of_query = get_query_types()
corrects_query_type = get_corrects_query_types(type_of_query)

print(len(type_of_query.keys()))
print('**********************************')
for elem1 in query_types.keys():
    print(elem1, len(query_types[elem1]))
    print('-------------------------------------')
    for elem2 in query_types[elem1].keys():
        print(elem2, corrects_query_type[elem2], query_types[elem1][elem2], (corrects_query_type[elem2]/query_types[elem1][elem2])*100.00)
    print('**********************************')