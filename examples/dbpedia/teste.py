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
    
    
    # possible values: train, test or both (only for qald)
    if sys.argv[1] == "qald":
        
        if sys.argv[2] == "train":
            dataset_json = train_qald_json
        elif sys.argv[2] == "test":
            dataset_json = test_qald_json
        elif sys.argv[2] == "both":
            dataset_json = train_and_test_qald_json
        if sys.argv[3] == "print":
            print_flag = True
        elif sys.argv[3] == "noprint":
            print_flag = False    
        process_questions.process_qald_questions(dataset_json, config_file, print_flag)
    elif sys.argv[1] == "test":
        
        if sys.argv[2] == "print":
            print_flag = True
        elif sys.argv[2] == "noprint":
            print_flag = False    
        process_questions.process_test_questions(test_questions, config_file, print_flag)
    
    clustering.group_questions(config_file, print_flag)

    


