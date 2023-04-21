from graph_contractor import GraphContractor
from generation import generate_eval_data

gc = GraphContractor(url='neo4j+s://5fc1bc71.databases.neo4j.io',password='GUIPdTc9tUjzTw63n47eFbcc6_rFbhjyI_OAg0tbcsU')
entities = gc.entities
relations = gc.relations
attributes = gc.attributes

eval_data = generate_eval_data(entities, relations, attributes)

bad_queries = []
n = 1

for test in eval_data:
    nl, ql = test
    print("Trying query: " + str(n))
    n += 1
    try:
        gc.make_query(ql)
    except BaseException as e:
        bad_queries.append((test, e))

print('The number of bad queries is: ', len(bad_queries))
for bq in bad_queries:
    print(bq)