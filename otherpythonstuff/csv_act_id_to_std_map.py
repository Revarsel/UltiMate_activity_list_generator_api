import csv

skill_data = []
with open("associated_skill.csv", "r") as file2:
    data = csv.reader(file2)
    
    for i in data:
        skill_data.append([i[0], i[1]])

skill_data = skill_data[1:]
# print(skill_data)

dictionary = {}

for i in skill_data:
    dictionary[i[1]] = i[0]

with open("Only_Activity_Database_Entry_file.csv", "r") as file:
    data = csv.reader(file, delimiter=',')
    count = 0
    for i in data:
        if count == 0:
            count += 1
            continue
        local = []
        local.append(i[0])
        i.pop(1)
        i = i[1:5]
        for k in i:
            if k != "None":
                local.append(dictionary[k])
        print(local)

# file_data = []

# with open("Only_Activity_Database_Entry_file.csv", "r") as file:
#     data = csv.DictReader(file, delimiter=',')
#     for i in data:
#         local = []
#         local.append(i["Act_id"])
#         keys = list(i.keys())
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(1)
#         keys.pop(0)
#         for k in keys:
#             if i[k] != "None":
#                 local.append(k)
#         file_data.append(local)

# string = ""
# for i in file_data:
#     act_id = i[0]
#     for k in i[1:]:
#         string = string + act_id + "," + k + "\n"

# print(string)
# with open("test.csv", "w") as file1:
#     file1.write(string)