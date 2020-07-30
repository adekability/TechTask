import re
import xlrd, xlwt


def get_number_validity(number):
    match = re.search('^((\+7|7|8)+([0-9]){10})$',number)
    if match is not None:
        return True
    else:
        return False


def get_valid_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


dictionary = dict()
allrows, messages= [],[]
excel_read = xlrd.open_workbook("parse.xlsx")
sheet = excel_read.sheet_by_index(0)
for i in range(sheet.nrows):
    row = sheet.row_values(i)
    allrows.append([])
    for y in range(len(row)):
        if y == 4 and i != 0:
            messages.append(row[y])
        allrows[i].append(row[y])
print(allrows)
for i in range(len(messages)):
    nums, urls = [], []
    dictionary = dict()
    array = messages[i].split()
    for y in array:
        if get_number_validity(y):
            nums.append(y)
    urls += get_valid_url(messages[i])
    nums = list(dict.fromkeys(nums))
    urls = list(dict.fromkeys(urls))
    dictionary['urls'] = urls
    dictionary['nums'] = nums
    allrows[i+1][len(allrows)+1]= str(dictionary)
print(allrows)


wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

for i in range(len(allrows)):
    for y in range(len(allrows[i])):
        print(allrows[i][y],end="\t")
        ws.write(i, y, allrows[i][y])
    print()
wb.save('example.xls')