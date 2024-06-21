import psycopg2
import datetime

DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

child_id = "1" #sys.argv[1]
grade = 4

currDate = datetime.datetime(2024, 8, 10)
subscribeDate = datetime.datetime(2024, 8, 1)

database = DB_NAME
host = DB_HOST
user = DB_USER
port = DB_PORT
password = DB_PASS
conn = psycopg2

dayDiff = (currDate - subscribeDate).days

week = int(dayDiff / 7) + 1

try:
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)

    cursor = conn.cursor()

    print("database connected")

    temp = []

    sql = "select * from story\
        where standard_id={grade} and week_num <= {week}".format(grade=grade, week=week)

    cursor.execute(sql)
    column_names = [desc[0] for desc in cursor.description]
    temp.append(column_names)

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

    for i in data:
        print(i["story_id"])

except:
    print("database not connected")