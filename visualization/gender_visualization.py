import json

import matplotlib.pyplot as plt
import numpy as np

import util.path as path

book = json.load(
    open(path.data_root() / 'gender_breakdown' / 'Through_the_Looking_Glass__and_What_Alice_Found_There.json', 'r'))

def draw_pronouns():
    plt.pie(list(book['pronoun_genders'].values()), labels=list(book['pronoun_genders'].keys()),
            colors=['blue', 'orange'])
    plt.suptitle(book['title'])
    plt.show()

def draw_names():
    plt.pie(list(book['names'].values()), labels=[n + "ale" if n == 'M' else n + 'emale' for n in list(book['names'].keys())],
            colors=['blue', 'orange'])
    plt.suptitle(book['title'])
    plt.show()

draw_names()