import random               # MAKE THIS CODE BETTER (use oops, refactor a little, etc)
import json
import datetime
import csv
from dateutil.relativedelta import relativedelta

HUActList = [] #["h act1", "h act2", "h act3", "h act4", "h act5", "h act6"]  
RNTActList = [] #["rnt act1", "rnt act2", "rnt act3", "rnt act4", "rnt act5", "rnt act6"]  # Filter out pin code and religion for RNT list
CCActList = [("CC " + str(r)) for r in range(91)]
ExpActList = [("EXP " + str(r)) for r in range(91)]
fortnightly = ["Fort 1", "Fort 2"]
weeklyAct = ["week 1", "week 2", "week 3", "week 4"]

fullActList = {}  # Main huge list
tempActList= {}  # Temporary list for for loop which appends to dailyAct list

startDate = datetime.date(2024, 3, 1) # START DATE

endDate = startDate + relativedelta(months=3)

diff = endDate - startDate # DAYS DIFFERENCE START DATE AND END DATE
difference = diff.days - 84 # 84 = 12 (weeks) X 7 (days)
# print(difference)

# MAIN INPUT VARIABLES
pin_code = 411038
religion = "Hindu" # jai shree ram
grade = "1"
focus_area = ["A", "B", "C", "D", "E", "F"]
gender = "MALE"
language = "english"

act_list_ref = []

with open("data-1716973262669.csv") as act_data:  # 1 -> habit up, 2 -> rnt, 4 -> CC  (act_category_id)
    data = csv.DictReader(act_data)
    for i in data:
        act_list_ref.append(i)

# HUActList.clear()
# RNTActList.clear()
# CCActList.clear()

for k in act_list_ref:
    id = int(k["act_category_id"])
    if id == 1:
        HUActList.append(k)
    elif id == 2:
        RNTActList.append(k)
    elif id == 4:
        CCActList.append(k)

for i in range(1, 7):
    RNTActList.append("rnt act" + str(i))

def grade_filter(act_info_dict):
    if act_info_dict["standard_id"] == grade:
        return True
    return False

HUActList = list(filter(grade_filter, HUActList))
# print(len(HUActList))
# RNTActList = list(filter(grade_filter, RNTActList))
# CCActList = list(filter(grade_filter, CCActList))

#exit()


# def filter_through_pin_and_religion_rnt():
#     return RNTActList.filter(pin_code, religion)

# def filter_through_grade_habit_up():
#     return HUActList.filter(grade)

# def filter_through_grade_creative_corner():
#     return CCActList.filter(grade)

# def filter_through_grade_learn_exp():
#     return ExpActList.filter(grade)

# RNTActList = filter_through_pin_and_religion_rnt()
# HUActList = filter_through_grade_habit_up()
# CCActList = filter_through_grade_creative_corner()
# ExpActList = filter_through_grade_learn_exp()

focus_index = 0
for j in range(1, 4): # 3 MONTHS
    for i in range(1, 5): # FIRST 4 WEEKS
        loopActList = {}
        fortnightAct = ""
        weekAct = ""
        fortnightAct = fortnightly[int((i-1)/2)]
        
        weekAct = weeklyAct[i-1]

        if ((i-1)) % 2 == 0:
            focus_num = focus_index
        elif (i-1) % 2 == 1:
            focus_num = focus_index + 1

        focus = focus_area[focus_num]
        focus_next = focus_area[focus_num + 1]

        tempExpAct1 = random.choice(ExpActList)
        tempExpAct2 = random.choice(ExpActList)
        for _ in range(len(ExpActList)):
            if tempExpAct1 in ExpActList:
                tempExpAct1 = random.choice(ExpActList)
            elif tempExpAct2 in ExpActList and tempExpAct2 != tempExpAct1:
                tempExpAct2 = random.choice(ExpActList)
            else:
                break

        for x in range(1, 8): # 7 DAYS
            loopActList["Fortnightly"] = fortnightAct
            loopActList["Weekly"] = weekAct

            loopActList["Habit Up"] = [HUActList[2 * (j-1)], HUActList[2 * (j-1) + 1]] # habit up

            loopActList["Roots And Tradition"] = [RNTActList[2 * (j-1)], RNTActList[2 * (j-1) + 1]] # roots and tradition

            tempCCAct = random.choice(CCActList)
            for _ in range(len(CCActList)):
                if tempCCAct in CCActList:
                    tempCCAct = random.choice(CCActList)
                else:
                    break

            loopActList["Creative Corner"] = (tempCCAct + ", Focus : " + focus) # creative corner

            loopActList["Learning Through Exploring"] = [(tempExpAct1 + ", Focus : " + focus), (tempExpAct2 + ", Focus : " + focus_next)] # Learning through exploring

            day = "day " + str(x)

            tempActList[day] = loopActList.copy()
            loopActList.clear()


        # once per 14 days

        week = "week " + str(i + (4 * (j-1)))
        fullActList[week] = tempActList.copy()

        tempActList.clear()
        break
    focus_index += 2


focus = focus_area[0]
focus_next = focus_area[1]

for d in range(min(difference, 7)):
    fortnightAct = None
    weekAct = None

    loopActList["Fortnightly"] = fortnightAct
    loopActList["Weekly"] = weekAct

    loopActList["Habit Up"] = [HUActList[0], HUActList[1]]
    loopActList["Roots And Tradition"] = [RNTActList[0], RNTActList[1]]

    tempCCAct = random.choice(CCActList)
    for _ in range(len(CCActList)):
        if tempCCAct in CCActList:
            tempCCAct = random.choice(CCActList)
        else:
            break

    loopActList["Creative Corner"] = (tempCCAct + ", Focus : " + focus) # creative corner

    tempExpAct1 = random.choice(ExpActList)
    tempExpAct2 = random.choice(ExpActList)
    for _ in range(len(ExpActList)):
        if tempExpAct1 in ExpActList:
            tempExpAct1 = random.choice(ExpActList)
        elif tempExpAct2 in ExpActList and tempExpAct2 != tempExpAct1:
            tempExpAct2 = random.choice(ExpActList)
        else:
            break

    loopActList["Learning Through Exploring"] = [(tempExpAct1 + ", Focus : " + focus), (tempExpAct2 + ", Focus : " + focus_next)] # Learning through exploring

    day = "day " + str(d + 1)

    tempActList[day] = loopActList.copy()
    loopActList.clear()

    fullActList["week 13"] = tempActList.copy()
    tempActList.clear()

focus = focus_area[2]
focus_next = focus_area[3]

if difference > 7:
    fortnightAct = None
    weekAct = None

    loopActList["Fortnightly"] = fortnightAct
    loopActList["Weekly"] = weekAct

    loopActList["Habit Up"] = [HUActList[0], HUActList[1]]
    loopActList["Roots And Tradition"] = [RNTActList[0], RNTActList[1]]

    tempCCAct = random.choice(CCActList)
    for _ in range(len(CCActList)):
        if tempCCAct in CCActList:
            tempCCAct = random.choice(CCActList)
        else:
            break

    loopActList["Creative Corner"] = (tempCCAct + ", Focus : " + focus) # creative corner

    tempExpAct1 = random.choice(ExpActList)
    tempExpAct2 = random.choice(ExpActList)
    for _ in range(len(ExpActList)):
        if tempExpAct1 in ExpActList:
            tempExpAct1 = random.choice(ExpActList)
        elif tempExpAct2 in ExpActList and tempExpAct2 != tempExpAct1:
            tempExpAct2 = random.choice(ExpActList)
        else:
            break

    loopActList["Learning Through Exploring"] = [(tempExpAct1 + ", Focus : " + focus), (tempExpAct2 + ", Focus : " + focus_next)] # Learning through exploring

    day = "day 1"

    tempActList[day] = loopActList.copy()
    loopActList.clear()

    fullActList["week 14"] = tempActList.copy()
    tempActList.clear()


fields = ["activity_id"]

with open("test.json", "w") as test:
    json.dump(fullActList, test)
    #print("dumped")

with open("output.csv", 'w') as output:
    csvwrite = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")

    csvwrite.writeheader()

    csvwrite.writerows(fullActList["week 1"]["day 1"]["Habit Up"])
