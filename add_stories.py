import connection
import datetime
import json
import sys

child_id = "1" #sys.argv[1]
grade = 4 #sys.argv[2]

currDate = datetime.datetime(2024, 8, 20)
subscribeDate = datetime.datetime(2024, 8, 1)

dayDiff = (currDate - subscribeDate).days

week = int(dayDiff / 7) + 1

conn = connection.Connection()

stories = conn.get_stories(week, grade)

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


index = 0
for i in stories:
    for k in range(len(i.keys())):
        value = list(i.values())
        keys = list(i.keys())
        if type(value[k]) == datetime.datetime:
            i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
    index += 1

json.dump(stories, sys.stdout, indent=4)

