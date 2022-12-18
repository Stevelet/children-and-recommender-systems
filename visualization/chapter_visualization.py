import json
import util.path as path
import numpy as np
import matplotlib.pyplot as plt
import functools as t

data = json.load(open(path.data_root() / 'wikisource_sentiment.json'))

plot_data = []
for age_category, books in data.items():
    chapter_counts = sorted(map(lambda book: book['chapter_count'], books))
    plot_data.append((age_category, chapter_counts))

plot_data = sorted(plot_data, key=lambda tup: int(tup[0].replace('+', '')))
boxplot_data = [tup[1] for tup in plot_data]
label_data = [tup[0] for tup in plot_data]

print(plot_data)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
bp = ax.boxplot(boxplot_data, vert=0, patch_artist=True)

for median in bp['medians']:
    median.set(color='black',
               linewidth=1)

# x-axis labels
ax.set_yticklabels(label_data)

# Adding title
plt.ylabel('Age categories', fontweight='bold', fontsize=15)
plt.xlabel('Chapter counts', fontweight='bold', fontsize=15)

# show plot
plt.show()
