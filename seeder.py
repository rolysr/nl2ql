from metaqakb import MetaQAKnowledgeBase


class DBSeeder:

    def __init__(self, metaqa_kb: MetaQAKnowledgeBase, db_base_file_path: str) -> None:
        self.metaqa_kb = metaqa_kb
        self.db_base_file_path = db_base_file_path

    def seed_db(self):
            # Open the file for reading
            with open(self.db_base_file_path, 'r') as file:
                # Iterate over each line in the file
                line_count = 1
                for line in file:
                    print("Analyzing line number: ", line_count)
                    line_count = line_count + 1
                    # Print the current line
                    line = line.strip()  # strip() is used to remove any trailing newline characters
                    line = line.split('|')
                    
                    # Create entities, attributes and relations
                    self.create_entities_relations_attributes(line[0], line[1], line[2])

    def create_entities_relations_attributes(self, entity1, relation_type, entity2):
        # Avoid ' character error when placed on a query
        entity1 = entity1.replace("'", "")
        entity2 = entity2.replace("'", "")
        
        # Check if entity1 exists
        if not self.metaqa_kb.entity_exists(label='Movie', property_name='name', property_value=entity1):
            self.metaqa_kb.graph.make_query(f"CREATE (:Movie {{name: '{entity1}'}})")

        if relation_type == 'directed_by':
            if not self.metaqa_kb.entity_exists(label='Director', property_name='name', property_value=entity2):
                self.metaqa_kb.graph.make_query(f"CREATE (:Director {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.metaqa_kb.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Director {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'written_by':
            if not self.metaqa_kb.entity_exists(label='Writer', property_name='name', property_value=entity2):
                self.metaqa_kb.graph.make_query(f"CREATE (:Writer {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.metaqa_kb.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Writer {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'starred_actors':
            if not self.metaqa_kb.entity_exists(label='Actor', property_name='name', property_value=entity2):
                self.metaqa_kb.graph.make_query(f"CREATE (:Actor {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.metaqa_kb.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Actor {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'release_year':
            if not self.metaqa_kb.entity_has_attribute(label='Movie', property_name='release_year', entity_name=entity1):
                # If it doesn’t have a release_year attribute, add it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.release_year = {entity2}")
            else:
                # If it already has a release_year attribute, update it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.release_year = {entity2}")

        elif relation_type == 'in_language':
            # If the Movie entity already exists, check if it has a language attribute
            if not self.metaqa_kb.entity_has_attribute(label='Movie', property_name='language', entity_name=entity1):
                # If it doesn’t have a language attribute, add it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.language = '{entity2}'")
            else:
                # If it already has a language attribute, update it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.language = '{entity2}'")

        elif relation_type == 'has_tags':
            if not self.metaqa_kb.entity_exists(label='Tag', property_name='name', property_value=entity2):
                self.metaqa_kb.graph.make_query(f"CREATE (:Tag {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.metaqa_kb.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Tag {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'has_genre':
            if not self.metaqa_kb.entity_exists(label='Genre', property_name='name', property_value=entity2):
                self.metaqa_kb.graph.make_query(f"CREATE (:Genre {{name: '{entity2}'}})")
            relation_type_upper = relation_type.upper()
            self.metaqa_kb.graph.make_query(f"""MATCH (a:Movie {{name: '{entity1}'}}), (b:Genre {{name: '{entity2}'}}) CREATE (a)-[:{relation_type_upper}]->(b)""")

        elif relation_type == 'has_imdb_votes':
            # If the Movie entity already exists, check if it has a language attribute
            if not self.metaqa_kb.entity_has_attribute(label='Movie', property_name='imdb_votes', entity_name=entity1):
                # If it doesn’t have a language attribute, add it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_votes = '{entity2}'")
            else:
                # If it already has a language attribute, update it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_votes = '{entity2}'")

        elif relation_type == 'has_imdb_rating':
            # If the Movie entity already exists, check if it has a language attribute
            if not self.metaqa_kb.entity_has_attribute(label='Movie', property_name='imdb_rating', entity_name=entity1):
                # If it doesn’t have a language attribute, add it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_rating = '{entity2}'")
            else:
                # If it already has a language attribute, update it
                self.metaqa_kb.graph.make_query(f"MATCH (a:Movie {{name: '{entity1}'}}) SET a.imdb_rating = '{entity2}'")

        else:
            pass