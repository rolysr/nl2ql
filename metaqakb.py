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
            attributes[entity] = []
            attrs_entity_names = self.get_keys_of_label(entity)
            for attribute_name in attrs_entity_names:
                attr_type, min_value, max_value = self.get_type_min_max_entity_attribute(entity, attribute_name)
                attributes[entity].append((attribute_name, attr_type, min_value, max_value))
        for relation in relations:
            attrs_relation_names = self.get_keys_of_relation(relation)
            attributes[relation] = []
            for attribute_name in attrs_relation_names:
                attr_type, min_value, max_value = self.get_type_min_max_relation_attribute(relation, attribute_name)
                attributes[relation].append((attribute_name, attr_type, min_value, max_value))
        return attributes
    
    def _infer_data_type(self, value):
        if isinstance(value, str):
            return "str"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        # Add more type checks as needed
        else:
            return "unknown"

    def get_type_min_max_entity_attribute(self, entity, attribute_name):
        # Query to get a sample value of the attribute for the entity
        query = f'''
        MATCH (p:{entity})
        WHERE p.{attribute_name} IS NOT NULL
        RETURN p.{attribute_name} as sample_value
        LIMIT 1
        '''
        resp = self.graph.graph.run(query).data()
        if not resp:
            return None, None, None

        sample_value = resp[0]['sample_value']
        attr_type = self._infer_data_type(sample_value)

        # If the attribute type is "str", return "str" and None for min and max
        if attr_type == "str":
            return "str", None, None

        # Otherwise, get the min and max values for the attribute
        query = f'''
        MATCH (p:{entity})
        RETURN 
            min(p.{attribute_name}) as min_value,
            max(p.{attribute_name}) as max_value
        LIMIT 1
        '''
        resp = self.graph.graph.run(query).data()
        return attr_type, resp[0]['min_value'], resp[0]['max_value']

    def get_type_min_max_relation_attribute(self, relation, attribute_name):
        # Query to get a sample value of the attribute for the relation
        query = f'''
        MATCH ()-[r:{relation}]-()
        WHERE r.{attribute_name} IS NOT NULL
        RETURN r.{attribute_name} as sample_value
        LIMIT 1
        '''
        resp = self.graph.graph.run(query).data()
        if not resp:
            return None, None, None

        sample_value = resp[0]['sample_value']
        attr_type = self._infer_data_type(sample_value)

        # If the attribute type is "str", return "str" and None for min and max
        if attr_type == "str":
            return "str", None, None

        # Otherwise, get the min and max values for the attribute
        query = f'''
        MATCH ()-[r:{relation}]-()
        RETURN 
            min(r.{attribute_name}) as min_value,
            max(r.{attribute_name}) as max_value
        LIMIT 1
        '''
        resp = self.graph.graph.run(query).data()
        return attr_type, resp[0]['min_value'], resp[0]['max_value']

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