class DBSchemaMaker:
    
    @staticmethod
    def compute_schema_description(entities, relations, attributes):
        schema_description = ""
        schema_description += f"Entities: {entities}\n"
        for entity in entities:
            entity_attrs = attributes[entity]
            if len(entity_attrs) > 0:
                schema_description += f"The entity named {entity} has the attributes: {[attr[0] for attr in entity_attrs]}\n"
        for relation in relations:
            for ent1, ent2, is_double_sense in relations[relation]: 
                if is_double_sense:
                    schema_description += f"There is a relation called {relation} between the entitites {ent1} and {ent2}. The relation {relation} can be used in both senses.\n"
                    continue
                schema_description += f"There is a relation called {relation} from {ent1} to {ent2}.\n"
            if len(attributes[relation]) > 0:
                schema_description += f"The relation {relation} has attributes {attributes[relation]}\n"
        return schema_description