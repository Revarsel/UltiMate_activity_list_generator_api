import psycopg2

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
conn = psycopg2

try:
    conn = psycopg2.connect(database=database,
                            user=user,
                            password=password,
                            host=host,
                            port=port)

    cursor = conn.cursor()

    print("database connected")

    temp = []

    sql = "SELECT child_activity.*, activity.act_category_id\
    FROM child_activity\
    LEFT JOIN activity ON child_activity.activity_id=activity.activity_id\
    WHERE child_activity.child_id={child}".format(child=child_id)

    cursor.execute(sql)
    column_names = [desc[0] for desc in cursor.description]
    temp.append(column_names)


    #sql = "SELECT * FROM public.child_activity WHERE child_id={child}".format(child=child_id)
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

except:
    print("database not connected")