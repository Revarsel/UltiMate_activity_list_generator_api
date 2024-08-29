from connection import Connection
from random import choice
# import sys
# import json

focus_area_id = [r for r in range(1,35)]

conn = Connection()

activities = conn.get_activities_only()

print(choice(activities))
print(choice(focus_area_id))

# for i in activities:
#     conn.dump_activities_in_act_focus_area_table(i, choice(focus_area_id))