import psycopg2
import csv
import datetime
 
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Satksh123?" # put in password
DB_HOST = "localhost"
DB_PORT = "5432"

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
            print("database connected (upload data)")
        except:
            print("database could not be connected (upload data)")
            exit()

    def dump_data_in_child_activity(self, fullActList: list):
        cursor = self.conn.cursor()
        for i in fullActList:
            query = "INSERT INTO(child_activity_id, activity_id, child_id, start_date, end_date, activity_status_id, act_start_time, act_completion_time, reassign_count, activity_time_minutes, wordle_words_id, is_archived, created_by, updated_id, created_date, updated_date, revision)VALUES (83762, {act_id}, , {child_id}, {start}, {end})".format(act_id=i["activity_id"], start=i["Start Date"], end=i["End Date"])
            cursor.execute(query)

if __name__ == "__main__":
    Connection = connection()
    Connection.get_table_data("activity")