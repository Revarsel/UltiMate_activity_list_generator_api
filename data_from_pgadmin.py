import psycopg2
import csv
import datetime
 
DB_NAME = "ultimatedb"
DB_USER = "postgres"
DB_PASS = "Pratik@2855" # put in password
DB_HOST = "localhost"
DB_PORT = "9876"

column_names = []

class connection:
    def __init__(self) -> None:
        self.database = DB_NAME
        self.host = DB_HOST
        self.user = DB_USER
        self.port = DB_PORT
        self.password = DB_PASS
        #self.conn = psycopg2.connect()
        try:
            self.conn = psycopg2.connect(database=self.database,
                                        user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)
            print("database connected")
        except:
            print("database could not be connected")

    def get_birth_year_data(self):
        cursor = self.conn.cursor()
        sql = "COPY (SELECT * FROM birth_year) TO STDOUT WITH CSV DELIMITER ';';"
        cursor.execute("SELECT * FROM birth_year LIMIT 0")
        column_names = [desc[0] for desc in cursor.description]


        with open("table.csv", "w") as file:
            csvwriter = csv.writer(file, delimiter=';')
            csvwriter.writerow(column_names)
            cursor.copy_expert(sql, file)
        
        # with open("table.csv", 'r') as file:
        #     csvreader = csv.DictReader(file)
        #     for i in csvreader:
        #         print(i)

        cursor.close()

        # print(column_names)
    
    def get_child_activity_table(self):
        cursor = self.conn.cursor()
        sql = "COPY (SELECT * FROM child_activity) TO STDOUT WITH CSV DELIMITER ';';"
        cursor.execute("SELECT * FROM language LIMIT 0")
        column_names = [desc[0] for desc in cursor.description]

        fullActList = []
        with open("table.csv", "w") as file:
            csvwriter = csv.writer(file, delimiter=';')
            csvwriter.writerow(column_names)
            cursor.copy_expert(sql, file)

            csvreader = csv.DictReader(file)
            for i in csvreader:
                fullActList.append(i)
            
        
        # for i in fullActList:
        #     if i[]

        cursor.close()
        pass

    def dump_data_in_child_activity(self, fullActList: list):
        cursor = self.conn.cursor()
        for i in fullActList:
            query = "INSERT INTO public.child_activity (activity_id, start_date, end_date)VALUES ({act_id}, {start}, {end})".format(act_id=i["activity_id"], start=i["Start Date"], end=i["End Date"])
            cursor.execute(query)

def check_date_between_two_dates(date1: datetime.datetime, date2: datetime.datetime, date_check: str):
    pass

if __name__ == "__main__":
    Connection = connection()
    Connection.get_birth_year_data()