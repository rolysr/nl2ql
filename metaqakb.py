from graph import GraphContractor
from query_utils import QueryUtils


class MetaQAKnowledgeBase:
    def __init__(self, graph: GraphContractor) -> None:
        self.graph = graph

    def entity_exists(self, label, property_name, property_value):
        property_value = property_value.replace("'", "")
        query = f"MATCH (n:{label} {{{property_name}: '{property_value}'}}) RETURN n LIMIT 1"
        result = self.graph.make_query(query)
        return len(result) > 0
    
    def entity_has_attribute(self, label, property_name, entity_name):
        entity_name = entity_name.replace("'", "")
        query = f"MATCH (n:{label} {{name: '{entity_name}'}}) RETURN n.{property_name} IS NOT NULL AS has_attribute"
        result = self.graph.make_query(query)
        return len(result) > 0 and result[0]['has_attribute']

    def compute_entities(self):
        ent = self.graph.graph.run('CALL db.labels()')
        entities = QueryUtils._unfold_graph_resp(ent)
        return entities

    def compute_attributes(self, entities, relations):
        attributes = {}
        for entity in entities:
            attributes[entity] = self.get_keys_of_label(entity)
        for relation in relations:
            attributes[relation] = self.get_keys_of_relation(relation)
        return attributes

    def get_keys_of_label(self, label):
        resp = self.graph.graph.run(f'MATCH (p:{label}) WITH DISTINCT keys(p) as key_list UNWIND key_list as key RETURN DISTINCT key')
        return QueryUtils._unfold_graph_resp(resp)

    def get_keys_of_relation(self, relation):
        resp = self.graph.graph.run(f'MATCH ()-[r:{relation}]-() WITH DISTINCT keys(r) as key_list UNWIND key_list as key RETURN DISTINCT key')
        return QueryUtils._unfold_graph_resp(resp)

    def compute_relations(self, entities):
        relations = QueryUtils._unfold_graph_resp(self.graph.graph.run(f'CALL db.relationshipTypes'))
        relations = { rel:[] for rel in relations}
        for entity_x in entities:
            for entity_y in entities:
                rels = QueryUtils._unfold_graph_resp(self.graph.graph.run(f'MATCH (x:{entity_x})-[r]->(y:{entity_y}) RETURN DISTINCT type(r)'))
                for rel in rels:
                    flag = False
                    for pair in relations[rel]:
                        if pair[0] == entity_y and pair[1] == entity_x and pair[2] == False:
                            pair[2] = True
                            flag = True
                    if not flag:
                        relations[rel].append([entity_x, entity_y, False])
        return relations