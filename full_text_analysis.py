import nltk
import pandas as pd
import text2emotion as te
import os

nltk.download('omw-1.4')

df = pd.read_csv('./data/wikisource.csv')

for index, row in df.iterrows():
    root = row['full_text_root_path']
    files = os.listdir(os.getcwd() + '/data' + root)
    print(files)
