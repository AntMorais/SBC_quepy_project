import json
import sys
import process_files
import main
import clustering
import process_questions

train_qald_json = json.load(open("data/qald-6-train-multilingual.json"))
test_qald_json = json.load(open("data/qald-6-test-multilingual.json"))
train_and_test_qald_json = json.load(open("data/qald-6-train-and-test-multilingual.json"))
test_questions =  open("data/test_questions.txt", "r")
config_file = json.load(open("print_config.json"))




if __name__ == "__main__":
    if sys.argv[3] == "print":
        print_flag = True
    elif sys.argv[2] == "noprint":
        print_flag = False
    
    # possible values: train, test or both (only for qald)
    if sys.argv[1] == "qald":
        if sys.argv[2] == "train":
            dataset_json = train_qald_json
        elif sys.argv[2] == "test":
            dataset_json = test_qald_json
        elif sys.argv[2] == "both":
            dataset_json = train_and_test_qald_json
        process_questions.process_qald_questions(dataset_json, config_file, print_flag)
    elif sys.argv[1] == "test":
        process_questions.process_test_questions(test_questions, config_file, print_flag)
    
    

    """
    not_generated_questions = process_files.read_questions("data/questions_not_generated.json")
    category_summary={
        'question_types': [],
        'question_prefixes': [],
        'category_list': []
    }
    category={
        'question_type': "",
        'question_prefix': "",
        'question_list': []
    }

    for question in not_generated_questions:
        tagged_words = clustering.simple_tag_words(question)
        first_word = [tagged_words[0][0], tagged_words[1][0], tagged_words[2][0]]
        if first_word not in category_summary['question_prefixes']:
            category={
                'question_type': "",
                'question_prefix': first_word,
                'question_list': [question]
            }
            category_summary['question_prefixes'].append(first_word)
            category_summary['category_list'].append(category)
        else:
            for cat in category_summary['category_list']:
                if cat['question_prefix']==first_word:
                    cat['question_list'].append(question)

    # sort category_list by length of question_list



    import pprint
    pp=pprint.PrettyPrinter(indent=4)
    sorted_categories = sorted(category_summary['category_list'], key=lambda k: len(k['question_list'])) 
    pp.pprint(sorted_categories)
    """


