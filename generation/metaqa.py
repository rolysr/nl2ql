import json
import random

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

def generate_template_pairs_agg_nested_tests_metaqa(entities, relations, attributes):
    template_pairs = []

    for label in entities:
        properties = attributes[label]
        
        # Generate COUNT templates
        template_pairs.append(generate_count_templates(label))
        
        # Generate MIN, MAX, AVG templates for numeric properties
        for prop in properties:
            if prop[1] != 'str' and prop[1] != 'unknown':
                template_pairs.append(generate_avg_template(label, prop[0]))
                template_pairs.append(generate_max_template(label, prop[0]))
                template_pairs.append(generate_min_template(label, prop[0]))

        # Generate MIN, MAX, AVG templates for numeric properties with conditionals
        conditional_ops = ['>', '<', '=', '>=', '<=']
        for prop in properties:
            if prop[1] != 'str' and prop[1] != 'unknown':
                condition_prop = prop[0]  # Replace with actual property for condition
                for cond in conditional_ops:
                    condition_value = cond + " " + str(random.randint(int(prop[2]), int(prop[3])))  # Replace with actual value or range for condition
                    template_pairs.append(generate_conditional_count_template(label, prop[0], condition_value))
                    template_pairs.append(generate_conditional_max_template(label, prop[0], condition_prop, condition_value))
                    template_pairs.append(generate_conditional_min_template(label, prop[0], condition_prop, condition_value))
                    template_pairs.append(generate_conditional_avg_template(label, prop[0], condition_prop, condition_value))
    
    for rel_type in relations:
        for rel in relations[rel_type]:
            # Generate relationship COUNT templates
            start_label, end_label = rel[0], rel[1]
            template_pairs.append(generate_relationship_count_templates(start_label, end_label, rel_type))
            
            # Generate nested query templates
            template_pairs.append(generate_nested_query_templates(start_label, end_label, rel_type))
    
    return template_pairs

def generate_metaqa_tests(tests_path: str, entities, relations, attributes, is_classic_metaqa=False):
    test_cases = []
    
    # Open the file in read mode and load the JSON
    with open(tests_path, 'r') as file:
        if is_classic_metaqa:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    question, answer = parts
                    test_cases.append((question, answer))
        else:
            data = json.load(file)

            # Now, take all default MetaQA test cases.
            for item in data:
                question_text = item['question'].replace("'", "")
                test_cases.append((question_text, item['LF']))

            # Add the tests created for Aggregation Functions and Nested Queries
            agg_nested_queries_metaqa = generate_template_pairs_agg_nested_tests_metaqa(entities, relations, attributes)
            test_cases = test_cases + agg_nested_queries_metaqa

    return test_cases