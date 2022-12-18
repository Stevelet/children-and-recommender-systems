import json
import util.path as path
import numpy as np
import matplotlib.pyplot as plt
import functools as t

data = json.load(open(path.data_root() / 'wikisource_sentiment.json'))
emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
emotion_colors = ['green', 'red', 'yellow', 'blue', 'orange']

keys = sorted([int(key.replace('+', '')) for key in list(data.keys())])
plot_data = []
for i in range(len(keys)):
    key = keys[i]
    raw_key = str(key) + '+'

    sentiments = [list(item['chapter_sentiments'].values()) for item in data[raw_key]]
    unpacked_book_sentiments = [[[chapter[emotion] for emotion in emotions] for chapter in book] for book in sentiments]
    filtered_book_sentiments = list(filter(lambda b: len(b) > 0,
                                           [[chapter for chapter in book if sum(chapter) > 0] for book in
                                            unpacked_book_sentiments]))
    total_book_sentiment = [(len(book), t.reduce(lambda l, r: list(map(lambda l1, r1: l1 + r1, l, r)), book)) for book
                            in filtered_book_sentiments]
    average_book_sentiment = [list(map(lambda chapter: chapter / float(book[0]), book[1])) for book in
                              total_book_sentiment]

    average_category_sentiment = t.reduce(
        lambda l, r: list(map(lambda l1, r1: l1 + r1 / len(average_book_sentiment), l, r)), average_book_sentiment)
    plot_data.append(average_category_sentiment)

emotion_dict = {}
for category in plot_data:
    for index, sentiment in enumerate(category):
        emotion_dict.setdefault(emotions[index], []).append(sentiment)

print(emotion_dict)

# set width of bar
barWidth = 1.0 / (len(emotion_dict.keys()) + 1)
fig = plt.subplots(figsize=(12, 8))

# Set position of bar on X axis
barX = [np.arange(len(list(emotion_dict.values())[0]))]
for i in range(1, len(emotion_dict.keys())):
    barX.append([x + barWidth for x in barX[i - 1]])

for index, (key, value) in enumerate(emotion_dict.items()):
    plt.bar(barX[index], value, color=emotion_colors[index], width=barWidth,
            edgecolor='grey', label=key)

# Adding Xticks
plt.xlabel('Age categories', fontweight='bold', fontsize=15)
plt.ylabel('Average sentiment', fontweight='bold', fontsize=15)
plt.xticks([r + barWidth for r in range(len(list(emotion_dict.values())[0]))],
           keys)

plt.legend()
plt.show()
