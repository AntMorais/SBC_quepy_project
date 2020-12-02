import quepy.nltktagger as ntag
import nltk
import json
import sys


def simple_tag_words(string):
    text = nltk.word_tokenize(string)
    tags = nltk.pos_tag(text)
    return tags


def tag_words(string):
    words = ntag.run_nltktagger(string)
    print(words)