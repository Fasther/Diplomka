import csv

csv.register_dialect("excel", delimiter=";")
print("Getting and sorting data...")
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
print("Getting counts...")
final_data = []

for guo, countries in results.items():
    k = list(countries.keys())
    v = list(countries.values())
    country_iso = k[v.index(max(v))]
    temp_data = dict({"GUO": guo, "Country ISO code": country_iso})
    final_data.append(temp_data)
    #
print("Writing data...")

with open("result_guo.csv", "w", newline='') as result_file:
    writer = csv.DictWriter(result_file, fieldnames=["GUO", "Country ISO code"], dialect="excel")
    writer.writeheader()
    writer.writerows(final_data)

print("Work done!")