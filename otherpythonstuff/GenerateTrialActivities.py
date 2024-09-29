from Generator import GenerateActivities
from connection import Connection, convert_all_values_to_json_readable
import sys
import json

if len(sys.argv) == 1:
    print("Provide A child_id To Fill Activities In")
    exit()

Conn = Connection()

for child_num in range(1, len(sys.argv)):

    child_id = sys.argv[child_num]
    Generator = GenerateActivities(child_id, Conn, trial=True)

    Generator.GenerateActivities()

    Conn.dump_data_in_child_activity(fullActList=Generator.fullActList, child_id=child_id)

    # tempArr = convert_all_values_to_json_readable(Generator.fullActList)

    # json.dump(tempArr.__len__(), sys.stdout, indent=4)