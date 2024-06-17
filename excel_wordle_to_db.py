import psycopg2
import csv
import datetime
from dateutil.relativedelta import relativedelta

all_columns = []
words_list = {}

standard = 4


with open("Wordle_List.csv", 'r') as file:
    csvread = csv.reader(file, delimiter=';')
    for i in csvread:
        # print(i)
        all_columns.append(i)

for i in range(1, 11):
    currDate = datetime.datetime(2024, 6, 2)
    words_list[i] = []
    for k in all_columns[1:]:
        words_list[i].append([k[i-1], currDate])
        currDate = currDate + relativedelta(days=1)
    
#print(words_list[2])

conn = psycopg2.connect(database="ultimatedb",
                                user="postgress",
                                password="Shubham123",
                                host="62.72.57.120",
                                port="5432")

conn.autocommit = True

print("database connected")

today = datetime.date.today()

cursor = conn.cursor()
index = 0
for i in words_list:
    for k in words_list[i]:
        #print(k[0])
        if k[0] == "null" or len(k[0]) != 5:
            continue

        sql = "INSERT INTO public.wordle_words\
                (wordle_words_id, word, standard_id, is_archived, created_by, created_date, revision, word_show_date)\
                VALUES\
                (%s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, [index, k[0], i, False, "Bhuvan", today, 0, k[1]])
        index += 1

# "wordle_words_id"	"word"	"standard_id"	"is_archived"	"created_by"	"updated_by"	"created_date"	"updated_date"	"revision"	"word_show_date"