from html.parser import HTMLParser
from urllib.request import urlopen
from parsers.index_parser import IndexParser
from parsers.book_parser import BookParser
from parsers.chapter_parser import ChapterParser
import re
import os.path
import unicodedata

url_root = "https://en.wikisource.org"
base_url = url_root + "/wiki/Portal:Children%27s_literature"
data_path = os.path.join(os.getcwd(), '..', 'data')

def get_or_create_dir(path, dirname):
    full_path = os.path.join(path, dirname)
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        os.mkdir(full_path)
    return full_path

def make_path_safe(raw_path):
    return re.sub(r'[^a-zA-Z\d]', '_', raw_path)

def retrieve_html(url):
    with urlopen(url) as response:
        html = response.read()
        response.close()
        return str(html)


get_or_create_dir(data_path, "fulltext")

base_book_list = []

index_parser = IndexParser()
index_parser.feed(retrieve_html(base_url))
book_index_dict = index_parser.retrieve_result()

for age_group in book_index_dict.keys():
    book_tuples = book_index_dict[age_group]

    for book_tuple in book_tuples:
        base_book_list.append(book_tuple + (age_group,))

chaptered_book_list = [] # TODO find a word for this

#print(base_book_list)

print(len(base_book_list))
chaptered = 0

for book_tuple in base_book_list:
    # print(book_tuple)
    book_parser = BookParser(book_tuple[0])
    raw_html = retrieve_html(url_root + book_tuple[0])
    book_parser.feed(raw_html)
    chapter_list = book_parser.retrieve_chapter_urls()

    if len(chapter_list) > 0:
        chaptered += 1
    else:
        continue # TODO handle other book types

    book_name = make_path_safe(book_tuple[1])

    book_path = get_or_create_dir(os.path.join(data_path, "fulltext"), book_name)

    for chapter_tuple in chapter_list:
        chapter_html = retrieve_html(url_root + chapter_tuple[1])
        chapter_parser = ChapterParser()
        chapter_parser.feed(chapter_html)
        chapter_text = chapter_parser.retrieve_text().strip()

        chapter_name = make_path_safe('_'.join(chapter_tuple[0].split('/')[1:]))

        chapter_path = os.path.join(book_path, chapter_name + '.txt')

        with open(chapter_path, 'w') as file:
            file.write(unicodedata.normalize('NFKD', chapter_text).encode('ascii', 'ignore').decode("utf-8"))

