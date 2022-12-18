import json
from math import ceil

import util.path as path
import numpy as np
import matplotlib.pyplot as plt
import functools as t

data = json.load(open(path.data_root() / 'wikisource_sentiment.json'))

emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
emotion_colors = ['green', 'red', 'yellow', 'blue', 'orange']
emotion_color_map = dict(zip(emotions, emotion_colors))

median_books = {}
for age_category, books in data.items():
    book_options = sorted(map(lambda book: (book['chapter_count'], book), books), key=lambda tup: tup[0])
    median_book = book_options[ceil(len(book_options) / 2.0)]
    median_books[age_category] = (len(books), median_book)

representation_book = sorted([tup for tup in median_books.items()], key=lambda tup: tup[1][0])[-1][1][1]

book_chapters = representation_book[1]['chapter_sentiments']
chapter_count = representation_book[0]

emotion_map = {emotion: [] for emotion in emotions}

for chapter_index in range(chapter_count):
    for emotion in emotions:
        emotion_map[emotion].append(book_chapters[str(chapter_index)][emotion])

for emotion in emotions:

    y_axis = emotion_map[emotion]
    print(emotion)
    print(y_axis[0])
    print(y_axis[-1])
    x_axis = list(range(1, chapter_count + 1))
    plt.plot(x_axis, y_axis, label=emotion, color=emotion_color_map[emotion])

plt.ylabel('Sentiment distribution', fontweight='bold', fontsize=15)
plt.xlabel('Chapter numbers', fontweight='bold', fontsize=15)
plt.title(representation_book[1]['title'] + ' by ' + representation_book[1]['author'])

plt.legend()
plt.show()
