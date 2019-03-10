import csv

with open("data3.csv", "r") as file:
    contents = csv.DictReader(file, dialect="excel")

    results = {}
    for row in contents:
        data = dict(row)