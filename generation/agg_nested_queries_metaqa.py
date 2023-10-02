def generate_count_templates(label):
    cypher_query = f"MATCH (n:{label}) RETURN COUNT(n) AS count"
    nl_query = f"How many {label.lower()} entities are there?"
    return nl_query, cypher_query

def generate_conditional_count_template(label, prop, condition_value):
    cypher_query = f"MATCH (n:{label}) WHERE n.{prop} {condition_value} RETURN COUNT(n) AS count"
    nl_query = f"How many {label.lower()} entities are there where {prop} is {condition_value}?"
    return nl_query, cypher_query

def generate_avg_template(label, prop):
    cypher_query = f"MATCH (n:{label}) RETURN AVG(n.{prop}) AS avg_{prop}"
    nl_query = f"What is the average value of {prop} for {label.lower()} entities?"
    return nl_query, cypher_query

def generate_conditional_avg_template(label, prop, condition_prop, condition_value):
    cypher_query = f"MATCH (n:{label}) WHERE n.{condition_prop} {condition_value} RETURN AVG(n.{prop}) AS avg_{prop}"
    nl_query = f"What is the average value of {prop} for {label.lower()} entities where {condition_prop} is {condition_value}?"
    return nl_query, cypher_query

def generate_max_template(label, prop):
    cypher_query = f"MATCH (n:{label}) RETURN MAX(n.{prop}) AS max_{prop}"
    nl_query = f"What is the maximum value of {prop} for {label.lower()} entities?"
    return nl_query, cypher_query

def generate_conditional_max_template(label, prop, condition_prop, condition_value):
    cypher_query = f"MATCH (n:{label}) WHERE n.{condition_prop} {condition_value} RETURN MAX(n.{prop}) AS max_{prop}"
    nl_query = f"What is the maximum value of {prop} for {label.lower()} entities where {condition_prop} is {condition_value}?"
    return nl_query, cypher_query

def generate_min_template(label, prop):
    cypher_query = f"MATCH (n:{label}) RETURN MIN(n.{prop}) AS min_{prop}"
    nl_query = f"What is the minimum value of {prop} for {label.lower()} entities?"
    return nl_query, cypher_query

def generate_conditional_min_template(label, prop, condition_prop, condition_value):
    cypher_query = f"MATCH (n:{label}) WHERE n.{condition_prop} {condition_value} RETURN MIN(n.{prop}) AS min_{prop}"
    nl_query = f"What is the minimum value of {prop} for {label.lower()} entities where {condition_prop} is {condition_value}?"
    return nl_query, cypher_query

def generate_relationship_count_templates(start_label, end_label, rel_type):
    cypher_query = f"MATCH (: {start_label})-[:{rel_type}]->(:{end_label}) RETURN COUNT(*) AS count"
    nl_query = f"How many {rel_type.lower()} relationships are there between {start_label.lower()} and {end_label.lower()} entities?"
    return nl_query, cypher_query

def generate_nested_query_templates(start_label, end_label, rel_type):
    cypher_query = f"MATCH (a:{start_label})-[:{rel_type}]->(b:{end_label}) WITH a, COLLECT(b) AS related_nodes RETURN a, related_nodes"
    nl_query = f"Can you list the {end_label.lower()} entities related to each {start_label.lower()} entity through {rel_type.lower()} relationships?"
    return nl_query, cypher_query

def generate_template_pairs(schema):
    template_pairs = []
    
    node_labels = schema.get_node_labels()
    relationship_types = schema.get_relationship_types()
    
    for label in node_labels:
        properties = schema.get_properties(label)
        
        # Generate COUNT templates
        template_pairs.append(generate_count_templates(label))
        
        # Generate MIN, MAX, AVG templates for numeric properties
        for prop in properties:
            if schema.is_numeric(prop):
                template_pairs.append(generate_avg_template(label, prop))
                template_pairs.append(generate_max_template(label, prop))
                template_pairs.append(generate_min_template(label, prop))

        # Generate MIN, MAX, AVG templates for numeric properties with conditionals
        for prop in properties:
            if schema.is_numeric(prop):
                condition_prop = "some_property"  # Replace with actual property for condition
                condition_value = "> some_value"  # Replace with actual value or range for condition
                template_pairs.append(generate_conditional_count_template(label, prop, condition_value))
                template_pairs.append(generate_conditional_max_template(label, prop, condition_prop, condition_value))
                template_pairs.append(generate_conditional_min_template(label, prop, condition_prop, condition_value))
                template_pairs.append(generate_conditional_avg_template(label, prop, condition_prop, condition_value))
    
    
    for rel_type in relationship_types:
        start_label, end_label = schema.get_connected_labels(rel_type)
        
        # Generate relationship COUNT templates
        template_pairs.append(generate_relationship_count_templates(start_label, end_label, rel_type))
        
        # Generate nested query templates
        template_pairs.append(generate_nested_query_templates(start_label, end_label, rel_type))
    
    return template_pairs