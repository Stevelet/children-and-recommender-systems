from html.parser import HTMLParser
import re


class BookParser(HTMLParser):
    def __init__(self, url_suffix):
        super().__init__()
        self.url_suffix = url_suffix
        self.chapter_urls = []
        self.poem = False
        self.disambiguation = []
        self.single_chapter_book = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        if tag == 'a' and "href" in attr_dict.keys() and self.url_suffix + '/' in attr_dict["href"]:
            chapter_tuple = (attr_dict["title"], attr_dict["href"])

            if chapter_tuple not in self.chapter_urls:
                self.chapter_urls.append(chapter_tuple)
        elif tag == 'div' and "class" in attr_dict.keys() and attr_dict["class"] == "poem":
            self.poem = True
        elif tag == "a" and "href" in attr_dict.keys():
            match = re.search(r'_\(.+\)', attr_dict["href"])
            if match is not None and attr_dict["href"] == str(self.url_suffix).split('#')[0] + match.group(0):
                self.disambiguation.append(attr_dict["href"])
        elif tag == "span" and "data-page-number" in attr_dict.keys():
            self.single_chapter_book = True

    def retrieve_chapter_urls(self):
        return self.chapter_urls
