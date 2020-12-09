import json
import sys
import process_files
import main
import clustering

dataset_json = json.load(open("data/qald-6-train-multilingual.json"))



def process_questions():

    questions_json = dataset_json['questions']
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
    process_files.write_to_json_files(questions_dict_not_generated, questions_dict_no_answer, questions_dict_answer, metrics)





if __name__ == "__main__":
    process_questions()
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
        first_word = tagged_words[0][0]
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



