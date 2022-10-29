import os.path
import urllib.request
import zipfile
import gzip
import shutil

kaggle_link = "https://storage.googleapis.com/kaggle-data-sets/937330/2230126/compressed/children_books.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20221029%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221029T120345Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=2affdf629c540913ba06f0dd60eea1465824482def268f8d678904da8864632601f8f0e607ce69ff25bcab828384c56570d3f494fb48262072bd8886bed2a5e81fd3a5ae2baf6d3b8b32aa05d55469e92be1984722245559d617efe541881e695672195ba4e7cf086d764479c65a4a400a382cbe52bf162bf4515d2967047496b61bb061a5e40ddb38ecff1382b7ce64d14bb9c5c47081a54ac4111e7aea828ac1f50b799a0f9079e9018552526091be35ab3da5edf36041f22eb0664aae04e53c8d390fd360bcf91e77ec0ce1fb47bcaa42e547a230e43d734f18596c61bf04951e204849f53ed38dedf2c14baa2fcf893f03eca953340f8bff4dcf4b3008ca"
goodreads_link = "https://drive.google.com/u/0/uc?id=1LXpK1UfqtP89H1tYy0pBGHjYk8IhigUK&export=download&confirm=t&uuid=4a00c5c0-f731-4618-abdf-80bc239208ad&at=ALAFpqyOwJtCbYMNhNGAyxQGA7ep:1667073539251"

if not os.path.isfile("data/kaggle.csv"):
    print("downloading kaggle...")
    urllib.request.urlretrieve(kaggle_link, "data/kaggle_source.zip")
    with zipfile.ZipFile("data/kaggle_source.zip", 'r') as zip_ref:
        zip_ref.extractall("data")
    os.remove("data/kaggle_source.zip")
    os.rename("data/children_books.csv", "data/kaggle.csv")
    print("kaggle complete")

if not os.path.isfile("data/goodreads.json"):
    print("downloading goodreads...")
    urllib.request.urlretrieve(goodreads_link, "data/goodreads_source.json.gz")
    with gzip.open("data/goodreads_source.json.gz", 'rb') as f_in:
        with open("data/goodreads.json", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove("data/goodreads_source.json.gz")
    print("goodreads complete")

