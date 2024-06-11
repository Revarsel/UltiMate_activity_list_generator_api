import psycopg2
import datetime
from dateutil.relativedelta import relativedelta

currDate = datetime.datetime(2024, 5, 21)

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

try:
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)
    
    cursor = conn.cursor()
    query = "SELECT * FROM public.child_activity"
    cursor.execute(query)
    data = cursor.fetchone()
    for i in data:
        print(i)
    
    print("database connected (upload data)")
except:
    print("database could not be connected (upload data)")
    exit()