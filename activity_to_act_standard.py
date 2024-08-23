from connection import Connection, convert_all_values_to_json_readable
import json
import sys

conn = Connection()

activities = conn.get_activities_only()
# activities = convert_all_values_to_json_readable(activities)

conn.dump_activities_in_activity_standard_table(activities)

# json.dump(activities.__len__(), sys.stdout, indent=4)