import json
import sys

def read_questions(file_path):
    list_questions = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        for el in data:
            questions = el["question"]
            for q in questions:
                if q['language']=='en':
                    list_questions.append(q['string'])
                    continue
    return list_questions


#write to json files
def write_to_json_files(questions_dict_not_generated, questions_dict_no_answer, questions_dict_answer, metrics):
    with open('data/questions_not_generated.json', 'w') as fout:
        json.dump(questions_dict_not_generated, fout)
    with open('data/questions_no_answer.json', 'w') as fout:
        json.dump(questions_dict_no_answer, fout)
    with open('data/questions_answer.json', 'w') as fout:
        json.dump(questions_dict_answer, fout)
    with open('data/metrics.json', 'w') as fout:
        json.dump(metrics, fout)


