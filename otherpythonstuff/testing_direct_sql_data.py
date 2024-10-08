import psycopg2

DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

data = []

table_name = "activity"

database = DB_NAME
host = DB_HOST
user = DB_USER
port = DB_PORT
password = DB_PASS

def get_data(grade):
    try:
        conn = psycopg2.connect(database=database,
                                    user=user,
                                    password=password,
                                    host=host,
                                    port=port)

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM public.{table} LIMIT 0".format(table=table_name))
        column_names = [desc[0] for desc in cursor.description]
        data.append(column_names)

        sql = "SELECT * FROM public.{table}\
               WHERE standard_id={grade}".format(table=table_name, grade=grade)
        cursor.execute(sql)
        data.append(cursor.fetchall())

        cursor.close()

        print("database connected (get data)")
    except:
        print("database could not be connected (get data)")

    data_to_dict = []

    col = data[0]
    for i in data[1]:
        temp = {}
        for k in range(len(col)):
            col_data = col[k]
            row_data = i[k]
            temp[col_data] = row_data
        data_to_dict.append(temp)

    #print(data_to_dict[5])
    return data_to_dict
