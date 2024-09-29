from Generator import GenerateActivities
from connection import Connection, convert_all_values_to_json_readable
import sys
import json

if len(sys.argv) in [1,2]:
    print("Usage is [is_trial, child_id_1, child_id_2, ...]")
    exit()

Conn = Connection()

for child_num in range(2, len(sys.argv)):
    try:
        child_id = sys.argv[child_num]
        Generator = GenerateActivities(child_id, Conn, sys.argv[1])

        Generator.GenerateActivities()

        Conn.dump_data_in_child_activity(fullActList=Generator.fullActList, child_id=child_id)

        # tempArr = convert_all_values_to_json_readable(Generator.fullActList)

        # json.dump(tempArr.__len__(), sys.stdout, indent=4)

    except Exception as error:
        print("Error occured : " + str(error))
