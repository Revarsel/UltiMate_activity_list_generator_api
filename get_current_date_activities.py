import psycopg2
import datetime
from dateutil.relativedelta import relativedelta

DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

currDate = datetime.datetime(2024, 6, 8) + relativedelta(hours=1) # adding hours because in db start dates arent exactly 2024-08-22, they have few minutes added to it
# nextDate = currDate + relativedelta(days=7)

database = DB_NAME
host = DB_HOST
user = DB_USER
port = DB_PORT
password = DB_PASS
conn = psycopg2
activities = []

try:
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)

    cursor = conn.cursor()

    query = "SELECT * FROM public.child_activity\
            WHERE start_date <= %s AND end_date > %s"
    
    cursor.execute(query, [currDate, currDate])

    data = cursor.fetchall()

    for i in data:

        if i[5] == 3: # all activities are 1 right now so this should be empty
            activities.append(i)

    print("database connected")
except Exception as error:
    print("database could not be connected" + error)
    exit()

for i in activities:
    print(i, end='\n')
