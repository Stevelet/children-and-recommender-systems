import csv
import json

# # Kaggle
# with open("data/kaggle.csv", 'r') as f:
#     r = csv.reader(f)
#     for row in r:
#         print(row)
#     f.close()

# Goodreads
with open("data/goodreads.json", 'r') as f_j:
    with open("data/combined_dataset.csv", 'a', newline='') as f_c:
        writer = csv.writer(f_c)

        breaker = 0
        language_whitelist = ["eng", "en-GB", "en-US"]

        for row in f_j:
            breaker += 1
            if breaker == 100:
                break

            j = json.loads(row)

            if j["isbn"] != "":
                if j["language_code"] in language_whitelist:
                    writer.writerow([j["isbn"]])
                    print(j)
