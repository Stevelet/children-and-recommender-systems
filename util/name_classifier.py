# -*- coding: utf-8 -*-

from nltk.tag import StanfordNERTagger
import nltk

import os

os.environ['JAVAHOME'] = 'C:/Program Files/Java/jre1.8.0_351/bin/java.exe'

# Add the jar and model via their path (instead of setting environment variables):
jar = 'C:/Users/stijn/PycharmProjects/children-and-recommender-systems/data/sanford-ner/stanford-ner.jar'
model = 'C:/Users/stijn/PycharmProjects/children-and-recommender-systems/data/sanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'

st = StanfordNERTagger(model, jar, encoding='utf8')


def extract_person_names(text):
    names = []
    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1] == 'PERSON':
                names.append(tag)
    return names