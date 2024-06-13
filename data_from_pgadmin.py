import psycopg2
 
DB_NAME = "ultimatedb"
DB_USER = "postgress"
DB_PASS = "Shubham123" # put in password
DB_HOST = "62.72.57.120"
DB_PORT = "5432"

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
                    (activity_id, child_id, start_date, end_date, activity_status_id, reassign_count, is_archived, created_by, updated_by, created_date, updated_date, revision)\
                    VALUES\
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    # ({child_act_id}, {act_id}, {child_id}, {start_date}, {end_date}, {act_status_id}, {reassign_count}, {is_archived}, {created_by}, {updated_by}, {created_date}, {updated_date}, {revision});"
                    #.format(child_act_id=index, act_id=i["activity_id"], child_id=child_id, start_date=i["start_date"], end_date=i["end_date"], act_status_id=10283, reassign_count=0, is_archived=i["is_archived"], created_by=i["created_by"], updated_by=i["updated_by"], created_date=i["created_date"], updated_date=i["updated_date"], revision=0)
            cursor.execute(query, [i["activity_id"], child_id, i["start_date"], i["end_date"], 1, 0, i["is_archived"], i["created_by"], i["updated_by"], i["created_date"], i["updated_date"], 0])
            index += 1
            self.conn.commit()
        cursor.close()
    
    def get_table_data(self, tableName):
        cursor = self.conn.cursor()
        sql = "SELECT activity_id FROM public.{table}".format(table=tableName)
        cursor.execute(sql)
        data = cursor.fetchall()
        temp = []
        for i in data:
            temp.append(i)
        return temp


if __name__ == "__main__":
    Connection = connection()



# "child_activity_id"	"activity_id"	"child_id"	"start_date"	"end_date"	"activity_status_id"	"act_start_time"	"act_completion_time"	"reassign_count"	"activity_time_minutes"	"wordle_words_id"	"is_archived"	"created_by"	"updated_by"	"created_date"	"updated_date"	"revision"