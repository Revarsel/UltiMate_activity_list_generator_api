from data_from_pgadmin import connection
from testing_direct_sql_data import get_data
import random
import json
import datetime
from dateutil.relativedelta import relativedelta

class Data: # All User Data
    def __init__(self) -> None:
        self.grade = ""
        self.pinCode = ""
        self.religion = ""
        self.focusArea = []
        self.gender = ""
        self.language = ""

userData = Data()

class ActivityData:
    def __init__(self) -> None:
        self.HUActList = []
        self.RNTActList = []
        self.CCActList = []
        self.ExpActList = []
        self.PGActList = []
        self.IPGActList = []
        self.LHActList = []
        self.WordleList = []

    def filterLists(self):
        FilterFunctions.grade(self.HUActList, userData.grade)
        FilterFunctions.grade(self.RNTActList, userData.grade)
        if userData.grade in ("N", "Jr", "Sr", "1", "2"):
            FilterFunctions.grade(self.CCActList, userData.grade)
            FilterFunctions.grade(self.ExpActList, userData.grade)
        else:
            FilterFunctions.grade(self.PGActList, userData.grade)
            FilterFunctions.grade(self.IPGActList, userData.grade)
            FilterFunctions.grade(self.LHActList, userData.grade)


actData = ActivityData()

start = "start_date" # one var for the key "Start Date"
end = "end_date" # one var for the key "End Date"
focus_string = "focus" # one var for the key "focus"

class GenerateActivities:
    def __init__(self) -> None:
        tempArrWeekly = []
        tempArr2PerWeek = []
        for i in range(3):  # loop to order focus areas as [A,B,A,B,C,D,C,D,E,F,E,F]
            for k in range(4):
                if k % 2 == 0:
                    tempArrWeekly.append(userData.focusArea[int((i * 2))])
                    tempArr2PerWeek.append((userData.focusArea[int((i * 2))], userData.focusArea[int(1 + (i * 2))]))
                else:
                    tempArrWeekly.append(userData.focusArea[int(1 + (i * 2))])
                    tempArr2PerWeek.append((userData.focusArea[int((i * 2))], userData.focusArea[int((i * 2) + 1)]))
                
        self.focusAreaWeekly = tempArrWeekly
        self.focusArea2PerWeek = tempArr2PerWeek
        self.fullActList = []
        self.monthDays = []
        self.actDone = [] # this stores all activity ids to check for duplicates in the following activity generators
        for j in range(1, 4):
            monthPrev = startDate + relativedelta(months=max((j-1), 0))
            monthNext = startDate + relativedelta(months=j)
            dayDiff = (monthNext - monthPrev).days
            self.monthDays.append(dayDiff)
    
    def GenerateDailyActivities(self):
        for b in range(dayDifference):
            currDate = startDate + relativedelta(days=b, second=30)
            nextDate = currDate + relativedelta(hours=23, minutes=59) # seconds = 0

            week = int((b) / 7)
            
            focus = self.focusAreaWeekly[week % 12]

            if grade in ("N", "Jr", "Sr", "1", "2"):
                tempCCList = FilterFunctions.focus_area(actData.CCActList, focus)
                tempCCAct = random.choice(actData.CCActList)   # Creative Corner

                for _ in range(len(tempCCList)):
                    if tempCCAct["activity_id"] not in self.actDone:
                        break
                    tempCCAct = random.choice(tempCCList)
                
                # for _ in range(len(actData.CCActList)):
                #     if tempCCAct["activity_id"] not in self.actDone:
                #         break
                #     tempCCAct = random.choice(actData.CCActList)

                #remove_key_values_from_dictionary(tempCCAct)
                self.actDone.append(tempCCAct["activity_id"])

                tempCCAct[start] = currDate
                tempCCAct[end] = nextDate
                tempCCAct[focus_string] = focus
                tempCCAct["wordle_words_id"] = 0
                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                #print(b)
                if currDate > currentDate:
                    if grade_num >= 3:
                        wordle_act = actData.WordleList[grade_num-3]
                        wordle_act["wordle_words_id"] = wordle_words_list[b][0]
                        wordle_act[start] = currDate
                        wordle_act[end] = nextDate
                        self.fullActList.append(wordle_act)
                    self.fullActList.append(tempCCAct)
            
            elif grade in ("3", "4", "5", "6", "7"):
                tempPGList = FilterFunctions.focus_area(actData.PGActList, focus)   # Personal Growth
                tempPGAct = random.choice(tempPGList)
                
                for _ in range(len(tempPGList)):
                    if tempPGAct["activity_id"] not in self.actDone:
                        break
                    tempPGAct = random.choice(tempPGList)

                #remove_key_values_from_dictionary(tempPGAct)
                self.actDone.append(tempPGAct["activity_id"])

                tempPGAct[start] = currDate
                tempPGAct[end] = nextDate
                tempPGAct["wordle_words_id"] = 0
                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                if currDate > currentDate:
                    if grade_num >= 3:
                        wordle_act = actData.WordleList[grade_num-3]
                        wordle_act["wordle_words_id"] = wordle_words_list[b][0]
                        wordle_act[start] = currDate
                        wordle_act[end] = nextDate
                        self.fullActList.append(wordle_act)
                    self.fullActList.append(tempPGAct) # Personal Growth

        
        index = 0
        for months in range(len(self.monthDays)):
            for currDay in range(self.monthDays[months]):
                currDate = startDate + relativedelta(months=months, days=currDay, second=30)
                nextDate = currDate + relativedelta(hours=23, minutes=59, seconds=29)  # days=currDay

                actData.HUActList[index][start] = currDate   # Habit Up
                actData.HUActList[index + 1][start] = currDate

                actData.HUActList[index][end] = nextDate
                actData.HUActList[index + 1][end] = nextDate

                actData.RNTActList[index][start] = currDate   # Roots and Traditions
                actData.RNTActList[index + 1][start] = currDate

                actData.RNTActList[index][end] = nextDate
                actData.RNTActList[index + 1][end] = nextDate

                actData.HUActList[index]["wordle_words_id"] = 0   # Habit Up
                actData.HUActList[index + 1]["wordle_words_id"] = 0

                actData.HUActList[index]["wordle_words_id"] = 0
                actData.HUActList[index + 1]["wordle_words_id"] = 0

                actData.RNTActList[index]["wordle_words_id"] = 0   # Roots and Traditions
                actData.RNTActList[index + 1]["wordle_words_id"] = 0

                actData.RNTActList[index]["wordle_words_id"] = 0
                actData.RNTActList[index + 1]["wordle_words_id"] = 0

                #remove_key_values_from_dictionary(actData.HUActList[index])
                #remove_key_values_from_dictionary(actData.HUActList[index + 1])
                #remove_key_values_from_dictionary(actData.RNTActList[index])
                #remove_key_values_from_dictionary(actData.RNTActList[index + 1])

                if currDate > currentDate and (grade_changed == True or subscribed == True):
                    self.fullActList.append(actData.HUActList[index].copy())
                    self.fullActList.append(actData.HUActList[index + 1].copy())

                    self.fullActList.append(actData.RNTActList[index].copy())
                    self.fullActList.append(actData.RNTActList[index + 1].copy())
            index += 2


    def GenerateWeeklyActivities(self):
        index = int(dayDifference / 7) + 1 # Find num of weeks (give 1 week less so we have to add 1 to it since half a week is taken as 0 week but we want it as 1 week)

        tempLHActList = actData.LHActList
        for i in range(index): # start to end date number of weeks
            currDate = startDate + relativedelta(weeks=i, seconds=30)
            nextDate = min_date(currDate + relativedelta(days=6, hours=23, minutes=59), endDate) # seconds=0

            focusWeek = self.focusAreaWeekly[i % 12]
            focusArea2PerWeek = self.focusArea2PerWeek[i % 12]

            tempExpActList = FilterFunctions.focus_area(actData.CCActList, focusArea2PerWeek[0]) # CCactlist should be expactlist (but both combine now so change that first)

            # length = int(len(tempExpActList) / 2)
            # tempExpActList1 = tempExpActList[:length]
            # tempExpActList2 = tempExpActList[length:]

            #print(len(tempExpActList2))
            tempIPGActList = FilterFunctions.focus_area(actData.IPGActList, focusWeek)
            if grade in ("N", "Jr", "Sr"):
                act1 = random.choice(tempExpActList)
                act2 = random.choice(tempExpActList)
                
                for _ in range(len(tempExpActList)):
                    if act1["activity_id"] not in self.actDone and act1["activity_id"] != act2["activity_id"]:
                        break
                    act1 = random.choice(tempExpActList)

                #remove_key_values_from_dictionary(act1["activity_id"])
                self.actDone.append(act1["activity_id"])

                for _ in range(len(tempExpActList)):
                    if act2["activity_id"] not in self.actDone and act1["activity_id"] != act2["activity_id"]:
                        break
                    act2 = random.choice(tempExpActList)

                #remove_key_values_from_dictionary(act2)
                self.actDone.append(act2["activity_id"])

                act1[start] = currDate
                act2[start] = currDate
                act1[end] = nextDate
                act2[end] = nextDate
                act1["wordle_words_id"] = 0
                act2["wordle_words_id"] = 0

                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                if currDate > currentDate:
                    self.fullActList.append(act1) # Learning Through Exploring for Nursery Junior and Senior KG
                    self.fullActList.append(act2)

            elif grade in ("1", "2"):
                for _ in range(2):
                    act1 = random.choice(tempExpActList)
                    act2 = random.choice(tempExpActList)

                    for _ in range(len(tempExpActList)):
                        if act1["activity_id"] not in self.actDone and act1["activity_id"] != act2["activity_id"]:
                            break
                        act1 = random.choice(tempExpActList)

                    #remove_key_values_from_dictionary(act1["activity_id"])
                    self.actDone.append(act1["activity_id"])

                    for _ in range(len(tempExpActList)):
                        if act2["activity_id"] not in self.actDone and act1["activity_id"] != act2["activity_id"]:
                            break
                        act2 = random.choice(tempExpActList)

                    #remove_key_values_from_dictionary(act2)
                    self.actDone.append(act2["activity_id"])

                    act1[start] = currDate
                    act2[start] = currDate
                    act1[end] = nextDate
                    act2[end] = nextDate
                    act1["wordle_words_id"] = 0
                    act2["wordle_words_id"] = 0

                    if subscribed == False and (grade_changed == False and focus_changed == False):
                        continue

                    if currDate > currentDate:
                        self.fullActList.append(act1) # Learning Through Exploring for First and Second Standards
                        self.fullActList.append(act2)

            else:
                tempIPGAct = random.choice(tempIPGActList)

                for _ in range(len(tempIPGActList)):
                    if tempIPGAct["activity_id"] not in self.actDone:
                        break
                    tempIPGAct = random.choice(tempIPGActList)

                #remove_key_values_from_dictionary(tempIPGAct)
                self.actDone.append(tempIPGAct["activity_id"])

                tempIPGAct[start] = currDate
                tempIPGAct[end] = nextDate
                tempIPGAct["wordle_words_id"] = 0
                self.fullActList.append(tempIPGAct) # Interpersonal Growth

                if i % 2 == 0 and grade not in ("8", "9"):
                    tempLHAct = random.choice(tempLHActList)

                    for _ in range(len(tempLHActList)):
                        if tempLHAct["activity_id"] not in self.actDone:
                            break
                        tempLHAct = random.choice(tempLHActList)

                    #remove_key_values_from_dictionary(tempLHAct)
                    self.actDone.append(tempLHAct["activity_id"])

                    tempLHAct[start] = currDate
                    tempLHAct[end] = min_date(currDate + relativedelta(days=13, hours=23, minutes=59), endDate) # seconds=0
                    tempLHAct["wordle_words_id"] = 0
                    if subscribed == False and (grade_changed == False and focus_changed == False):
                        continue

                    if currDate > currentDate:
                        self.fullActList.append(tempLHAct)

                elif grade in ("8", "9"):
                    tempLHAct = random.choice(tempLHActList)

                    for _ in range(len(tempLHActList)):
                        if tempLHAct["activity_id"] not in self.actDone:
                            break
                        tempLHAct = random.choice(tempLHActList)

                    #remove_key_values_from_dictionary(tempLHAct)
                    self.actDone.append(tempLHAct["activity_id"])

                    tempLHAct[start] = currDate
                    tempLHAct[end] = nextDate

                    tempLHAct["wordle_words_id"] = 0

                    if subscribed == False and (grade_changed == False and focus_changed == False):
                        continue

                    if currDate > currentDate:
                        self.fullActList.append(tempLHAct) # Life Hacks

                    tempPGList = FilterFunctions.focus_area(actData.PGActList, focusWeek)
                    tempPGAct = random.choice(tempPGList)

                    for _ in range(len(tempPGList)):
                        if tempPGAct["activity_id"] not in self.actDone:
                            break
                        tempPGAct = random.choice(tempPGList)

                    #remove_key_values_from_dictionary(tempPGAct)
                    self.actDone.append(tempPGAct["activity_id"])

                    tempPGAct[start] = currDate
                    tempPGAct[end] = nextDate

                    tempPGAct["wordle_words_id"] = 0

                    if subscribed == False and (grade_changed == False and focus_changed == False):
                        continue

                    if currDate > currentDate:
                        self.fullActList.append(tempPGAct) # Personal Growth For Eighth and Ninth (1 per week not everyday)

    def GenerateActivities(self):
        self.GenerateDailyActivities()
        self.GenerateWeeklyActivities()
    
    def AddExistingActivities(self, activities: list):
        for i in activities:
            self.actDone.append(i[0])


startDate = datetime.datetime(2024, 6, 1)
endDate = startDate + relativedelta(months=3)
dayDifference = (endDate - startDate).days # - 84 # 84 days = 12 weeks

# MAIN INPUT VARIABLES
pin_code = 411038
religion = "Hindu" # jai shree ram
grade_num = 4  # 1 -> N, 2 -> Jr etc
grade = ""
focus_area = ["A", "B", "C", "D", "E", "F"]
gender = "MALE"
language = "english"
child_id = "1"

currentDate = datetime.datetime(2024, 6, 1)
subscribed = True
grade_changed = True
focus_changed = False

map_grade = ["N", "Jr", "Sr"]
if grade_num - 3 < 0:
    grade = map_grade[grade_num]
else:
    grade = str(grade_num-3)

HUActList = [] # ["h act1["activity_id"]", "h act2", "h act3", "h act4", "h act5", "h act6"]  
RNTActList = [] # ["rnt act1["activity_id"]", "rnt act2", "rnt act3", "rnt act4", "rnt act5", "rnt act6"]

# CCActList = [{"activity_id" : r} for r in range(92)]  # Comment this for main deployment
# ExpActList = [{"activity_id" : r} for r in range(92)]  # Comment this for main deployment
# PGActList = [{"activity_id" : r} for r in range(92)]  # Comment this for main deployment
# IPGActList = [{"activity_id" : r} for r in range(92)]  # Comment this for main deployment

# for i in range(1, 31):  # Comment this loop for main deployment
#     actData.HUActList.append({"activity_id" : i}) # ("hu act " + str(i))
#     actData.RNTActList.append({"activity_id" : i})
#     actData.IPGActList.append({"activity_id" : i})
#     actData.LHActList.append({"activity_id" : i})

# actData.CCActList = CCActList
# actData.ExpActList = ExpActList
# actData.PGActList = PGActList

userData.pinCode = pin_code
userData.religion = religion
userData.grade = grade
userData.focusArea = focus_area
userData.gender = gender
userData.language = language

class FilterFunctions:
    def grade(list, grade) -> list:
        # return list
        tempArr = []
        for t in list:
            if t["standard_id"] == grade: # Uncomment this for main deployment
                tempArr.append(t)
        return tempArr
    
        # if pair["standard_id"] == grade:
        #     return True
        # return False

    def focus_area(list, focus) -> list:
        return list
        # tempArr = []
        # for k in list:
        #     if k["primary_skill"] == focus:
        #         tempArr.append(k)
        # return tempArr
    
        # if pair["primary_skill"] == focus: # Uncomment this for main deployment
        #     return True
        # return False

counter = 0

def convert_datetime_to_str(date, data=""):
    if type(date) == str:
        print(data)
        return date
    else:
        pass
        #return date
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    if int(month) / 10 < 1:
        month = "0{month}".format(month=month)
    if int(day) / 10 < 1:
        day = "0{day}".format(day=day)
    if int(hour) / 10 < 1:
        hour = "0{hour}".format(hour=hour)
    if int(minute) / 10 < 1:
        minute = "0{minute}".format(minute=minute)
    if int(second) / 10 < 1:
        second = "0{second}".format(second=second)

    string = "{year}-{month}-{day} {hour}:{minutes}:{seconds}".format(year=year, month=month, day=day, hour=hour, minutes=minute, seconds=second)
    return string

def min_date(date1: datetime.datetime, date2: datetime.datetime):
    year1 = date1.year
    year2 = date2.year
    if year2 > year1:
        return date1
    elif year2 < year1:
        return date2
    
    month1 = date1.month
    month2 = date2.month
    if month2 > month1:
        return date1
    elif month2 < month1:
        return date2

    day1 = date1.day
    day2 = date2.day
    if day2 > day1:
        return date1
    elif day2 < day1:
        return date2

def remove_key_values_from_dictionary(dictionary: dict):
    keys = list(dictionary.keys())
    for i in keys:
        if i not in (end, start, focus_string, "activity_id", "child_id"):
            dictionary.pop(i)

actListRef = []

# with open("table1.csv") as activities_data:  # 1 -> habit up, 2 -> rnt, 4 -> CC  (act_category_id)
#     data = csv.DictReader(activities_data)
#     for i in data:
#         actListRef.append(i)
#     print(actListRef[0])

actListRef = get_data()

for k in actListRef:
    id = int(k["act_category_id"])
    if id == 1:
        actData.HUActList.append(k)
    elif id == 2:
        actData.RNTActList.append(k)
    elif id == 3:
        actData.WordleList.append(k)
    elif id == 4:
        actData.CCActList.append(k)

actData.filterLists()

Connection = connection()
# print(Connection.get_table_data("child_activity")[0])
# Connection.get_table_data("activity")
wordle_words_list = Connection.get_wordle_words(startDate, endDate, grade_num) # get data from wordle_word db
# print(len(wordle_words_list), dayDifference, end='\n')
# print(wordle_words_list[0], end='\n')
# print(wordle_words_list[-1], end='\n')

Generator = GenerateActivities()
Generator.AddExistingActivities(Connection.get_table_data("child_activity"))
# Generator.GenerateDailyActivities()
# Generator.GenerateWeeklyActivities()
Generator.GenerateActivities()

tempArr = []

for i in Generator.fullActList:
    tempArr.append(i)

Connection.dump_data_in_child_activity(tempArr, child_id)

# index = 0

# for i in tempArr:
#     for k in range(len(i.keys())):
#         value = list(i.values())
#         keys = list(i.keys())
#         if type(value[k]) == datetime.datetime:
#             i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
#         # i[start] = convert_datetime_to_str(i[start], i)
#         # i[end] = convert_datetime_to_str(i[end])
#     i["index"] = index
#     index += 1

# with open("test1.json", "w") as test:
#     json.dump(tempArr, test)

