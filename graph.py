from py2neo import Graph


class GraphContractor(Graph):
    """
        Graph Contractor class for interacting with a Neo4J DB instance
    """

    def __init__(self, url, name, password):
        try:
            self.graph = Graph(url, auth=(name, password))

        except Exception as e:
            print(e)
            print('Error connecting to the database(Remember VPN)')

    def make_query(self, query: str):
        try:
            return self.graph.run(query).data()
        except BaseException as e:
            print(e)
            return str(e)