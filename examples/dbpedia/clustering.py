import quepy.nltktagger as ntag
import nltk
import json
import sys
import process_files


def simple_tag_words(string):
    text = nltk.word_tokenize(string)
    tags = nltk.pos_tag(text)
    return tags


def tag_words(string):
    words = ntag.run_nltktagger(string)
    print(words)


def group_questions(config_file, print_flag):

    group_flag = config_file['group']
    if not group_flag:
        return 
    group_number = config_file['group_number']
    print_categories = config_file['categories']
    if not print_flag:
        print_categories = False
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
        tagged_words = simple_tag_words(question)
        first_word = [tagged_words[i][0] for i in range(group_number)]
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

    if print_categories:
        import pprint
        pp=pprint.PrettyPrinter(indent=4)
        sorted_categories = sorted(category_summary['category_list'], key=lambda k: len(k['question_list'])) 
        pp.pprint(sorted_categories)
        