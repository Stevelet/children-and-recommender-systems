import csv
import json


# Goodreads
def merge_goodreads():
    with open("data/goodreads.json", 'r') as f_j:
        with open("data/combined_dataset.csv", 'a', newline='') as f_c:
            writer = csv.writer(f_c)

            language_whitelist = ["eng", "en-GB", "en-US"]
            author_whitelist = ["Author", "Author and Illustrator", "Ghostwriter", "Author, Illustrator", "author/illustrator", "Author/Narrator", "Author/Illustrator", "Fictional Author", "Illustrator , Author", "author", "Author & Illustrator", "Author & Illustrator ", "Writer", "Original Author", "Author Illustrator", "original author", "Author and Photographer", "Writer/Illustrator", "Author / Illustrator", "Original author", "writer", "Author, Narrator", "Author and Drawings", "Auhor/Illustrator", "Writer & Illustrator", "Editor/Contributing Author", "author, illustrator", "Story and illustrations"]
            illustrator_whitelist = ["Illustrator", "-Illustrator", "Illustrations", "illustrator", "Author and Illustrator", "Colorist", "Ilustrator", "Illustration", "Illustrator ", "Author, Illustrator", "author/illustrator", "Translator, Illustrator", "Author/Illustrator", "Illustrator , Author", "Artist", "Illistrator", "Author & Illustrator", "Author & Illustrator ", "adaptor/illustrator", "Adaptor, Illustrator", "Cover Illustrator", "Illustartor", "Adaptor / Illustrator", "Illustrations  Provided by", "Illustrated by", "Translator and Illustrator", "Illsutrator", "Artist/Designer", "Illustrators", "Illustrator/Designer", "Colorer", "Cover Artist", "Cover Illustration", "IIustrator", "Adaptor and Illustrator", "Adapted and Illustrated by", "Author Illustrator", "cover art", "Cover Illustrations", "Interior Illustrator", "cover illustrator", "lllustrator", "Co-Illustrator", "penciller/ colorist", "cover", "Penciller", "Cover", "Illlustrator", "Colourist", "illustratar", "Retold & Illustrated by", "Illustrator/Adapter", "Illusrator", "illustrator - cover", "adapter/illustrator", "Cover Art", "Cover Design", "Writer/Illustrator", "Author / Illustrator", "Cover illustration", "Illustrator, Adaptor", "Author and Drawings", "Auhor/Illustrator", "Illustrato", "Writer & Illustrator", "Cover illustrator", "*Illustrator", "illustrations", "Illustraror", "Illustratoer", "cover artist", "author, illustrator", "Story and illustrations", "Illustrator, Translator", "Illustrator / Contributor", "-Illustrator Mariano Epelbaum", "Illustratir", "Illustator", "Illustrator/Adaptor", "Interior llustrator"]

            for row in f_j:
                j = json.loads(row)

                if j["isbn"] != "":
                    if j["language_code"] in language_whitelist:

                        authors = ""
                        illustrators = ""

                        for i in j["authors"]:
                            if i["role"] == "" or i["role"] in author_whitelist:
                                authors += i["author_id"]
                                authors += ";"
                            if i["role"] in illustrator_whitelist:
                                illustrators += i["author_id"]
                                illustrators += ";"

                        if authors != "":
                            authors = authors[:-1]
                        else:
                            authors = "NULL"

                        if illustrators != "":
                            illustrators = illustrators[:-1]
                        else:
                            illustrators = "NULL"

                        csv_row = [
                            j["isbn"] if j["isbn"] else "NULL",  # isbn
                            int((j["url"].removeprefix("https://www.goodreads.com/book/show/").split('.')[0].split('-')[0])),  # goodreads_id
                            "NULL",  # amazon_id
                            j["book_id"] if j["book_id"] else "NULL",  # book_id
                            j["title"] if j["title"] else "NULL",  # title
                            "NULL",  # series
                            authors,  # authors
                            illustrators,  # artists
                            j["publisher"] if j["publisher"] else "NULL",  # publisher
                            j["publication_year"] if j["publication_year"] else "NULL",  # publication_year
                            j["country_code"] if j["country_code"] else "NULL",  # publication_country
                            j["num_pages"] if j["num_pages"] else "NULL",  # number_of_pages
                            "NULL",  # number_of_chapters
                            "NULL",  # dimensions
                            "NULL",  # weight
                            "NULL",  # format
                            j["image_url"] if j["image_url"] else "NULL",  # cover_image
                            "NULL",  # full_text
                            "NULL",  # subject
                            j["description"] if j["description"] else "NULL",  # description
                            "NULL",  # interest_age
                            "NULL",  # recommended_age
                            "NULL",  # similar_books
                            "NULL",  # average_rating
                            j["ratings_count"] if j["ratings_count"] else "NULL",  # rating_count
                            j["text_reviews_count"] if j["text_reviews_count"] else "NULL"  # text_review_count
                        ]

                        try:
                            writer.writerow(csv_row)
                        except:
                            pass


# Kaggle
with open("data/kaggle.csv", 'r') as f:
    all_titles = []

    r = csv.reader(f)
    for row in r:
        all_titles.append(row[0])
        # print(row)

    print(all_titles)

    with open("data/combined_dataset.csv", 'r') as c:
        l = csv.reader(c)

        for x in l:
            if x[4] in all_titles:
                print(x[4])


def merge_all():
    merge_goodreads()
