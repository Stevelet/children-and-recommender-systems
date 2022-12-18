import sqlite3
from util import path

def create_connection():
    conn = sqlite3.connect(path.data_root() / "wikisource.db")

    cursor = conn.cursor()

    res = cursor.execute("SELECT name FROM sqlite_master")
    tables = list(map(lambda t: t[0], res.fetchall()))

    if 'book' not in tables:
        cursor.execute(
            "CREATE TABLE book(id, url,title,author,publishing_year,recommended_age,chapter_count,full_text_root_path)")

    if 'chapter' not in tables:
        cursor.execute("CREATE TABLE chapter(id, book_id, word_count, path)")

    if 'sentiment' not in tables:
        cursor.execute("CREATE TABLE sentiment(chapter_id, angry, fear, happy, sad, surprise)")

    return conn, cursor