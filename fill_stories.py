import connection
import json
import sys
import datetime
import copy 

def convert_datetime_to_str(date, data=""):
    if type(date) == str:
        print(data)
        return date
    else:
        pass
        #return date
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    if int(month) / 10 < 1:
        month = "0{month}".format(month=month)
    if int(day) / 10 < 1:
        day = "0{day}".format(day=day)
    if int(hour) / 10 < 1:
        hour = "0{hour}".format(hour=hour)
    if int(minute) / 10 < 1:
        minute = "0{minute}".format(minute=minute)
    if int(second) / 10 < 1:
        second = "0{second}".format(second=second)

    string = "{year}-{month}-{day} {hour}:{minutes}:{seconds}".format(year=year, month=month, day=day, hour=hour, minutes=minute, seconds=second)
    return string

conn = connection.Connection()

stories = conn.get_stories_only_n(10)

stories_title = []

for b in stories:
    stories_title.append(b["title"]) #add first 8 titles

focus_list = conn.get_focus_area()

focus_ordered = [[] for _ in range(12)] # array for each std

index = 0
for i in focus_list:
    for k in range(len(i.keys())):
        value = list(i.values())
        keys = list(i.keys())
        if type(value[k]) == datetime.datetime:
            i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
    index += 1

# index = 0
# for i in stories:
#     for k in range(len(i.keys())):
#         value = list(i.values())
#         keys = list(i.keys())
#         if type(value[k]) == datetime.datetime:
#             i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)  # use this for json dump only
#     index += 1

for i in focus_list:
    match i["standard_id"]:
        case 1:
            focus_ordered[0].append(i)
        case 2:
            focus_ordered[1].append(i)
        case 3:
            focus_ordered[2].append(i)
        case 4:
            focus_ordered[3].append(i)
        case 5:
            focus_ordered[4].append(i)
        case 6:
            focus_ordered[5].append(i)
        case 7:
            focus_ordered[6].append(i)
        case 8:
            focus_ordered[7].append(i)
        case 9:
            focus_ordered[8].append(i)
        case 10:
            focus_ordered[9].append(i)
        case 11:
            focus_ordered[10].append(i)
        case 12:
            focus_ordered[11].append(i)

final_stories = []

for standard in range(12): # 12 stds
    for focusindex in range(len(focus_ordered[standard])): # focus of each std
        # for i in range(1): # 8 stories per focus area per standard
        story = copy.deepcopy(stories[0])
        for i in range(8):
            story["title"] = str(focus_ordered[standard][focusindex]["focus_area_id"]) + "_Q1_" + str(standard+1) + "_" + str(stories_title[i])
            final_stories.append(copy.deepcopy(story))

# json.dump(len(final_stories), sys.stdout, indent=4)

conn.dump_stories_in_story_table(final_stories)
