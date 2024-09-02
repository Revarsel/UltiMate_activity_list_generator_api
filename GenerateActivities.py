import random
import json
import datetime
from dateutil.relativedelta import relativedelta
from connection import Connection, convert_all_values_to_json_readable
import sys

if len(sys.argv) != 2:
    print("Wrong Usage. Usage is: ____.py (child_id)")
    exit()

class ActivityData:
    def __init__(self) -> None:
        self.HUActList = [[], []]
        self.RNTActList = [[], []]
        self.CCActList = [[], []]
        self.ExpActList = [[], []]
        self.PGActList = [[], []]
        self.IPGActList = [[], []]
        self.LHActList = [[], []]
        self.WordleList = [[], []]


actData = ActivityData()

start = "start_date" # one var for the key "Start Date"
end = "end_date" # one var for the key "End Date"
focus_string = "focus" # one var for the key "focus"

class GenerateActivities:
    def __init__(self) -> None:
        tempArrWeekly = []
        tempArr2PerWeek = []
        # for i in range(3):  # loop to order focus areas as [A,B,A,B,C,D,C,D,E,F,E,F]
        #     for k in range(4):
        #         if k % 2 == 0:
        #             tempArrWeekly.append(userData.focusArea[int((i * 2))])
        #             tempArr2PerWeek.append((userData.focusArea[int((i * 2))], userData.focusArea[int(1 + (i * 2))]))
        #         else:
        #             tempArrWeekly.append(userData.focusArea[int(1 + (i * 2))])
        #             tempArr2PerWeek.append((userData.focusArea[int((i * 2))], userData.focusArea[int((i * 2) + 1)]))

        weeks_num = int(dayDifference/7)
        self.focusAreaWeekly = Conn.get_focus_area_frequency(grade_num)[:weeks_num+1] #tempArrWeekly
        # self.focusArea2PerWeek = tempArr2PerWeek #Conn.get_focus_area_frequency(grade_num)[:weeks_num*2] #tempArr2PerWeek
        self.fullActList = []
        self.monthDays = []
        self.actDone = [] # this stores all activity ids to check for duplicates in the following activity generators
        for j in range(1, 4):
            monthPrev = startDate + relativedelta(months=max((j-1), 0))
            monthNext = startDate + relativedelta(months=j)
            dayDiff = (monthNext - monthPrev).days
            self.monthDays.append(dayDiff)
    
    def GenerateDailyActivities(self):
        discuss = 0 # 0 = False, 1 = True

        for b in range(dayDifference):
            currDate = startDate + relativedelta(days=b, second=30)
            nextDate = currDate + relativedelta(hours=23, minutes=59) # seconds = 0
            day = currDate.weekday()
            if day == 5:
                discuss = 1
            elif day == 6 or day % 2 == 1: # 6 is sunday, day % 0 gives alternate
                discuss = 0
                continue
            else:
                discuss = 0

            week = int((b) / 7)

            focus = self.focusAreaWeekly[week]

            if grade in ("N", "Jr", "Sr", "1", "2"): # Creative Corner
                tempCCList = []
                prev = True
                if len(actData.CCActList[1]) == 0: # previous grade activities are empty
                    prev = False
                    tempCCList = FilterFunctions.focus_area(actData.CCActList[0], focus)
                else:
                    tempCCList = FilterFunctions.focus_area(actData.CCActList[1], focus)
                tempCCAct = random.choice(tempCCList)

                for _ in range(1000):
                    if tempCCAct["activity_id"] not in self.actDone and tempCCAct["is_discussion"] == discuss:
                        break
                    tempCCAct = random.choice(tempCCList)

                self.actDone.append(tempCCAct["activity_id"])

                tempCCAct[start] = currDate
                tempCCAct[end] = nextDate

                self.fullActList.append(tempCCAct.copy())
                
                if prev:
                    actData.CCActList[1] = custom_remove(actData.CCActList[1], tempCCAct)
                else:
                    actData.CCActList[0] = custom_remove(actData.CCActList[0], tempCCAct)
            
            elif grade in ("3", "4", "5", "6", "7"): # Personal Growth
                tempPGList = []
                prev = True
                if len(actData.PGActList[1]) == 0: # previous grade activities are empty
                    prev = False
                    tempPGList = FilterFunctions.focus_area(actData.PGActList[0], focus)
                else:
                    tempPGList = FilterFunctions.focus_area(actData.PGActList[1], focus)
                tempPGAct = random.choice(tempPGList)
                
                for _ in range(1000):
                    if tempPGAct["activity_id"] not in self.actDone:
                        break
                    tempPGAct = random.choice(tempPGList)

                self.actDone.append(tempPGAct["activity_id"])

                tempPGAct[start] = currDate
                tempPGAct[end] = nextDate

                self.fullActList.append(tempPGAct.copy()) # Personal Growth
                
                if prev:
                    actData.PGActList[1] = custom_remove(actData.PGActList[1], tempPGAct)
                else:
                    actData.PGActList[0] = custom_remove(actData.PGActList[0], tempPGAct)
        
        index = 0
        for months in range(len(self.monthDays)):
            for currDay in range(self.monthDays[months]):
                currDate = startDate + relativedelta(months=months, days=currDay, second=30)
                nextDate = currDate + relativedelta(hours=23, minutes=59, seconds=29)  # days=currDay

                actData.HUActList[0][index][start] = currDate   # Habit Up
                actData.HUActList[0][index + 1][start] = currDate

                actData.HUActList[0][index][end] = nextDate
                actData.HUActList[0][index + 1][end] = nextDate

                # actData.RNTActList[index][start] = currDate   # Roots and Traditions
                # actData.RNTActList[index + 1][start] = currDate

                # actData.RNTActList[index][end] = nextDate
                # actData.RNTActList[index + 1][end] = nextDate

                #remove_key_values_from_dictionary(actData.HUActList[index])
                #remove_key_values_from_dictionary(actData.HUActList[index + 1])
                #remove_key_values_from_dictionary(actData.RNTActList[index])
                #remove_key_values_from_dictionary(actData.RNTActList[index + 1])


                self.fullActList.append(actData.HUActList[0][index].copy())
                self.fullActList.append(actData.HUActList[0][index + 1].copy())

                # self.fullActList.append(actData.RNTActList[index].copy())
                # self.fullActList.append(actData.RNTActList[index + 1].copy())
            index += 2


    def GenerateWeeklyActivities(self):
        weeks = int(dayDifference / 7) + 1 # Find num of weeks (give 1 week less so we have to add 1 to it since half a week is taken as 0 week but we want it as 1 week)

        for i in range(weeks): # start to end date number of weeks
            focus = self.focusAreaWeekly[i]
            currDate = startDate + relativedelta(weeks=i, seconds=30)
            nextDate = min_date(currDate + relativedelta(days=6, hours=23, minutes=59), endDate) # seconds=0

            if grade in ("3", "4", "5"): # Interpersonal Growth (once a week)
                tempIPGList = []
                prev = True
                if len(actData.IPGActList[1]) == 0: # previous grade activities are empty
                    prev = False
                    tempIPGList = FilterFunctions.focus_area(actData.IPGActList[0], focus)
                else:
                    tempIPGList = FilterFunctions.focus_area(actData.IPGActList[1], focus)
                tempIPGAct = random.choice(tempIPGList)

                for _ in range(1000):
                    if tempIPGAct["activity_id"] not in self.actDone:
                        break
                    tempIPGAct = random.choice(tempIPGList)

                self.actDone.append(tempIPGAct["activity_id"])

                tempIPGAct[start] = currDate
                tempIPGAct[end] = nextDate
                self.fullActList.append(tempIPGAct.copy())

                if prev:
                    actData.IPGActList[1] = custom_remove(actData.IPGActList[1], tempIPGAct)
                else:
                    actData.IPGActList[0] = custom_remove(actData.IPGActList[0], tempIPGAct)
            
            elif grade in ("6", "7", "8", "9"): # (once every 2 weeks)
                if i % 2 == 0:
                    tempIPGList = []
                    prev = True
                    if len(actData.IPGActList[1]) == 0: # previous grade activities are empty
                        prev = False
                        tempIPGList = FilterFunctions.focus_area(actData.IPGActList[0], focus)
                    else:
                        tempIPGList = FilterFunctions.focus_area(actData.IPGActList[1], focus)
                    tempIPGAct = random.choice(tempIPGList)

                    for _ in range(1000):
                        if tempIPGAct["activity_id"] not in self.actDone:
                            break
                        tempIPGAct = random.choice(tempIPGList)

                    self.actDone.append(tempIPGAct["activity_id"])

                    tempIPGAct[start] = currDate
                    tempIPGAct[end] = nextDate
                    self.fullActList.append(tempIPGAct.copy())

                    if prev:
                        actData.IPGActList[1] = custom_remove(actData.IPGActList[1], tempIPGAct)
                    else:
                        actData.IPGActList[0] = custom_remove(actData.IPGActList[0], tempIPGAct)
            
            if grade in ("8", "9"): # Personal Growth
                tempPGList = []
                prev = True
                if len(actData.PGActList[1]) == 0: # previous grade activities are empty
                    prev = False
                    tempPGList = FilterFunctions.focus_area(actData.PGActList[0], focus)
                else:
                    tempPGList = FilterFunctions.focus_area(actData.PGActList[1], focus)
                tempPGAct = random.choice(tempPGList)
                
                for _ in range(1000):
                    if tempPGAct["activity_id"] not in self.actDone:
                        break
                    tempPGAct = random.choice(tempPGList)

                self.actDone.append(tempPGAct["activity_id"])

                tempPGAct[start] = currDate
                tempPGAct[end] = nextDate

                self.fullActList.append(tempPGAct.copy()) # Personal Growth
                
                if prev:
                    actData.PGActList[1] = custom_remove(actData.PGActList[1], tempPGAct)
                else:
                    actData.PGActList[0] = custom_remove(actData.PGActList[0], tempPGAct)

            if grade in ("8", "9"): # life hacks (once a week)
                tempLHList = []
                prev = True
                if len(actData.LHActList[1]) == 0: # previous grade activities are empty
                    prev = False
                    tempLHList = FilterFunctions.focus_area(actData.LHActList[0], focus)
                else:
                    tempLHList = FilterFunctions.focus_area(actData.LHActList[1], focus)
                tempLHAct = random.choice(tempLHList)
                
                for _ in range(1000):
                    if tempLHAct["activity_id"] not in self.actDone:
                        break
                    tempPGAct = random.choice(tempLHList)

                self.actDone.append(tempLHAct["activity_id"])

                tempLHAct[start] = currDate
                tempLHAct[end] = nextDate

                self.fullActList.append(tempLHAct.copy()) # Personal Growth
                
                if prev:
                    actData.LHActList[1] = custom_remove(actData.LHActList[1], tempLHAct)
                else:
                    actData.LHActList[0] = custom_remove(actData.LHActList[0], tempLHAct)
            
            elif grade in ("3", "4", "5", "6", "7"): # (once every 2 weeks)
                if i % 2 == 0:
                    tempLHList = []
                    prev = True
                    if len(actData.LHActList[1]) == 0: # previous grade activities are empty
                        prev = False
                        tempLHList = FilterFunctions.focus_area(actData.LHActList[0], focus)
                    else:
                        tempLHList = FilterFunctions.focus_area(actData.LHActList[1], focus)
                    tempLHAct = random.choice(tempLHList)
                    
                    for _ in range(1000):
                        if tempLHAct["activity_id"] not in self.actDone:
                            break
                        tempLHAct = random.choice(tempLHList)

                    self.actDone.append(tempLHAct["activity_id"])

                    tempLHAct[start] = currDate
                    tempLHAct[end] = nextDate

                    self.fullActList.append(tempLHAct.copy()) # Personal Growth
                    
                    if prev:
                        actData.LHActList[1] = custom_remove(actData.LHActList[1], tempLHAct)
                    else:
                        actData.LHActList[0] = custom_remove(actData.LHActList[0], tempLHAct)
                
    def GenerateQuarterlyActivities(self):
        if grade not in ("N", "Jr", "Sr", "1", "2"):
            focus = self.focusAreaWeekly[0]
            tempLHList = []
            prev = True
            if len(actData.LHActList[1]) == 0: # previous grade activities are empty
                prev = False
                tempLHList = FilterFunctions.focus_area(actData.LHActList[0], focus)
            else:
                tempLHList = FilterFunctions.focus_area(actData.LHActList[1], focus)
            tempLHAct = random.choice(tempLHList)
            
            for _ in range(1000):
                if tempLHAct["activity_id"] not in self.actDone:
                    break
                tempLHAct = random.choice(tempLHList)

            self.actDone.append(tempLHAct["activity_id"])

            tempLHAct[start] = startDate
            tempLHAct[end] = endDate

            self.fullActList.append(tempLHAct.copy()) # Personal Growth
            
            if prev:
                actData.LHActList[1] = custom_remove(actData.LHActList[1], tempLHAct)
            else:
                actData.LHActList[0] = custom_remove(actData.LHActList[0], tempLHAct)
            
            ################################################

            # tempLHActList = actData.LHActList
            # tempLHAct = random.choice(tempLHActList)

            # for _ in range(1000):
            #     if tempLHAct["activity_id"] not in self.actDone and tempLHAct["act_frequency_id"] == 1: # this number should be for quarterly frequency
            #         break
            #     tempLHAct = random.choice(tempLHActList)

            # self.actDone.append(tempLHAct["activity_id"])

            # tempLHAct[start] = startDate
            # tempLHAct[end] = endDate

            # self.fullActList.append(tempLHAct.copy())
    
    def GenerateMudras(self):
        weeks = int(dayDifference / 7) + 1
        currDate = startDate
        nextDate = currDate + relativedelta(weeks=2)

        existing_mudras: list = Conn.get_child_activities_with_activity_table(child_id)

        mudras.sort(key=sort_activity_id)
        existing_mudras = list(filter(func, existing_mudras))

        for i in range(weeks):
            if i % 2 == 1:
                continue
            rand_mudra = random.choice(mudras)
            for _ in range(1000):
                if rand_mudra["activity_id"] not in self.actDone:
                    break
                rand_mudra = random.choice(mudras)
            
            rand_mudra["start_date"] = currDate
            rand_mudra["end_date"] = nextDate
            currDate = nextDate
            nextDate = min_date(endDate, currDate + relativedelta(weeks=2))
            self.fullActList.append(rand_mudra.copy())
    
    def GenerateShloks(self):
        shloks = Conn.get_shloks()

        short = list(filter(filter_short, shloks))
        medium = list(filter(filter_medium, shloks))
        long = list(filter(filter_long, shloks))

        short_shlok = random.choice(short)
        medium_shlok = random.choice(medium)
        long_shlok = random.choice(long)

        short_shlok["start_date"] = startDate
        short_shlok["end_date"] = startDate + relativedelta(weeks=2)

        medium_shlok["start_date"] = startDate
        medium_shlok["end_date"] = startDate + relativedelta(weeks=2)

        long_shlok["start_date"] = startDate
        long_shlok["end_date"] = startDate + relativedelta(weeks=2)

        self.fullActList.append(short_shlok)
        self.fullActList.append(medium_shlok)
        self.fullActList.append(long_shlok)


    def GenerateActivities(self):
        self.GenerateDailyActivities()
        self.GenerateWeeklyActivities()
        self.GenerateQuarterlyActivities()
        self.GenerateMudras()
        if is_new_user:
            self.GenerateShloks()
    
    def AddExistingActivitiesToExclude(self, activities: list):
        for i in activities:
            self.actDone.append(i["activity_id"])


startDate = datetime.datetime.now() #datetime.datetime(2024, 6, 1)
endDate = startDate + relativedelta(months=3)
dayDifference = (endDate - startDate).days # - 84 # 84 days = 12 weeks

Conn = Connection()

# MAIN INPUT VARIABLES
pin_code = 411038
religion = "Hindu" # jai shree ram
grade = ""
focus_area = ["A", "B", "C", "D", "E", "F"]
gender = "MALE"
language = "english"

child_id = sys.argv[1]
child_details = Conn.get_child_details(child_id)
grade_num = int(child_details["standard_id"])  # 1 -> N, 2 -> Jr etc
is_new_user = child_details["is_new_user"]

quarter = 1

map_grade = ["N", "Jr", "Sr"] # = [1,2,3] grade_num
if grade_num - 3 < 0:
    grade = map_grade[grade_num]
else:
    grade = str(grade_num-3)

class FilterFunctions:
    def grade(list, grade) -> list:
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

def custom_remove(data, data_to_remove):
    for i in range(len(data)):
        index = 0
        data_value = data[i]
        if data_value["activity_id"] == data_to_remove["activity_id"]:
            index = i
            data.pop(index)
            return data
    else:
        return []

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

def is_in_actDone(generator: GenerateActivities, act_id):
    return (act_id in generator.actDone)

def func(val):
    if val["act_category_id"] == 2 and val["activity_game_type_id"] == 5:
        return True
    return False

def sort_activity_id(val):
    return val["activity_id"]

def filter_short(data):
    if data["shlok_length_id"] == 1:
        return True
    return False

def filter_medium(data):
    if data["shlok_length_id"] == 2:
        return True
    return False

def filter_long(data):
    if data["shlok_length_id"] == 3:
        return True
    return False

def filter_shloks(data):
    if data["act_category_id"] == 2 and data["activity_game_type_id"] == 4:
        return True
    return False

actListBothGrade = Conn.get_activities(grade_num)
actListRefCurrGrade = actListBothGrade[0]
actListRefPrevGrade = actListBothGrade[1]

mudras = Conn.get_mudras()

wordle_words_list = Conn.get_wordle_words(startDate, endDate, grade_num)
# print(len(wordle_words_list), dayDifference, end='\n')
# print(wordle_words_list[0], end='\n')
# print(wordle_words_list[-1], end='\n')

Generator = GenerateActivities()
Generator.AddExistingActivitiesToExclude(Conn.get_child_activity_table_activities(child_id))

for k in actListRefCurrGrade:
    id = int(k["act_category_id"])
    act_id = int(k["activity_id"])

    if is_in_actDone(Generator, act_id):
        continue

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

    if is_in_actDone(Generator, act_id):
        continue

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

Conn.dump_data_in_child_activity(fullActList=Generator.fullActList, child_id=child_id)

# tempArr = convert_all_values_to_json_readable(Generator.fullActList)

# json.dump(len(tempArr), sys.stdout, indent=4)
# print("\n" + str(grade))
