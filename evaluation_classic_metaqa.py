from generation.metaqa import generate_metaqa_tests

#Load the datasets
tests_1hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-1hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
print(len(tests_1hop))

tests_2hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-2hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
print(len(tests_2hop))

tests_3hop = generate_metaqa_tests(tests_path="./metaqa_data/hop_reasoning/metaqa-3hop/ntm/qa_test.txt", entities=[], relations=[], attributes=[], is_classic_metaqa=True)
print(len(tests_3hop))