import csv

csv.register_dialect("excel", delimiter=";")
with open("training.csv", "r") as file:
    contents = csv.DictReader(file, dialect="excel")
    rowno = 0
    results = {}
    for row in contents:
        data = dict(row)
        results.setdefault(data["GUO - BvD ID number"], dict())
        results[data["GUO - BvD ID number"]].setdefault(data["Country ISO code"], 0)
        results[data["GUO - BvD ID number"]][data["Country ISO code"]] += 1
        rowno += 1
    file.close()

for guo, countries in results.items():
    print(guo, countries)