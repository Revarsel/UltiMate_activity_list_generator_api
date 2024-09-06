from GenerateActivities import GenerateActivities, ActivityData
from connection import Connection, convert_all_values_to_json_readable
import datetime
import sys

Conn = Connection()

for child_num in range(1, len(sys.argv)):
    print(child_num)

    actData = ActivityData()

    child_id = sys.argv[child_num]
    child_details = Conn.get_child_details(child_id)
    grade_num = int(child_details["standard_id"])  # 1 -> N, 2 -> Jr etc
    user_id = int(child_details["user_id"])
    is_new_user = child_details["is_new_user"]
    grade = ""

    map_grade = ["N", "Jr", "Sr"] # = [1,2,3] grade_num
    if grade_num - 3 < 0:
        grade = map_grade[grade_num]
    else:
        grade = str(grade_num-3)

    subscription = Conn.get_subscription_from_user_id(user_id) # returns all subscriptions of the user in descending order
    start_date: datetime.datetime = subscription[0]["start_date"]
    end_date: datetime.datetime = subscription[0]["end_date"]

    weeks_completed_already = 0
    if len(subscription) > 0:
        for index, value in enumerate(subscription[1:]):
            weeks = 0
            sub_start: datetime.datetime = value["start_date"]
            sub_end: datetime.datetime = value["end_date"]
            weeks = int(((sub_end-sub_start).days)/7)
            weeks_completed_already += weeks

    # print(start_date)
    # print(end_date)
    # print((end_date-start_date).days)
    # print(int((((subscription[1]["end_date"])-(subscription[1]["start_date"])).days)/7))
    # print(subscription[1:])

    # generate2 = GenerateActivities(start_date, end_date, 0)
    # generate2.GenerateDailyActivities()
    # print()
    # generatpr = GenerateActivities(start_date, end_date, weeks_completed_already)
    # generatpr.GenerateDailyActivities()

    # exit()

    actListBothGrade = Conn.get_trial_activities(grade_num)
    mudras = Conn.get_trial_mudras()

    actListRefCurrGrade = actListBothGrade[0]
    actListRefPrevGrade = actListBothGrade[1]

    Generator = GenerateActivities(start_date=start_date, end_date=end_date, weeks_completed=weeks_completed_already)
    wordle_words_list = Conn.get_wordle_words(Generator.startDate, Generator.endDate, grade_num)
    Generator.AddExistingActivitiesToExclude(Conn.get_child_activity_table_activities(child_id))

    for k in actListRefCurrGrade:
        id = int(k["act_category_id"])
        act_id = int(k["activity_id"])

        if id == 1:
            actData.HUActList[0].append(k)
        elif id == 2:
            actData.RNTActList[0].append(k)
        elif id == 3:
            actData.WordleList[0].append(k)
        elif id == 4:
            actData.CCActList[0].append(k)
        elif id == 5:
            actData.PGActList[0].append(k)
        elif id == 6:
            actData.IPGActList[0].append(k)
        elif id == 7:
            actData.LHActList[0].append(k)

    for k in actListRefPrevGrade:
        id = int(k["act_category_id"])

        if id == 1:
            actData.HUActList[1].append(k)
        elif id == 2:
            actData.RNTActList[1].append(k)
        elif id == 3:
            actData.WordleList[1].append(k)
        elif id == 4:
            actData.CCActList[1].append(k)
        elif id == 5:
            actData.PGActList[1].append(k)
        elif id == 6:
            actData.IPGActList[1].append(k)
        elif id == 7:
            actData.LHActList[1].append(k)

    Generator.GenerateActivities()
    # Generator.GenerateWeeklyActivities()

    Conn.dump_data_in_child_activity(fullActList=Generator.fullActList, child_id=child_id)

    # tempArr = convert_all_values_to_json_readable(Generator.fullActList)

    # json.dump(tempArr, sys.stdout, indent=4)
    # print("\n" + str(grade))