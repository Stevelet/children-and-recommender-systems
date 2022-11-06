import os.path
import urllib.request
import gzip
import shutil
import csv
import sys
import time
import zipfile

start_time = 0
kaggle_url = "https://storage.googleapis.com/kaggle-data-sets/937330/2230126/compressed/children_books.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20221104%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221104T132812Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=56a238b2fa69b29fcefd2769d7f1c7a1c992f8f7c496de8889b6b90f29c47a79d7bbc6ccb29be0da192805d37c6973e651e447da69401fc745029f101e9ba64d7ad84da0da4d88c9c4dfc394cc7420ad9326639927f26e5db39378e6b2379d19f55c6e653931eb03e6e9879404d2130e7a8ba62a916ac508e4b58df5cb2449062ab682700be6e862464a9e011e90f4ae3651626e09377088ce68eb1ff628572da3eabf3cfb3fda3ea05a398206b76790e9dd38f02ebd10a7d6f88112d7370a27c6261c7c9d52e0e2bdae2aa3a1fd103da2c6e73e071ec5fe1cc698802bcc25bb8f96aed41caa7ca018f4a3461f6ca1ed258f911401430082f2ab0cf7aedf5d3b"
goodreads_url = "https://drive.google.com/uc?id=1R3wJPgyzEX9w6EI8_LmqLbpY4cIC9gw4&confirm=t&uuid=e347bf6e-fbf4-48b0-a732-70c0309e58a2&at=ALAFpqzaZEeR0vKTgxLid4jqSb6A:1667130831307"
openlibrary_url = "https://openlibrary.org/data/ol_dump_latest.txt.gz"


def initialize():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.isfile("data/combined_dataset.csv"):
        with open("data/combined_dataset.csv", 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(["isbn", "goodreads_id", "amazon_id", "book_id", "title", "series", "authors", "artists", "publisher", "publication_year", "publication_country", "number_of_pages", "number_of_chapters", "dimensions", "weight", "format", "cover_image", "full_text", "subject", "description", "interest_age", "recommended_age", "similar_books", "average_rating", "rating_count", "text_review_count"])


def download_zip(source_url, source_name, target_name, data_extension):
    if not os.path.isfile("data/"+target_name+"."+data_extension):
        # Download file
        print("downloading "+target_name+"...")
        urllib.request.urlretrieve(source_url, "data/"+target_name+"_source.zip", show_progress)

        # Extract file
        print("\nextracting " + target_name + "...")
        with zipfile.ZipFile("data/"+target_name+"_source.zip") as zip_ref:
            zip_ref.extractall("data")

        # Finish
        os.remove("data/"+target_name+"_source.zip")
        os.rename("data/"+source_name+"."+data_extension, "data/"+target_name+"."+data_extension)
        print(target_name+" complete\n")


def download_gz(source_url, target_name, data_extension):
    if not os.path.isfile("data/"+target_name+"."+data_extension):
        # Download file
        print("downloading "+target_name+"...")
        urllib.request.urlretrieve(source_url, "data/" + target_name + "_source."+data_extension+".gz", show_progress)

        # Extract file
        print("\nextracting " + target_name + "...")
        with gzip.open("data/" + target_name + "_source."+data_extension+".gz", 'rb') as f_in:
            with open("data/" + target_name + "."+data_extension, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Finish
        os.remove("data/" + target_name + "_source."+data_extension+".gz")
        print(target_name+" complete\n")


def show_progress(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time + 0.1
    progress_size = int(count * block_size)
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d seconds passed" % (percent, progress_size / (1024 * 1024), duration))
    sys.stdout.flush()


def download_all():
    initialize()
    download_zip(kaggle_url, "children_books", "kaggle", "csv")
    download_gz(goodreads_url, "goodreads", "json")
    download_gz(openlibrary_url, "openlibrary", "txt")
