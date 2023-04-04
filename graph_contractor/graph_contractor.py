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
            self._compute_attributes()
            self._compute_relations()
            self._compute_schema()

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

    def _get_keys_of_label(self, label):
        resp = self._call_get_keys(label)
        return QueryUtils._unfold_graph_resp(resp)

    def _call_get_keys(self, label):
        return self.graph.run(f'MATCH (n:{label}) WITH n LIMIT 1000 UNWIND keys(n) as key RETURN distinct key')

    def _compute_relations(self):
        self.relations = []

    def _compute_schema(self):
        self.schema = QueryUtils._unfold_graph_resp(self.graph.run(f'CALL apoc.meta.stats YIELD labels, relTypes'))