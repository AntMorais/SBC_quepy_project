import json
import sys
import process_files
import main
import clustering
import pprint



def process_test_questions(test_questions, config_file, print_flag):
    lines = test_questions.readlines()

    question_flag = config_file['question']
    query_flag = config_file['query']
    results_flag =config_file['results']
    answers_flag = config_file['show_answers']
    answered_flag = config_file['answered']
    no_answers_flag = config_file['not_answered']
    not_gen_flag = config_file['not_generated']
    if not print_flag:
        question_flag = False
        query_flag = False
        results_flag = False
        answers_flag = False
        answered_flag = False
        no_answers_flag = False
        not_gen_flag = False
    
    pp=pprint.PrettyPrinter(indent=4)
    # question_list has a specific question in every language
    for question in lines:


        

        target, query, metadata, target_entity = main.dbpedia.get_query(question)
          

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            if(not_gen_flag):
                if(question_flag):
                        print("|------------------------------------------------------------------------------------------------------|")
                        print("|------------------------------------------------------------------------------------------------------|")
                        print question
                print("No query generated! :(")
            continue
        

        if target.startswith("?"):
            target = target[1:]
        if query:
            main.sparql.setQuery(query)
            main.sparql.setReturnFormat(main.JSON)
            results = main.sparql.query().convert()

            if not results["results"]["bindings"]:
                if(no_answers_flag):
                    if(question_flag):
                        print("|------------------------------------------------------------------------------------------------------|")
                        print("|------------------------------------------------------------------------------------------------------|")
                        print question
                    if(query_flag):
                        print query
                    print "No answer found :("
                continue

            


            query_results_dict_all_languages = results["results"]["bindings"]

            # if we received a string or a uri, the variable we want to print is Target
            if query_results_dict_all_languages[0][target]['type'] == 'typed-literal' or \
                query_results_dict_all_languages[0][target]['type'] == 'uri':
                # If we are receiving a string, keep everything
                query_results_dict = query_results_dict_all_languages
                # identifier of the entity we want
                uri_variable_name = target
            elif query_results_dict_all_languages[0][target]['type'] == 'literal':
                # Else, we are receiving  a normal label, only keep english results
                query_results_dict = [el for el in query_results_dict_all_languages if el[target]['xml:lang']=='en']
                # identifier of the entity we want
                uri_variable_name = str(target_entity[1:])


            
            # list of uris returned by query
            list_query_uris = [el[uri_variable_name]['value'] for el in query_results_dict]
            if(answered_flag):
                if(question_flag):
                    print("|------------------------------------------------------------------------------------------------------|")
                    print("|------------------------------------------------------------------------------------------------------|")
                    print question
                if(query_flag):
                    print query
                if(results_flag):
                    pp.pprint(results)
                if(answers_flag):
                    print("Answers: :)")
                    pp.pprint(list_query_uris)





def process_qald_questions(dataset_json, config_file, print_flag):

    question_flag = config_file['question']
    query_flag = config_file['query']
    results_flag =config_file['results']
    answers_flag = config_file['show_answers']
    answered_flag = config_file['answered']
    no_answers_flag = config_file['not_answered']
    not_gen_flag = config_file['not_generated']
    metrics_flag = config_file['metrics']
    write_flag = config_file['write']
    if not print_flag:
        question_flag = False
        query_flag = False
        results_flag = False
        answers_flag = False
        answered_flag = False
        no_answers_flag = False
        not_gen_flag = False
        metrics_flag = False
    
    pp=pprint.PrettyPrinter(indent=4)

    questions_json = dataset_json['questions']
    

    num_questions = len(questions_json)
    num_not_generated = 0
    num_no_answer = 0
    num_not_valid = 0

    global_precision = 0
    global_recall = 0

    questions_dict_answer = []
    questions_dict_no_answer = []
    questions_dict_not_generated = []
    



    # question_list has a specific question in every language
    for question_list in questions_json:
        # question_dict has question dictionary
        question_dict = [q for q in question_list['question'] if q['language']=='en'][0]
        # question is the question string
        question = question_dict['string']

        # the question has no answers
        if not question_list['answers']:
            num_not_valid += 1
            num_questions -= 1
            continue
        correct_answer_dict = question_list['answers'][0]

        
        target, query, metadata, target_entity = main.dbpedia.get_query(question)
        

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            if(not_gen_flag):
                if(question_flag):
                        print("|------------------------------------------------------------------------------------------------------|")
                        print("|------------------------------------------------------------------------------------------------------|")
                        print question
                print("No query generated! :(")
            num_not_generated += 1
            questions_dict_not_generated.append(question_list)
            continue

  

        if target.startswith("?"):
            target = target[1:]
        if query:
            main.sparql.setQuery(query)
            main.sparql.setReturnFormat(main.JSON)
            results = main.sparql.query().convert()

            if not results["results"]["bindings"]:
                if(no_answers_flag):
                    if(question_flag):
                        print("|------------------------------------------------------------------------------------------------------|")
                        print("|------------------------------------------------------------------------------------------------------|")
                        print question
                    if(query_flag):
                        print query
                    print "No answer found :("
                num_no_answer += 1
                questions_dict_no_answer.append(question_list)
                continue

            questions_dict_answer.append(question_list)

            
            if(answered_flag):
                if(question_flag):
                    print("|------------------------------------------------------------------------------------------------------|")
                    print("|------------------------------------------------------------------------------------------------------|")
                    print question
                if(query_flag):
                    print query
                if(results_flag):
                    pp.pprint(results)
            # Input the expected answers, and the answers we got, Output the precision and recall
            precision, recall = calculate_metrics(correct_answer_dict, results, target, target_entity, answers_flag)
            global_precision += precision
            global_recall += recall

            
            





    global_precision = float(global_precision) / num_questions
    global_recall = float(global_recall) / num_questions
    len(questions_dict_answer)
    try:
        f_measure_global = (2*global_precision*global_recall)/(global_precision+global_recall)
    except ZeroDivisionError:
        print("There are no correct answers")
        f_measure_global = 0
    num_questions_answered = len(questions_dict_answer)
    global_precision_answered = float(global_precision) / num_questions_answered
    global_recall_answered = float(global_recall) / num_questions_answered
    try:
        f_measure = (2*global_precision_answered*global_recall_answered)/(global_precision_answered+global_recall_answered)
    except ZeroDivisionError:
        print("There are no correct answers")
        f_measure = 0



    if (metrics_flag):
        print("Precision---------->"+str(global_precision))
        print("Recall------------->"+str(global_recall))
        print("F-measure---------->"+str(f_measure_global))
        print("F-measure Global--->"+str(f_measure_global))
        print("Number of not generated------>"+str(len(questions_dict_not_generated)))
        print("Number of no answer---------->"+str(len(questions_dict_no_answer)))
        print("Number of answered----------->"+str(len(questions_dict_answer)))
        print("Number of not valid---------->"+str(num_not_valid))
    
    metrics = {
        "precision": global_precision,
        "recall": global_recall,
        "f_measure" : f_measure,
        "f_measure_global": f_measure_global
    }
    if (write_flag):
        process_files.write_to_json_files(questions_dict_not_generated, questions_dict_no_answer, questions_dict_answer, metrics)






def calculate_metrics(correct_answer_dict, results, target, target_entity, answers_flag):
    answer_head_type = correct_answer_dict['head']['vars'][0]
    correct_results_dict = correct_answer_dict['results']['bindings']
    query_results_dict_all_languages = results["results"]["bindings"]

    # if we received a string or a uri, the variable we want to print is Target
    if query_results_dict_all_languages[0][target]['type'] == 'typed-literal' or \
        query_results_dict_all_languages[0][target]['type'] == 'uri':
        # If we are receiving a string, keep everything
        query_results_dict = query_results_dict_all_languages
        # identifier of the entity we want
        uri_variable_name = target
    elif query_results_dict_all_languages[0][target]['type'] == 'literal':
        # Else, we are receiving  a normal label, only keep english results
        query_results_dict = [el for el in query_results_dict_all_languages if el[target]['xml:lang']=='en']
        # identifier of the entity we want
        uri_variable_name = str(target_entity[1:])
    # label variable in the instances where the value returned is a literal (mistake)
    label_variable_name = target
    # correct values from json data
    correct_results_values = [el[answer_head_type]['value'] for el in correct_results_dict]
    # list of uris returned by query
    list_query_uris = [el[uri_variable_name]['value'] for el in query_results_dict]
    if(answers_flag):
        pp=pprint.PrettyPrinter(indent=4)
        print("Answers: :)")
        pp.pprint(list_query_uris)
    # list of labels returned by query
    list_query_labels = [el[label_variable_name]['value'] for el in query_results_dict]
    # number of correct answers
    number_correct_answers_uris = sum(el in correct_results_values for el in list_query_uris)
    number_correct_answers_labels = sum(el in correct_results_values for el in list_query_labels)
    # we use the type (uri vs label) that has the most correct values
    number_correct_answers = number_correct_answers_uris if number_correct_answers_uris>=number_correct_answers_labels else number_correct_answers_labels
    # number of answers in the gold standard
    number_gold_answers = len(correct_results_dict)
    # number of answers returned by the system
    number_system_answers = len(query_results_dict)
    precision = number_correct_answers/number_system_answers
    recall = number_correct_answers/number_gold_answers
    return precision, recall


