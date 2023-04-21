def generate_tests(entities, relations, attributes):
    test_set_nl_ql = []
    
    # get entity
    for entity in entities:
        test_set_nl_ql.append((f"Give all the information about {entity}s", f"MATCH (e:{entity}) RETURN e"))
        test_set_nl_ql.append((f"What are the instances of {entity}s", f"MATCH (e:{entity}) RETURN e"))
        test_set_nl_ql.append((f"Get all the information from {entity}s", f"MATCH (e:{entity}) RETURN e"))

    # get attribute from entity
    for entity in entities:
        attrs = attributes[entity]
        for attr in attrs:
            test_set_nl_ql.append((f"Give the attribute {attr} from the entity {entity}", f"MATCH (e:{entity}) RETURN e.{attr}"))
            test_set_nl_ql.append((f"Which is the value of {attr} in {entity}", f"MATCH (e:{entity}) RETURN e.{attr}"))
    
    # domain specific queries
    movie_names = ["The Matrix", "Top Gun","Stand By Me", "As Good as It Gets", "The Green Mile"]

    for movie_name in movie_names:
        for relation in relations:
            ent1, ent2 = relations[relation][0]
            if ent2 == 'Movie':
                test_set_nl_ql.append((f"Who {relation.lower()} the movie called {movie_name}", "MATCH (p:Person)-[r:{relation}]-(m:Movie {{title: '{movie_name}'}}) RETURN p.name".format(relation=relation.lower(), movie_name=movie_name)))
                test_set_nl_ql.append((f"Which is the name of the person who {relation.lower()} the movie called {movie_name}", "MATCH (p:Person)-[r:{relation}]-(m:Movie {{title: '{movie_name}'}}) RETURN p.name".format(relation=relation.lower(), movie_name=movie_name)))
                test_set_nl_ql.append((f"Return the name of the person who {relation.lower()} the movie called {movie_name}", "MATCH (p:Person)-[r:{relation}]-(m:Movie {{title: '{movie_name}'}}) RETURN p.name".format(relation=relation.lower(), movie_name=movie_name)))

    # other queries:
    test_set_nl_ql.append(("Return all the movies that were released after the year 2000 limiting the result to 5 items.", "MATCH (m:Movie) WHERE m.released > 2000 RETURN m LIMIT 5"))
    test_set_nl_ql.append(("Retrieve all the movies released after the year 2005", "MATCH (m:Movie) WHERE m.released > 2005 RETURN m"))
    test_set_nl_ql.append(("Get the count of movies released after the year 2005.", "MATCH (m:Movie) WHERE m.released > 2005 RETURN COUNT(m)"))
    test_set_nl_ql.append(("return all Person nodes who directed a movie that was released after 2010.", "MATCH (p:Person)-[d:ACTED_IN]-(m:Movie) WHERE m.released > 2010 RETURN p,d,m"))
    test_set_nl_ql.append(("return only Person nodes (limiting to 20 items)", "MATCH (p:Person) RETURN p LIMIT 20"))
    test_set_nl_ql.append(("return all kinds of nodes (limiting to 20 items)", "MATCH (n) RETURN n LIMIT 20"))
    test_set_nl_ql.append(("return Movie nodes but with only the title and released properties.", "MATCH (m:Movie) RETURN m.title, m.released"))
    test_set_nl_ql.append(("get name and born properties of the Person node", "MATCH (p:Person) RETURN p.name, p.born"))
    test_set_nl_ql.append(("Give me all data about Tom Hanks","MATCH (p:Person {name: 'Tom Hanks'}) RETURN p"))
    test_set_nl_ql.append(("Give me all data about Tom Hanks", "MATCH (p:Person) WHERE p.name = 'Tom Hanks' RETURN p"))
    test_set_nl_ql.append(("Find the movie with title Cloud Atlas", "MATCH (m:Movie {title: 'Cloud Atlas'}) RETURN m"))
    test_set_nl_ql.append(("Get all the movies that were released between 2010 and 2015.", "MATCH (m:Movie) WHERE m.released > 2010 AND m.released < 2015 RETURN m"))
    test_set_nl_ql.append(("Write a query to find the nodes Person and Movie which are connected by a REVIEWED relationship and is outgoing from the Person node and incoming to the Movie node", "MATCH (p:Person)-[r:REVIEWED]-(m:Movie) RETURN p,r,m"))
    test_set_nl_ql.append(("""Finding who directed the "Cloud Atlas" movie""", "MATCH (m:Movie {title: 'Cloud Atlas'})<-[d:DIRECTED]-(p:Person) RETURN p.name"))
    test_set_nl_ql.append(("Finding all people who have co-acted with Tom Hanks in any movie", """MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(p:Person) RETURN p.name"""))
    test_set_nl_ql.append(("""Finding all people related to the movie "Cloud Atlas" in any way""", """MATCH (p:Person)-[relatedTo]-(m:Movie {title: "Cloud Atlas"}) RETURN p.name, type(relatedTo)"""))
    test_set_nl_ql.append(("Finding Movies and Actors that are 3 hops away from Kevin Bacon.", "MATCH (p:Person {name: 'Kevin Bacon'})-[*1..3]-(hollywood) RETURN DISTINCT p, hollywood"))

    return test_set_nl_ql