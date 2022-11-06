from urllib.request import urlopen
from parsers.index_parser import IndexParser
from parsers.book_parser import BookParser
from parsers.chapter_parser import ChapterParser
import re
import os.path
import unicodedata

url_root = "https://en.wikisource.org"
base_url = url_root + "/wiki/Portal:Children%27s_literature"


def get_or_create_dir(path, dirname):
    """
    Create directory at path or return path if it already exists.

    :param path: Root dir for the new directory
    :param dirname: New directory name
    :return: Full path to new directory
    """
    full_path = os.path.join(path, dirname)
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        os.mkdir(full_path)
    return full_path


def make_path_safe(raw_path):
    """
    Parse string to path string for file storage.

    :param raw_path: Path
    :return: Path without special characters
    """
    return re.sub(r'[^a-zA-Z\d()]', '_', raw_path)


def retrieve_html(url):
    """
    Retrieve the html found at the given url and parse to string.

    :param url: Url to GET
    :return: The body html as a string
    """
    with urlopen(url) as response:
        html = response.read()
        response.close()
        return str(html)

def clean_hexadecimal(raw_str, remove=True):
    """
    Convert hexadecimal strings to their corresponding character or remove them entirely.

    :param raw_str: String to clean
    :param remove: If true, delete occurrences. If false, Replace with corresponding character
    :return: String without hexadecimal characters
    """
    cleaned_string = raw_str
    matches = list(set(re.findall(r'\\x[a-f0-9]{2}', raw_str)))
    for match in matches:
        cleaned_string = cleaned_string.replace(match, '' if remove else chr(int("".join(match[2:4]), 16)))
    return cleaned_string

def sanitize_file(file_path):
    """
    Remove garbage from files.

    :param file_path: File to sanitize
    :return: file_path
    """
    lines = []
    old_lines = []
    with open(file_path, encoding='UTF-8') as file:
        for line in file:
            old_lines.append(line)
            clean_line = clean_hexadecimal(line)
            lines.append(clean_line.replace('\\', ''))
    lines = '\n'.join(lines)
    old_lines = '\n'.join(old_lines)

    if old_lines == lines:
        return file_path

    with open(file_path, "w") as file:
        file.write(lines)

    return file_path


def retrieve_book_details(data_path):
    """
    Scrape the index page of wikisource and all pages following from it to
    retrieve details about the books in public domain.

    :param data_path: Path to the data directory
    :return: List of tuples containing data about the books found
    """
    get_or_create_dir(data_path, "fulltext")

    base_book_list = []

    index_parser = IndexParser()
    index_parser.feed(retrieve_html(base_url))
    book_index_dict = index_parser.retrieve_result()

    for age_group in book_index_dict.keys():
        book_tuples = book_index_dict[age_group]

        for book_tuple in book_tuples:
            base_book_list.append(book_tuple + (age_group,))

    final_book_list = []  # TODO find a word for this

    parsed_count = 0

    for book_tuple in base_book_list:
        # print(book_tuple)
        book_parser = BookParser(book_tuple[0])
        raw_html = retrieve_html(url_root + book_tuple[0])
        book_parser.feed(raw_html)
        chapter_list = book_parser.retrieve_chapter_urls()

        if len(chapter_list) > 0:
            parsed_count += 1
        else:
            continue  # TODO handle other book types

        book_name = make_path_safe(book_tuple[1])

        book_path = get_or_create_dir(os.path.join(data_path, "fulltext"), book_name)

        full_tuple = book_tuple + (len(chapter_list), book_path.replace(data_path, ''), chapter_list)

        final_book_list.append(full_tuple)

    return final_book_list


def store_book_details(data_path, book_tuples):
    """
    Store the data about the books in the wikisource csv file.

    :param data_path: Path to the data directory
    :param book_tuples: List of tuples containing the information about the scraped books
    """
    headers = "url,title,author,publishing_year,recommended_age,chapter_count,full_text_root_path"
    csv_string = headers + '\n'

    for book_tuple in book_tuples:
        part = ""
        for entry in book_tuple[:-1]:
            part += str(entry).replace(',', ';') + ','
        part = part[:-1] + '\n'
        csv_string += part

    with open(os.path.join(data_path, 'wikisource.csv'), 'w') as file:
        file.write(csv_string)


def store_book_chapters(data_path, book_tuples):
    """
    Store the chapters found during book parsing to files

    :param data_path: Path to the data directory
    :param book_tuples: List of tuples containing book details and chapter urls
    :return:
    """
    chapter_matrix = []
    for book_tuple in book_tuples:
        book_path = data_path + book_tuple[6]
        chapter_list = []

        for chapter_tuple in book_tuple[7]:
            chapter_name = make_path_safe('_'.join(chapter_tuple[0].split('/')[1:]))

            chapter_path = os.path.join(book_path, chapter_name + '.txt')

            chapter_list.append(chapter_path)

            if os.path.exists(chapter_path):
                continue

            chapter_html = retrieve_html(url_root + chapter_tuple[1])
            chapter_parser = ChapterParser()
            chapter_parser.feed(chapter_html)
            chapter_text = chapter_parser.retrieve_text().strip()

            with open(chapter_path, 'w') as file:
                # noinspection SpellCheckingInspection
                file.write(unicodedata.normalize('NFKD', chapter_text).encode('ascii', 'ignore').decode("utf-8"))
        chapter_matrix.append(chapter_list)
    return chapter_matrix


def download_wikisource(data_path):
    """
    Download as many of the wikisource books as possible.

    :param data_path: Path to the data directory
    :return: A list of tuples corresponding to the csv file that is generated
    """
    book_details = retrieve_book_details(data_path)
    store_book_details(data_path, book_details)
    chapter_matrix = store_book_chapters(data_path, book_details)
    for chapter_list in chapter_matrix:
        for chapter_path in chapter_list:
            sanitize_file(chapter_path)
    return book_details


# Example of call
local_data_path = os.path.join(os.getcwd(), '..', 'data')
# download_wikisource(local_data_path)
