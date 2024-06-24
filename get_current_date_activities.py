import sqlalchemy_test
import datetime
from dateutil.relativedelta import relativedelta
import json
import sys

if len(sys.argv) != 3:
    print("Wrong Usage. Usage is: python ___.py (child_id) (current date in string)")
    exit()

child_id = sys.argv[1]

date_string = sys.argv[2]
try:
    date_time_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
except ValueError as e:
    print(f"Error parsing date = {e}")

currDate = date_time_obj #datetime.datetime(2024, 7, 8) + relativedelta(hours=1) # adding hours because in db start dates arent exactly 2024-08-22, they have few minutes added to it
# print(currDate)
# nextDate = currDate + relativedelta(days=7)

# activities = []

# def get_activities(activities):
#     CC = []
#     EXP = []
#     PG = []
#     IPG = []
#     LH = []
#     daily = []
#     weekly = []
#     fortnightly = []
#     activityArr = []

#     # for i in activities:
#     #     if i["act_category_id"] == 4:
#     #         CC.append(i)

#     for i in activities:
#         if i["start_date"] + relativedelta(days=1) > i["end_date"] and currDate > i["start_date"]: # get all daily activities
#             daily.append(i)
#         elif i["start_date"] + relativedelta(weeks=1) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
#             weekly.append(i)
#         elif i["start_date"] + relativedelta(weeks=2) > i["end_date"] and currDate > i["start_date"]: # get all fortnightly activities
#             fortnightly.append(i)
#         # else:
#         #     print("not weekly or daily")
    
#     # for i in CC: # CC is daily
#     #     if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3: # 3 is completed
#     #         activityArr.append(i)

#     for i in daily:
#         if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3:
#             activityArr.append(i)

#     for i in weekly:
#         if i["start_date"] < currDate and i["end_date"] > currDate - relativedelta(weeks=1) and i["activity_status_id"] != 3:
#             activityArr.append(i)
    
#     for i in fortnightly:
#         if i["start_date"] < currDate and i["end_date"] > currDate - relativedelta(weeks=3) and i["activity_status_id"] != 3:
#             activityArr.append(i)

#     for i in activityArr:
#         pass
#         # print(i["activity_id"], end='\n')
    
#     return activityArr

conn = sqlalchemy_test.Connection()
activities = conn.get_child_activities_with_activity_table(child_id)
currDateActivities = conn.get_current_date_activities(activities, currDate)

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
for i in currDateActivities:
    for k in range(len(i.keys())):
        value = list(i.values())
        keys = list(i.keys())
        if type(value[k]) == datetime.datetime:
            i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
    index += 1

json.dump(currDateActivities, sys.stdout, indent=4)
# print(index)

# try:
#     conn = psycopg2.connect(database=database,
#                             user=user,
#                             password=password,
#                             host=host,
#                             port=port)

#     cursor = conn.cursor()

#     temp = []

#     # query = "SELECT * FROM public.child_activity\
#     #          WHERE start_date <= %s AND end_date > %s"
    
#     # cursor.execute(query, [currDate, currDate])

#     cursor.execute("SELECT * FROM public.child_activity LIMIT 0")
#     column_names = [desc[0] for desc in cursor.description]
#     temp.append(column_names)

#     sql = "SELECT * FROM public.child_activity"
#     cursor.execute(sql)
#     temp.append(cursor.fetchall())

#     data = []

#     col = temp[0]
#     for i in temp[1]:
#         temp = {}
#         for k in range(len(col)):
#             col_data = col[k]
#             row_data = i[k]
#             temp[col_data] = row_data
#         data.append(temp)
    
#     activities = get_activities(data)
#     print(len(activities))

#     print("database connected")
# except Exception as error:
#     print("database could not be connected")
#     print(error)
#     exit()

# for i in activities:
#     print(i, end='\n')

''' add category id and standard id in the table
select child_activity.*, activity.act_category_id, activity.standard_id
from child_activity
left join activity on child_activity.activity_id=activity.activity_id
'''
