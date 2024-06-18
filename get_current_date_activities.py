import psycopg2
import datetime
from dateutil.relativedelta import relativedelta

DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

currDate = datetime.datetime(2024, 7, 8) + relativedelta(hours=1) # adding hours because in db start dates arent exactly 2024-08-22, they have few minutes added to it
# nextDate = currDate + relativedelta(days=7)

database = DB_NAME
host = DB_HOST
user = DB_USER
port = DB_PORT
password = DB_PASS
conn = psycopg2
activities = []

def get_activities(activities):
    CC = []
    EXP = []
    PG = []
    IPG = []
    LH = []
    daily = []
    weekly = []
    fortnightly = []
    activityArr = []

    # for i in activities:
    #     if i["act_category_id"] == 4:
    #         CC.append(i)

    for i in activities:
        if i["start_date"] + relativedelta(days=1) > i["end_date"] and currDate > i["start_date"]: # get all daily activities
            daily.append(i)
        elif i["start_date"] + relativedelta(weeks=1) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
            weekly.append(i)
        elif i["start_date"] + relativedelta(weeks=2) > i["end_date"] and currDate > i["start_date"]: # get all fortnightly activities
            fortnightly.append(i)
        # else:
        #     print("not weekly or daily")
    
    # for i in CC: # CC is daily
    #     if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3: # 3 is completed
    #         activityArr.append(i)

    for i in daily:
        if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3:
            activityArr.append(i)

    for i in weekly:
        if i["start_date"] < currDate and i["end_date"] > currDate - relativedelta(weeks=1) and i["activity_status_id"] != 3:
            activityArr.append(i)
    
    for i in fortnightly:
        if i["start_date"] < currDate and i["end_date"] > currDate - relativedelta(weeks=3) and i["activity_status_id"] != 3:
            activityArr.append(i)

    for i in activityArr:
        print(i["activity_id"], end='\n')
    
    return activityArr

try:
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)

    cursor = conn.cursor()

    temp = []

    # query = "SELECT * FROM public.child_activity\
    #          WHERE start_date <= %s AND end_date > %s"
    
    # cursor.execute(query, [currDate, currDate])

    cursor.execute("SELECT * FROM public.child_activity LIMIT 0")
    column_names = [desc[0] for desc in cursor.description]
    temp.append(column_names)

    sql = "SELECT * FROM public.child_activity"
    cursor.execute(sql)
    temp.append(cursor.fetchall())

    data = []

    col = temp[0]
    for i in temp[1]:
        temp = {}
        for k in range(len(col)):
            col_data = col[k]
            row_data = i[k]
            temp[col_data] = row_data
        data.append(temp)
    
    activities = get_activities(data)
    print(len(activities))

    print("database connected")
except Exception as error:
    print("database could not be connected")
    print(error)
    exit()

# for i in activities:
#     print(i, end='\n')

''' add category id and standard id in the table
select child_activity.*, activity.act_category_id, activity.standard_id
from child_activity
left join activity on child_activity.activity_id=activity.activity_id
'''
