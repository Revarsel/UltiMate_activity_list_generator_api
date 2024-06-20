import psycopg2
import datetime
from dateutil.relativedelta import relativedelta

DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

database = DB_NAME
host = DB_HOST
user = DB_USER
port = DB_PORT
password = DB_PASS
conn = psycopg2
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

try:
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)

    cursor = conn.cursor()

    temp = []

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
    
    activity_pool = get_activity_pool_activities(data)

    cursor.close()

    print("database connected")
except Exception as error:
    print("database could not be connected")
    print(error)
    exit()

'''  this is for joining activity and focus_area to get both data in same table (understand this again)
SELECT * FROM public.activity
INNER JOIN
public.act_focus_area ON activity.activity_id=act_focus_area.activity_id
WHERE act_focus_area.focus_area_id IN (SELECT focus_area_id FROM child_focus_area WHERE child_id=1)
'''