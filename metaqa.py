from graph import GraphContractor
from query_utils import QueryUtils


class MetaQAKnowledgeBase:
    def __init__(self, graph: GraphContractor, db_base_filepath: str) -> None:
        self.graph = graph
        self.db_base_filepath = db_base_filepath
        self._seed_db()
        self._compute_entities()
        self._compute_relations()
        self._compute_attributes()
        
    def _seed_db(self):
        # Open the file for reading
        with open(self.db_base_filepath, 'r') as file:
            # Iterate over each line in the file
            for line in file:
                # Print the current line
                line = line.strip()  # strip() is used to remove any trailing newline characters
                line = line.split('|')
                
                # Create entities, attributes and relations
                self.create_entities_relations_attributes(line[0], line[1], line[2])

    def create_entities_relations_attributes(self, entity1, relation_type, entity2):
        # Check if entity1 exists
        if not self.entity_exists(label='Movie', property_name='name', property_value=entity1):
            self.graph.make_query(f"CREATE (:Movie {{name: '{entity1}'}})")

        if relation_type == 'directed_by':
            if not self.entity_exists(label='Director', property_name='name', property_value=entity2):
                self.graph.make_query(f"CREATE (:Director {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Director {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'written_by':
            if not self.entity_exists(label='Writer', property_name='name', property_value=entity2):
                self.graph.make_query(f"CREATE (:Writer {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Writer {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'starred_actors':
            if not self.entity_exists(label='Actor', property_name='name', property_value=entity2):
                self.graph.make_query(f"CREATE (:Actor {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Actor {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'release_year':
            if not self.entity_has_attribute(label='Movie', property_name='release_year', entity_name=entity1):
                # If it doesn’t have a release_year attribute, add it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.release_year = {entity2}")
            else:
                # If it already has a release_year attribute, update it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.release_year = {entity2}")

        elif relation_type == 'in_language':
            # If the Movie entity already exists, check if it has a language attribute
            if not self.entity_has_attribute(label='Movie', property_name='language', entity_name=entity1):
                # If it doesn’t have a language attribute, add it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.language = '{entity2}'")
            else:
                # If it already has a language attribute, update it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.language = '{entity2}'")

        elif relation_type == 'has_tags':
            if not self.entity_exists(label='Tag', property_name='name', property_value=entity2):
                self.graph.make_query(f"CREATE (:Tag {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Tag {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'has_genre':
            if not self.entity_exists(label='Genre', property_name='name', property_value=entity2):
                self.graph.make_query(f"CREATE (:Genre {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Genre {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'has_imdb_votes':
            # If the Movie entity already exists, check if it has a language attribute
            if not self.entity_has_attribute(label='Movie', property_name='imdb_votes', entity_name=entity1):
                # If it doesn’t have a language attribute, add it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_votes = '{entity2}'")
            else:
                # If it already has a language attribute, update it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_votes = '{entity2}'")

        elif relation_type == 'has_imdb_rating':
            # If the Movie entity already exists, check if it has a language attribute
            if not self.entity_has_attribute(label='Movie', property_name='imdb_rating', entity_name=entity1):
                # If it doesn’t have a language attribute, add it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_rating = '{entity2}'")
            else:
                # If it already has a language attribute, update it
                self.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_rating = '{entity2}'")

        else:
            pass

    def entity_exists(self, label, property_name, property_value):
        query = f"MATCH (n:{label} {{{property_name}: '{property_value}'}}) RETURN n LIMIT 1"
        result = self.graph.make(query).data()
        return len(result) > 0
    
    def entity_has_attribute(self, label, property_name, entity_name):
        query = f"MATCH (n:{label} {{name: '{entity_name}'}}) RETURN n.{property_name} IS NOT NULL AS has_attribute"
        result = self.graph.make_query(query).data()
        return len(result) > 0 and result[0]['has_attribute']

    def _compute_entities(self):
        ent = self.graph.run('CALL db.labels()')
        self.entities = QueryUtils._unfold_graph_resp(ent)

    def _compute_attributes(self):
        self.attributes = {}
        for entity in self.entities:
            self.attributes[entity] = self._get_keys_of_label(entity)
        for relation in self.relations:
            self.attributes[relation] = self._get_keys_of_relation(relation)

    def _get_keys_of_label(self, label):
        resp = self.graph.run(f'MATCH (p:{label}) WITH DISTINCT keys(p) as key_list UNWIND key_list as key RETURN DISTINCT key')
        return QueryUtils._unfold_graph_resp(resp)

    def _get_keys_of_relation(self, relation):
        resp = self.graph.run(f'MATCH ()-[r:{relation}]-() WITH DISTINCT keys(r) as key_list UNWIND key_list as key RETURN DISTINCT key')
        return QueryUtils._unfold_graph_resp(resp)

    def _compute_relations(self):
        self.relations = QueryUtils._unfold_graph_resp(self.graph.run(f'CALL db.relationshipTypes'))
        self.relations = { rel:[] for rel in self.relations}
        for entity_x in self.entities:
            for entity_y in self.entities:
                rels = QueryUtils._unfold_graph_resp(self.graph.run(f'MATCH (x:{entity_x})-[r]->(y:{entity_y}) RETURN DISTINCT type(r)'))
                for rel in rels:
                    self.relations[rel].append((entity_x, entity_y))