import json


def generate_metaqa_tests(tests_path: str):
    test_cases = []
    
    # Open the file in read mode and load the JSON
    with open(tests_path, 'r') as file:
        data = json.load(file)

        # Now, data is a Python list containing dictionaries, and you can iterate over it and access individual elements as needed.
        for item in data:
            test_cases.append((item['question'], item['LF']))

    return test_cases
