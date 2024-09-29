import psycopg2
import datetime
from dateutil.relativedelta import relativedelta
 
DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

startdate = datetime.datetime(2024, 6, 1)
enddate = startdate + relativedelta(months=3)

column_names = []

class connection:
    def __init__(self) -> None:
        self.database = DB_NAME
        self.host = DB_HOST
        self.user = DB_USER
        self.port = DB_PORT
        self.password = DB_PASS
        self.conn = psycopg2
        try:
            self.conn = psycopg2.connect(database=self.database,
                                        user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)
            # cursor = self.conn.cursor()
            # cursor.execute("SELECT * FROM public.activity;")
            # for i in cursor.fetchall():
            #     print(i)
            print("database connected (upload data)")
        except:
            print("database could not be connected (upload data)")
            exit()

    def dump_data_in_child_activity(self, fullActList: list, child_id):
        cursor = self.conn.cursor()
        index = 1
        for i in fullActList:
            query = "INSERT INTO public.child_activity\
                    (activity_id, child_id, start_date, end_date, activity_status_id, reassign_count, wordle_words_id, is_archived, created_by, updated_by, created_date, updated_date, revision)\
                    VALUES\
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    # ({child_act_id}, {act_id}, {child_id}, {start_date}, {end_date}, {act_status_id}, {reassign_count}, {is_archived}, {created_by}, {updated_by}, {created_date}, {updated_date}, {revision});"
                    #.format(child_act_id=index, act_id=i["activity_id"], child_id=child_id, start_date=i["start_date"], end_date=i["end_date"], act_status_id=10283, reassign_count=0, is_archived=i["is_archived"], created_by=i["created_by"], updated_by=i["updated_by"], created_date=i["created_date"], updated_date=i["updated_date"], revision=0)
            cursor.execute(query, [i["activity_id"], child_id, i["start_date"], i["end_date"], 1, 0, i["wordle_words_id"], i["is_archived"], i["created_by"], i["updated_by"], i["created_date"], i["updated_date"], 0])
            index += 1
            self.conn.commit()
            # return
        cursor.close()
    
    def get_table_data(self, tableName):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM public.{table}".format(table=tableName)
        cursor.execute(sql)
        data = cursor.fetchall()
        temp = []
        for i in data:
            temp.append(i)
        return temp
    
    def get_wordle_words(self, startdate, enddate, grade):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM public.wordle_words\
                WHERE word_show_date >= %s AND word_show_date <= %s AND standard_id = %s" #.format(start=startdate, end=enddate, grade=5)
        #print(sql)
        cursor.execute(sql, [startdate, enddate, grade])
        return cursor.fetchall()


if __name__ == "__main__":
    Connection = connection()
    for i in Connection.get_wordle_words(startdate, enddate, 5):
        print(i)



# "child_activity_id"	"activity_id"	"child_id"	"start_date"	"end_date"	"activity_status_id"	"act_start_time"	"act_completion_time"	"reassign_count"	"activity_time_minutes"	"wordle_words_id"	"is_archived"	"created_by"	"updated_by"	"created_date"	"updated_date"	"revision"