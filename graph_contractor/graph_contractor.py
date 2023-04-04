from py2neo import Graph
from graph_contractor.query_utils import QueryUtils


class GraphContractor(Graph):
    """
        Graph Contractor class for interacting with a Neo4J DB instance
    """

    def __init__(self, url, password):
        try:
            self.graph = Graph(url, password=password)
            self._compute_entities()
            self._compute_relations()
            self._compute_attributes()

        except Exception as e:
            print(e)
            print('Error connecting to the database(Remember VPN)')


    def make_query(self, query: str):
        if QueryUtils.not_valid_query(query):
            return 'Not a Valid Query!'

        return self.graph.run(query).data()

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