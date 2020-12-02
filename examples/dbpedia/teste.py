import pickle
import subprocess
import main
import json
import sys

dataset_json = json.load(open("data/qald-6-train-multilingual.json"))
questions_json = dataset_json['questions']



#file_path = "data/trainData.pickle"
#question_list = pickle.load(open(file_path, "rb"))
print_handlers = {
        "define": main.print_define,
        "enum": main.print_enum,
        "time": main.print_time,
        "literal": main.print_literal,
        "age": main.print_age,
}


num_questions = len(questions_json)
num_not_generated = 0
num_no_answer = 0

global_precision = 0
global_recall = 0

questions_dict_answer = []
questions_dict_no_answer = []
questions_dict_not_generated = []


# question_list has a specific question in every language
for question_list in questions_json:
    if question_list['id'] != "126":
        continue
    # question_dict has question dictionary
    question_dict = [q for q in question_list['question'] if q['language']=='en'][0]
    # question is the question string
    question = question_dict['string']


    # the question has no answers
    if not question_list['answers']:
        num_questions -= 1
        continue
    correct_answer_dict = question_list['answers'][0]


    #print question
    #print "-" * len(question)

    target, query, metadata, target_entity = main.dbpedia.get_query(question)


    if isinstance(metadata, tuple):
        query_type = metadata[0]
        metadata = metadata[1]
    else:
        query_type = metadata
        metadata = None

    if query is None:
        #print "Query not generated :(\n"
        num_not_generated += 1
        questions_dict_not_generated.append(question_list)
        continue

    #print("----------------------------------------------")
    #print(question)
    #print query
    

    if target.startswith("?"):
        target = target[1:]
    if query:
        main.sparql.setQuery(query)
        main.sparql.setReturnFormat(main.JSON)
        results = main.sparql.query().convert()

        if not results["results"]["bindings"]:
            #print "No answer found :("
            num_no_answer += 1
            questions_dict_no_answer.append(question_list)
            continue

        questions_dict_answer.append(question_list)

        # Print results of the query
        import pprint
        pp=pprint.PrettyPrinter(indent=4)
        #pp.pprint(results)
        
        # TODO isto deve estar mal, temos de ir a answer type == resource
        answer_head_type = correct_answer_dict['head']['vars'][0]
        correct_results_dict = correct_answer_dict['results']['bindings']
        query_results_dict_all_languages = results["results"]["bindings"]
        # only keep english results
        query_results_dict = [el for el in query_results_dict_all_languages if el[target]['xml:lang']=='en']
        # identifier of the entity we want
        variable_name = str(target_entity[1:])
        # correct values from json data
        correct_results_values = [el[answer_head_type]['value'] for el in correct_results_dict]
        # list of values returned by query
        list_query_values = [el[variable_name]['value'] for el in query_results_dict]
        
        # number of correct answers
        number_correct_answers = sum(el in correct_results_values for el in list_query_values)
        # number of answers in the gold standard
        number_gold_answers = len(correct_results_dict)
        # number of answers returned by the system
        number_system_answers = len(query_results_dict)
        precision = number_correct_answers/number_system_answers
        recall = number_correct_answers/number_gold_answers
        
        global_precision += precision
        global_recall += recall

        
        #print_handlers[query_type](results, target, metadata)
        #print

global_precision = float(global_precision) / num_questions
global_recall = float(global_recall) / num_questions
try:
    f_measure = (2*global_precision*global_recall)/(global_precision+global_recall)
except ZeroDivisionError:
    print("There are no correct answers")
    f_measure = 0

print("Precision------>"+str(global_precision))
print("Recall------>"+str(global_recall))
print("F-measure------>"+str(f_measure))
metrics = {
    "precision": global_precision,
    "recall": global_recall,
    "f_measure": f_measure
}
#write to json files

with open('data/questions_not_generated.json', 'w') as fout:
    json.dump(questions_dict_not_generated, fout)
with open('data/questions_no_answer.json', 'w') as fout:
    json.dump(questions_dict_no_answer, fout)
with open('data/questions_answer.json', 'w') as fout:
    json.dump(questions_dict_answer, fout)
with open('data/metrics.json', 'w') as fout:
    json.dump(metrics, fout)