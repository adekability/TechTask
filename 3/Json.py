import json
from datetime import datetime
from tabulate import tabulate


def get_date_obj(sample):
    sample = sample.replace("-", " ").replace("T", " ").replace(".", " ").replace(":", " ").replace("+0600","")
    sample = sample.split(" ")
    sample = [int(digit) for digit in sample]
    sample = datetime(sample[0], sample[1], sample[2], sample[3], sample[4], sample[5], sample[6])
    return sample


with open("status.json", "r", encoding="utf-8") as fb:
    whole_file = json.load(fb)

variable, dict_time, count_time, result_dict = "", dict(), dict(), dict()
part_file = whole_file['changelog']['histories']
purchase = list(dict.fromkeys([i['items'][0]['toString'] for i in part_file]))

for i in purchase:
    dict_time[i] = datetime(2020, 7, 22, 0, 0, 0, 0) - datetime(2020, 7, 22, 0, 0, 0, 0)
    count_time[i] = 0

for i in part_file:
    if variable is not "":
        for y in purchase:
            if variable == y:
                count_time[y] += 1
        dict_time[variable] += (get_date_obj(i['created']) - result_dict[variable])
    result_dict[i['items'][0]['toString']] = get_date_obj(i['created'])
    variable = i['items'][0]['toString']

table = tabulate([[i, count_time[i], dict_time[i]] for i in dict_time], headers=['Status', 'Count', 'Time'])

print(table)