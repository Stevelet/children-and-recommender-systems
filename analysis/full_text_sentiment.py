import json
import sys

import nltk

from download_script import show_progress
from util import path
from multiprocessing import pool
import text2emotion as te
import time

nltk.download('omw-1.4')
threadpool = pool.ThreadPool()

progress_map = {}


def analyse_chapter_sentiment(chapter_tuple):
    index, chapter = chapter_tuple
    success = False
    slept_for = 1
    with open(chapter) as file:
        while success is not True:
            try:
                chapter_sentiment = te.get_emotion(file.read())
                success = True
            except:
                time.sleep(slept_for)
                slept_for += 1
                if slept_for > 60:
                    print(slept_for)


    return index, chapter_sentiment


def analyse_book_sentiment(book):
    chapters = book['chapters']
    chapter_sentiments = {}
    for chapter_tuple in enumerate(chapters):
        mapped_chapter_tuple = analyse_chapter_sentiment(chapter_tuple)
        chapter_sentiments[str(mapped_chapter_tuple[0])] = mapped_chapter_tuple[1]
    book['chapter_sentiments'] = chapter_sentiments
    return book


def analyse_book_list_sentiment(book_list_path):
    with open(book_list_path, 'r') as file:
        book_list = json.load(file)

    age_map = {}
    print('Starting book analysis')
    for mapped_book in threadpool.imap_unordered(analyse_book_sentiment, book_list):
        if mapped_book['recommended_age'] not in age_map:
            age_map[mapped_book['recommended_age']] = []
        age_map[mapped_book['recommended_age']].append(mapped_book)

    with open(path.data_root() / 'wikisource_sentiment.json', 'w') as file:
        file.write(json.dumps(age_map))


analyse_book_list_sentiment(path.data_root() / 'wikisource.json')
