import json


def generate_metaqa_tests(tests_path: str):
    test_cases = []
    
    # Open the file in read mode and load the JSON
    with open(tests_path, 'r') as file:
        data = json.load(file)

        # Now, take all test cases.
        for item in data:
            test_cases.append((item['question'], item['LF']))

    return test_cases