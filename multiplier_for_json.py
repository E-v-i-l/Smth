import os
import re

print("please, enter the path to the folder")
way = input()
num = int(input("reqierd number of copies"))
files = os.listdir(way)
patternjson = re.compile(r".*\.json")
json = []
for i in files:
    matchjson = patternjson.match(i)
    if matchjson:
        json += [matchjson.group()]
for i in json:
    with open(way + "\\" + i, "r") as file:
        string = file.read()
    for j in range(num):
        with open(way + "\\" + i[0:-5:1] + "-" + str(j) + '.json', "w") as file:
            file.write(string)
