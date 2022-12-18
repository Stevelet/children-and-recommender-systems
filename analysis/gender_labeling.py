import json
import os

import util.path as path
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from util.dict_util import merge_dictionary
import util.gender_classifier as gc

directory = path.data_root() / 'gender'

pronoun_map = {'he': 'male', 'him': 'male', 'himself': 'male', 'his': 'male', 'she': 'female', 'her': 'female',
               'hers': 'female', 'herself': 'female'}

book = json.load(open(path.data_root() / 'gender' / 'Through_the_Looking_Glass__and_What_Alice_Found_There.json'))

names = {'M': 0, 'F': 0}
name_genders = {}

for key in book['chapter_person_names'].keys():
    chapter_names = book['chapter_person_names'][key]
    for name in chapter_names:
        if name not in name_genders.keys():
            name_genders[name] = gc.lookup(name)
        names[name_genders[name]] += 1

pronoun_genders = {'male': 0, 'female': 0}

for key in book['chapter_pronouns'].keys():
    chapter_pronouns = book['chapter_pronouns'][key]
    for pronoun in chapter_pronouns.keys():
        pronoun_genders[pronoun_map[pronoun]] += 1

file_name = path.make_path_safe(book['title']) + '.json'
with open(path.data_root() / 'gender_breakdown' / file_name, 'w+') as file:
    st = json.dumps({'title': book['title'], 'pronoun_genders': pronoun_genders, 'names': names, 'name_genders': name_genders})
    file.write(st)