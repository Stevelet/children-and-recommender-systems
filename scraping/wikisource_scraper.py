from html.parser import HTMLParser
from urllib.request import urlopen
from parsers.index_parser import IndexParser

url_root = "https://en.wikisource.org"
base_url = url_root + "/wiki/Portal:Children%27s_literature"


def retrieve_html(url):
    with urlopen(url) as response:
        html = response.read()
        response.close()
        return html


index_parser = IndexParser()
index_parser.feed(str(retrieve_html(base_url)))
print(index_parser.retrieve_result())

