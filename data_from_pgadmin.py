import psycopg2
import csv
 
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Satksh123?" # put in password
DB_HOST = "localhost"
DB_PORT = "5432"

column_names = []

def get_birth_year_data():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        cursor = conn.cursor()
        sql = "COPY (SELECT * FROM language) TO STDOUT WITH CSV DELIMITER ';';"
        cursor.execute("SELECT * FROM language LIMIT 0")
        column_names = [desc[0] for desc in cursor.description]


        with open("table.csv", "w") as file:
            csvwriter = csv.writer(file, delimiter=';')
            csvwriter.writerow(column_names)
            cursor.copy_expert(sql, file)

        cursor.close()

        # print(column_names)

        print("Database connected successfully")
    except:
        print("Database not connected successfully")

if __name__ == "__main__":
    get_birth_year_data()