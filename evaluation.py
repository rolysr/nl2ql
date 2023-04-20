from generation import generate_eval_data

gc = GraphContractor(url='neo4j+s://5fc1bc71.databases.neo4j.io',password='GUIPdTc9tUjzTw63n47eFbcc6_rFbhjyI_OAg0tbcsU')

eval_data = generate_eval_data(entities, relations, attributes)