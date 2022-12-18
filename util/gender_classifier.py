import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import matplotlib as mlp
from util.path import data_root
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

mlp.use("TKAgg")

mlp.rcParams.update({'font.family': "Open Sans", 'font.size': 16})

names = pd.read_csv(data_root() / "NationalNames.csv", dtype={'Count': np.int32})
names = names.fillna(0)

namechart = names.groupby(['Name', 'Gender'], as_index=False)['Count'].sum()

namechartdiff = namechart.reset_index().pivot('Name', 'Gender', 'Count')
namechartdiff = namechartdiff.fillna(0)
namechartdiff["Mpercent"] = ((namechartdiff["M"] - namechartdiff["F"]) / (namechartdiff["M"] + namechartdiff["F"]))
namechartdiff['gender'] = np.where(namechartdiff['Mpercent'] > 0.001, 'male', 'female')

char_vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
X = char_vectorizer.fit_transform(namechartdiff.index)
X = X.tocsc()
y = (namechartdiff.gender == 'male').values.astype(np.int)

itrain, itest = train_test_split(range(namechartdiff.shape[0]), train_size=0.7)
mask = np.ones(namechartdiff.shape[0], dtype='int')
mask[itrain] = 1
mask[itest] = 0
mask = (mask == 1)

Xtrainthis = X[mask]
Ytrainthis = y[mask]
Xtestthis = X[~mask]
Ytestthis = y[~mask]
clf = MultinomialNB(alpha=1)
clf.fit(Xtrainthis, Ytrainthis)

training_accuracy = clf.score(Xtrainthis, Ytrainthis)
test_accuracy = clf.score(Xtestthis, Ytestthis)


def lookup(x):
    str(x)
    new = char_vectorizer.transform([x])
    y_pred = clf.predict(new)
    return 'M' if (y_pred == 1) else 'F'
