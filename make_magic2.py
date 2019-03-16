import csv

open_file = "data4.csv"
write_file = "result_datafactor.csv"


def set_temp_guo_data():
    guo_temp_data.setdefault(data["Country ISO code"],
                             dict({"Revenue": 0, "Empl": 0, "Assets": 0, "PL_before": 0, "PL_after": 0}))
    guo_temp_data[data["Country ISO code"]]["Revenue"] += int(data["Result OP Revenue"])
    guo_temp_data[data["Country ISO code"]]["Empl"] += int(data["Result - EMPl"])
    guo_temp_data[data["Country ISO code"]]["Assets"] += int(data["Result - assets"])
    guo_temp_data[data["Country ISO code"]]["PL_before"] += int(data["Result P/L"])
    guo_temp_data[data["Country ISO code"]]["E_factor"] = int(data["E Faktor"])


def get_results():
    total_temp_revenue = 0
    total_temp_empl = 0
    total_temp_assets = 0
    total_temp_pl = 0
    total_temp_e_factor = 0

    check_sum_after_cctb = 0
    check_sum_after_data = 0

    for country in guo_temp_data:
        total_temp_revenue += guo_temp_data[country]["Revenue"]
        total_temp_empl += guo_temp_data[country]["Empl"]
        total_temp_assets += guo_temp_data[country]["Assets"]
        total_temp_pl += guo_temp_data[country]["PL_before"]
        total_temp_e_factor += guo_temp_data[country]["E_factor"]

    # calculate CCTB

    for country in guo_temp_data:
        guo_temp_data[country]["PL_after"] = (
                (((1 / 3) * (guo_temp_data[country]["Revenue"] / total_temp_revenue)) + (
                        (1 / 3) * (guo_temp_data[country]["Empl"] / total_temp_empl)) + (
                         (1 / 3) * (guo_temp_data[country]["Assets"] / total_temp_assets))) * total_temp_pl)
        check_sum_after_cctb += guo_temp_data[country]["PL_after"]

    # calculate ratio
    ratio = 100 / total_temp_e_factor

    # calculate data factor
    for country in guo_temp_data:
        guo_temp_data[country]["E_factor_after"] = (
                (((1 / 4) * (guo_temp_data[country]["Revenue"] / total_temp_revenue)) + (
                        (1 / 4) * (guo_temp_data[country]["Empl"] / total_temp_empl)) + (
                         (1 / 4) * (guo_temp_data[country]["Assets"] / total_temp_assets)) +
                 (1 / 4) * (guo_temp_data[country]["E_factor"] * ratio / 100)) * total_temp_pl)
        check_sum_after_data += guo_temp_data[country]["E_factor_after"]

    print("= After: {0:>10} -- Data: {2:>10} -- Before: {1:>10}".format(int(check_sum_after_cctb), total_temp_pl,
                                                                        int(check_sum_after_data)))

    if abs((float(check_sum_after_cctb) - float(total_temp_pl))) > 2:
        print("** We have error here!")
        raise ValueError("Error in SUM!")

    for country in guo_temp_data:
        results.setdefault(country, dict({"PL before": 0, "CCTB": 0, "Data factor": 0}))
        results[country]["PL before"] += guo_temp_data[country]["PL_before"]
        results[country]["CCTB"] += guo_temp_data[country]["PL_after"]
        results[country]["Data factor"] += guo_temp_data[country]["E_factor_after"]

    # print(results)

    guo_temp_data.clear()


csv.register_dialect("excel", delimiter=";")

with open(open_file, "r") as file:
    contents = csv.DictReader(file, dialect="excel")

    results = {}  # Country: CZ; P/L before: 12345; PL after: 1258

    GUO = ""
    row_no = 0
    guo_temp_data = {}  # Country: CZ; {OP Revenue: 123; Empl: 123; Assets: 123; P/L before: 123; PL after: 123}
    for row in contents:
        data = dict(row)

        if row_no == 0:
            GUO = data["GUO - BvD ID number"]
        row_no += 1

        if GUO == data["GUO - BvD ID number"]:
            set_temp_guo_data()
            print("Working on ROW: {} and BVD id: {}".format(row_no, data["BvD ID number"]))

        else:
            get_results()

            GUO = data["GUO - BvD ID number"]
            set_temp_guo_data()
            print("Working on ROW: {} and BVD id: {}".format(row_no, data["BvD ID number"]))

    get_results()

    file.close()

write_data = []

for country in results:
    temp = dict({"Country": country, "PL before": results[country]["PL before"], "CCTB": results[country]["CCTB"],
                 "Data factor": results[country]["Data factor"]})
    write_data.append(temp)

with open(write_file, "w", newline='') as result_file:
    writer = csv.DictWriter(result_file, fieldnames=["Country", "PL before", "CCTB", "Data factor"], dialect="excel")
    writer.writeheader()
    print("Saving...")
    writer.writerows(write_data)
    print("Completed")
result_file.close()
