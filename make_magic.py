import csv


def make

csv.register_dialect("excel", delimiter=";")

with open("training.csv", "r") as file:
    contents = csv.DictReader(file, dialect="excel")

    total_revenue = 0
    results = {}


    GUO = ""
    row_no = 0
    temp_total_revenue = 0
    temp_countries_revenue = {}
    temp_countries_cctb_revenue = {}
    for row in contents:
        data = dict(row)

        if row_no == 0:
            GUO = data["GUO - BvD ID number"]
        row_no += 1
        print("Working on GUO: {}".format(data["GUO - BvD ID number"]))
        if GUO == data["GUO - BvD ID number"]:
            temp_total_revenue += int(data["Result OP Revenue"])
            temp_countries_revenue.setdefault(data["Country ISO code"], 0)
            temp_countries_revenue[data["Country ISO code"]] += int(data["Result OP Revenue"])
        else:
            print("Total revenue is: {}".format(temp_total_revenue))
            for country, value in temp_countries_revenue.items():
                print(country, value)
            break
            GUO = data["GUO - BvD ID number"]
            temp_total_revenue = 0

    file.close()

