import datetime
from dateutil.relativedelta import relativedelta
import sqlalchemy_test
import json
import sys

DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

child_id = "1" #sys.argv[1]

database = DB_NAME
host = DB_HOST
user = DB_USER
port = DB_PORT
password = DB_PASS
# conn = psycopg2
activities = []

currDate = datetime.datetime(2024, 8, 21)

def get_activity_pool_activities(activities):
    CC = []
    daily = []
    weekly = []
    fortnightly = []
    activity_pool = []

    for i in activities:
        if i["act_category_id"] == 4:
            # print(i)
            CC.append(i)

    # for i in activities:
    #     if i["start_date"] + relativedelta(days=1) > i["end_date"] and currDate > i["start_date"]: # get all daily activities
    #         daily.append(i)
    #     elif i["start_date"] + relativedelta(weeks=1) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
    #         weekly.append(i)
    #     elif i["start_date"] + relativedelta(weeks=2) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
    #         fortnightly.append(i)
        # else:
        #     print("not weekly or daily")
    
    for i in CC: # CC is daily
        if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3: # 3 is completed
            # print(i)
            activity_pool.append(i)

    # for i in daily:
    #     if i["start_date"] + relativedelta(days=3) < currDate and i["activity_status_id"] != 3:
    #         activity_pool.append(i)

    # for i in weekly:
    #     if i["start_date"] + relativedelta(weeks=2) < currDate and i["activity_status_id"] != 3:
    #         activity_pool.append(i)
    
    # for i in fortnightly:
    #     if i["start_date"] + relativedelta(weeks=4) < currDate and i["activity_status_id"] != 3:
    #         activity_pool.append(i)

    for i in activity_pool:
        print(i["activity_id"], end='\n')
    
    return activity_pool

conn = sqlalchemy_test.Connection()
activities = conn.get_child_activities(child_id)
activity_pool = conn.get_activity_pool_activities(activities, currDate)
# for i in activities:
#     print(i["start_date"])
# print(len(activity_pool))

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
for i in activity_pool:
    for k in range(len(i.keys())):
        value = list(i.values())
        keys = list(i.keys())
        if type(value[k]) == datetime.datetime:
            i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
        # i[start] = convert_datetime_to_str(i[start], i)
        # i[end] = convert_datetime_to_str(i[end])
    # i["index"] = index
    index += 1

sys.stdout.write(json.dumps(activity_pool))

# try:
#     conn = psycopg2.connect(database=database,
#                             user=user,
#                             password=password,
#                             host=host,
#                             port=port)

#     cursor = conn.cursor()

#     temp = []

#     sql = "SELECT child_activity.child_id, child_activity.start_date, child_activity.end_date, child_activity.activity_status_id, activity.*\
#     FROM activity\
#     LEFT JOIN child_activity ON child_activity.activity_id=activity.activity_id\
#     WHERE child_activity.child_id={child}".format(child=child_id)

#     cursor.execute(sql)
#     column_names = [desc[0] for desc in cursor.description]
#     temp.append(column_names)


#     #sql = "SELECT * FROM public.child_activity WHERE child_id={child}".format(child=child_id)
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
    
#     activity_pool = get_activity_pool_activities(data)

#     cursor.close()

#     print("database connected")
# except Exception as error:
#     print("database could not be connected")
#     print(error)
#     exit()

# '''  this is for joining activity and focus_area to get both data in same table (understand this again)
# SELECT * FROM public.activity
# INNER JOIN
# public.act_focus_area ON activity.activity_id=act_focus_area.activity_id
# WHERE act_focus_area.focus_area_id IN (SELECT focus_area_id FROM child_focus_area WHERE child_id=1)
# '''