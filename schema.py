class DBSchemaMaker:
    
    @staticmethod
    def compute_schema_description(entities, relations, attributes):
        schema_description = ""
        schema_description += f"Entities: {entities}\n"
        for entity in entities:
            entity_attrs = attributes[entity]
            schema_description += f"The entity named {entity} has the attributes: {entity_attrs}\n"
        for relation in relations:
            for ent1, ent2 in relations[relation]: 
                schema_description += f"There is a relation called {relation} between the entitites {ent1} and {ent2}\n"
            if len(attributes[relation]) > 0:
                schema_description += f"The relation {relation} has attributes {attributes[relation]}\n"
        return schema_description