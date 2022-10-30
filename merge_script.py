import csv
import json

# # Kaggle
# with open("data/kaggle.csv", 'r') as f:
#     r = csv.reader(f)
#     for row in r:
#         print(row)
#     f.close()

# Goodreads
with open("data/goodreads.json") as f:
    # breaker = 1
    language_whitelist = ["", "eng", "en-GB", "en-US"]

    no_lang = 0
    eng = 0
    en_GB = 0
    en_US = 0

    for row in f:
        # breaker += 1
        # if breaker == 100:
        #     break

        j = json.loads(row)

        if j["isbn"] != "":
            if j["language_code"] in language_whitelist:
                if j["language_code"] == "":
                    no_lang += 1
                if j["language_code"] == "eng":
                    eng += 1
                if j["language_code"] == "en-GB":
                    en_GB += 1
                if j["language_code"] == "en-US":
                    en_US += 1

    print(no_lang)
    print(eng)
    print(en_GB)
    print(en_US)
    f.close()
