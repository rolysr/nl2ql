import os
import pandas as pd
from langchain.callbacks import get_openai_callback

from query_utils import QueryUtils


def put_results_on_files(hop_index, model_name, successful_compilations, correct_responses, unsuccessful_compilations, wrong_responses, number_of_tests, experiment_total_cost, end_time):
    number_of_successful_compilations = len(successful_compilations)
    number_of_correct_responses = len(correct_responses)

    successful_compilations_avg = (
        number_of_successful_compilations/number_of_tests)*100
    correct_responses_avg = (number_of_correct_responses/number_of_tests)*100

    global_metrics_results = pd.DataFrame(data={
        "number_of_tests": [number_of_tests],
        "number_of_successful_compilations": [number_of_successful_compilations],
        "number_of_correct_responses": [number_of_correct_responses],
        "successful_compilations_avg": [successful_compilations_avg],
        "correct_responses_avg": [correct_responses_avg],
        "experiment_total_cost": [experiment_total_cost],
        "time_elapsed_in_seconds": end_time
    })

    PATH_RESULTS_PREFIX = 'results/classic_metaqa/{}/hop{}'.format(
        model_name, hop_index)

    try:
        os.mkdir('results')
    except:
        pass
    try:
        os.mkdir('results/classic_metaqa')
    except:
        pass
    try:
        os.mkdir('results/classic_metaqa/{}'.format(model_name))
    except:
        pass
    try:
        os.mkdir('results/classic_metaqa/{}/hop{}'.format(model_name, hop_index))
    except:
        pass

    # save global metric to csv
    global_metrics_results.to_csv(
        PATH_RESULTS_PREFIX + "/global_metrics_results.csv")

    # store specific cases into csvs
    successful_compilations = pd.DataFrame(successful_compilations, columns=[
        "query", "target_query", "generated_query"]).to_csv(PATH_RESULTS_PREFIX + "/successful_compilations.csv")
    correct_responses = pd.DataFrame(correct_responses, columns=["query", "target_query", "generated_query"]).to_csv(
        PATH_RESULTS_PREFIX + "/correct_responses.csv")
    unsuccessful_compilations = pd.DataFrame(unsuccessful_compilations, columns=[
        "query", "target_query", "generated_query"]).to_csv(PATH_RESULTS_PREFIX + "/unsuccessful_compilations.csv")
    wrong_responses = pd.DataFrame(wrong_responses, columns=[
        "query", "target_query", "generated_query"]).to_csv(PATH_RESULTS_PREFIX + "/wrong_responses.csv")


def update_metrics_tests(model, tests, query_language, database_type, schema, gc, successful_compilations, unsuccessful_compilations, correct_responses, wrong_responses):
    test_index = 1
    experiment_total_cost = 0
    for test in tests:
        print("Checking test: ", str(test_index))
        test_index += 1

        # get natural language query and target formal query
        query, target_response = test

        # make the natural language query to the model
        with get_openai_callback() as cb:
            formal_query = model.run(query_language=query_language,
                                     database_type=database_type, schema=schema, query=query)

        # update total cost
        experiment_total_cost += cb.total_cost

        # run the formal query in the database
        try:
            response = gc.make_query(formal_query)
            new_test = (test[0], test[1], formal_query)
            successful_compilations.append(new_test)
        except:  # in case of no compilation, continue
            new_test = (test[0], test[1], formal_query)
            unsuccessful_compilations.append(new_test)
            wrong_responses.append(new_test)
            continue

        # check responses match
        if QueryUtils.equal_classic_query_results(response, target_response):
            new_test = (test[0], test[1], formal_query)
            correct_responses.append(new_test)
        else:
            new_test = (test[0], test[1], formal_query)
            wrong_responses.append(new_test)
    return experiment_total_cost
