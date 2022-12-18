import json
import os
from functools import reduce
import util.path as path
import util.name_classifier as name_classifier
import time
from util.dict_util import merge_dictionary

basic_pronouns = ['he', 'him', 'himself', 'his', 'she', 'her', 'hers', 'herself']


# Dictionary source: https://github.com/dwyl/english-words

def analyse_line_names(line):
    words = ' '.join(filter(lambda word: word.isalpha(), line.split(' ')))

    return [name[0] for name in name_classifier.extract_person_names(words)]


def analyse_line_pronouns(line):
    words = filter(lambda w: w.isalpha(), line.split(' '))

    pronoun_map = {key: 0 for key in basic_pronouns}

    for word in words:
        low = word.lower()
        if low in basic_pronouns:
            pronoun_map[low] += 1

    return pronoun_map


def analyse_chapter_names_and_pronouns(chapter_tuple):
    index, chapter = chapter_tuple

    with open(chapter) as file:
        lines = file.read().split('\n')
        names = [item for sublist in list(map(analyse_line_names, lines)) for item in sublist]
        pronouns = reduce(merge_dictionary, list(map(analyse_line_pronouns, lines)))

    return index, names, pronouns


def analyse_book_names_and_pronouns(book):
    chapters = book['chapters']
    chapter_person_names = {}
    chapter_pronouns = {}
    for chapter_tuple in enumerate(chapters):
        mapped_chapter_tuple = analyse_chapter_names_and_pronouns(chapter_tuple)
        chapter_person_names[str(mapped_chapter_tuple[0])] = mapped_chapter_tuple[1]
        chapter_pronouns[str(mapped_chapter_tuple[0])] = mapped_chapter_tuple[2]
        print('#', end='')
    book['chapter_person_names'] = chapter_person_names
    book['chapter_pronouns'] = chapter_pronouns
    return book


def analyse_book_list_names_and_pronouns(book_list_path):
    with open(book_list_path, 'r') as file:
        book_list = json.load(file)

    print('Starting book analysis')
    total_books = len(book_list)
    completed_books = 0
    start_time = time.time()
    for book in book_list:
        safe_title = str(path.make_path_safe(book['title'])) + '.json'
        file_name = path.data_root() / 'gender' / safe_title

        if os.path.exists(file_name):
            completed_books += 1
            print('Skipped : ' + str(completed_books) + '/' + str(total_books))
            continue

        mapped_book = analyse_book_names_and_pronouns(book)
        completed_books += 1
        print('')
        print(str(completed_books) + '/' + str(total_books) + ' after ' + str(time.time() - start_time) + " seconds")

        with open(file_name, 'w') as file:
            file.write(json.dumps(mapped_book))


analyse_book_list_names_and_pronouns(path.data_root() / 'wikisource.json')
