import connection
import datetime
import json
import sys

child_id = 4 #sys.argv[1]

conn = connection.Connection()

conn.get_child_activity_table_activities(child_id)


