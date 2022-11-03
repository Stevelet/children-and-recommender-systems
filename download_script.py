import os.path
import urllib.request
import zipfile
import gzip
import shutil

kaggle_url = "https://storage.googleapis.com/kaggle-data-sets/937330/2230126/compressed/children_books.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20221101%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221101T131034Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=86962516e4df5f6b1409d9e14bf81ea9f5d6be3958d6ad525a656c3522c4f89144d699e64de037fef0829a067f11851896e1ce4e3da2b026f49687c0ea089dee1e0f1cba6f8bad0f759beb255eb9b3a19739696eed9f3ebbbd07e16cd24314ede9918584cc18f41be05209457e99e99a965c72e3ed81286234de66605ccbb2b083dc86ff0a4be68f55c1064bf469b8694c8025928b0e9ecb50ace3ab287091ab74f18bd51df042aae52a518d3240a878d453b93f7baff0055ade65a30a8fef08383077cf6f139d005b4a866f67032043ae46e1aad7c961aa2fdcec68107b94f8b5515933c88537fdf8e0b3c31a00dcef2bb9cfb79f9154d07e76dd39dc68c2a4"
goodreads_url = "https://drive.google.com/uc?id=1R3wJPgyzEX9w6EI8_LmqLbpY4cIC9gw4&confirm=t&uuid=e347bf6e-fbf4-48b0-a732-70c0309e58a2&at=ALAFpqzaZEeR0vKTgxLid4jqSb6A:1667130831307"
openlibrary_url = "https://openlibrary.org/data/ol_dump_latest.txt.gz"


def download_zip(source_url, source_name, target_name, data_extension):
    if not os.path.isfile("data/"+target_name+"."+data_extension):
        print("downloading "+target_name+"...")
        urllib.request.urlretrieve(source_url, "data/"+target_name+"_source.zip")
        print("extracting " + target_name + "...")
        with zipfile.ZipFile("data/"+target_name+"_source.zip", 'r') as zip_ref:
            zip_ref.extractall("data")
        os.remove("data/"+target_name+"_source.zip")
        os.rename("data/"+source_name+"."+data_extension, "data/"+target_name+"."+data_extension)
        print(target_name+" complete\n")


def download_gz(source_url, target_name, data_extension):
    if not os.path.isfile("data/"+target_name+"."+data_extension):
        print("downloading "+target_name+"...")
        urllib.request.urlretrieve(source_url, "data/" + target_name + "_source."+data_extension+".gz")
        print("extracting " + target_name + "...")
        with gzip.open("data/" + target_name + "_source."+data_extension+".gz", 'rb') as f_in:
            with open("data/" + target_name + "."+data_extension, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove("data/" + target_name + "_source."+data_extension+".gz")
        print(target_name+" complete\n")


download_zip(kaggle_url, "children_books", "kaggle", "csv")
download_gz(goodreads_url, "goodreads", "json")
download_gz(openlibrary_url, "openlibrary", "txt")
