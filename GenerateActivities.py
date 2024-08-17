import random
import json
import datetime
from dateutil.relativedelta import relativedelta
from connection import Connection, convert_all_values_to_json_readable
import sys

if len(sys.argv) != 3:
    print("Wrong Usage. Usage is: ____.py (child_id) (grade)")
    exit()

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
                
        # print(tempArr2PerWeek)
        weeks_num = int(dayDifference/7)
        self.focusAreaWeekly = tempArrWeekly #Conn.get_focus_area_frequency(grade_num)[:weeks_num*2] #tempArrWeekly
        self.focusArea2PerWeek = tempArr2PerWeek #Conn.get_focus_area_frequency(grade_num)[:weeks_num*2] #tempArr2PerWeek
        self.fullActList = []
        self.monthDays = []
        self.actDone = [] # this stores all activity ids to check for duplicates in the following activity generators
        for j in range(1, 4):
            monthPrev = startDate + relativedelta(months=max((j-1), 0))
            monthNext = startDate + relativedelta(months=j)
            dayDiff = (monthNext - monthPrev).days
            self.monthDays.append(dayDiff)
    
    def GenerateDailyActivities(self):
        discuss = 0 # 0=False, 1=True
        # match quarter: # get this quarter from data table and the percentages too
        #     case 1:
        #         quarterDay = int(dayDifference / 2)
        #     case 2:
        #         quarterDay = int(dayDifference / 3)

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
            
            focus = self.focusAreaWeekly[week % 12]

            if grade in ("N", "Jr", "Sr", "1", "2"): # Creative Corner
                tempCCList = FilterFunctions.focus_area(actData.CCActList, focus)
                tempCCAct = random.choice(actData.CCActList)

                for _ in range(1000):
                    if tempCCAct["activity_id"] not in self.actDone: #and tempCCAct["is_discussion"] == discuss:
                        break
                    tempCCAct = random.choice(tempCCList)

                self.actDone.append(tempCCAct["activity_id"])

                tempCCAct[start] = currDate
                tempCCAct[end] = nextDate
                tempCCAct[focus_string] = focus
                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                if currDate > currentDate:
                    self.fullActList.append(tempCCAct.copy())
            
            elif grade in ("3", "4", "5", "6", "7"): # Personal Growth
                tempPGList = FilterFunctions.focus_area(actData.PGActList, focus)
                tempPGAct = random.choice(tempPGList)
                
                for _ in range(1000):
                    if tempPGAct["activity_id"] not in self.actDone:
                        break
                    tempPGAct = random.choice(tempPGList)

                self.actDone.append(tempPGAct["activity_id"])

                tempPGAct[start] = currDate
                tempPGAct[end] = nextDate
                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                if currDate > currentDate:
                    self.fullActList.append(tempPGAct.copy()) # Personal Growth
        
        index = 0
        for months in range(len(self.monthDays)):
            for currDay in range(self.monthDays[months]):
                currDate = startDate + relativedelta(months=months, days=currDay, second=30)
                nextDate = currDate + relativedelta(hours=23, minutes=59, seconds=29)  # days=currDay

                actData.HUActList[index][start] = currDate   # Habit Up
                actData.HUActList[index + 1][start] = currDate

                actData.HUActList[index][end] = nextDate
                actData.HUActList[index + 1][end] = nextDate

                # actData.RNTActList[index][start] = currDate   # Roots and Traditions
                # actData.RNTActList[index + 1][start] = currDate

                # actData.RNTActList[index][end] = nextDate
                # actData.RNTActList[index + 1][end] = nextDate

                #remove_key_values_from_dictionary(actData.HUActList[index])
                #remove_key_values_from_dictionary(actData.HUActList[index + 1])
                #remove_key_values_from_dictionary(actData.RNTActList[index])
                #remove_key_values_from_dictionary(actData.RNTActList[index + 1])

                if currDate > currentDate and (grade_changed == True or subscribed == True):
                    self.fullActList.append(actData.HUActList[index].copy())
                    self.fullActList.append(actData.HUActList[index + 1].copy())

                    # self.fullActList.append(actData.RNTActList[index].copy())
                    # self.fullActList.append(actData.RNTActList[index + 1].copy())
            index += 2


    def GenerateWeeklyActivities(self):
        weeks = int(dayDifference / 7) + 1 # Find num of weeks (give 1 week less so we have to add 1 to it since half a week is taken as 0 week but we want it as 1 week)

        tempLHActList = FilterFunctions.focus_area(actData.LHActList, focusWeek)
        tempIPGActList = FilterFunctions.focus_area(actData.IPGActList, focusWeek)
        tempPGList = FilterFunctions.focus_area(actData.PGActList, focusWeek)

        for i in range(weeks): # start to end date number of weeks
            currDate = startDate + relativedelta(weeks=i, seconds=30)
            nextDate = min_date(currDate + relativedelta(days=6, hours=23, minutes=59), endDate) # seconds=0

            focusWeek = self.focusAreaWeekly[i % 12]

            if grade in ("3", "4", "5"): # Interpersonal Growth (once a week)
                tempIPGAct = random.choice(tempIPGActList)

                for _ in range(1000):
                    if tempIPGAct["activity_id"] not in self.actDone:
                        break
                    tempIPGAct = random.choice(tempIPGActList)

                self.actDone.append(tempIPGAct["activity_id"])

                tempIPGAct[start] = currDate
                tempIPGAct[end] = nextDate
                self.fullActList.append(tempIPGAct.copy())
            
            elif grade in ("6", "7", "8", "9"): # (once every 2 weeks)
                if i % 2 == 0:
                    tempIPGAct = random.choice(tempIPGActList)

                    for _ in range(1000):
                        if tempIPGAct["activity_id"] not in self.actDone:
                            break
                        tempIPGAct = random.choice(tempIPGActList)

                    self.actDone.append(tempIPGAct["activity_id"])

                    tempIPGAct[start] = currDate
                    tempIPGAct[end] = min_date(currDate + relativedelta(days=13, hours=23, minutes=59), endDate)
                    self.fullActList.append(tempIPGAct.copy())
            
            if grade in ("8", "9"): # Personal Growth
                tempPGAct = random.choice(tempPGList)

                for _ in range(1000):
                    if tempPGAct["activity_id"] not in self.actDone:
                        break
                    tempPGAct = random.choice(tempPGList)

                self.actDone.append(tempPGAct["activity_id"])

                tempPGAct[start] = currDate
                tempPGAct[end] = nextDate

                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                if currDate > currentDate:
                    self.fullActList.append(tempPGAct.copy())

            if grade in ("8", "9"): # life hacks (once a week)
                tempLHAct = random.choice(tempLHActList)

                for _ in range(1000):
                    if tempLHAct["activity_id"] not in self.actDone:
                        break
                    tempLHAct = random.choice(tempLHActList)

                self.actDone.append(tempLHAct["activity_id"])

                tempLHAct[start] = currDate
                tempLHAct[end] = nextDate
                if subscribed == False and (grade_changed == False and focus_changed == False):
                    continue

                if currDate > currentDate:
                    self.fullActList.append(tempLHAct.copy())
            
            elif grade in ("3", "4", "5", "6", "7"): # (once every 2 weeks)
                if i % 2 == 0:
                    tempLHAct = random.choice(tempLHActList)

                    for _ in range(1000):
                        if tempLHAct["activity_id"] not in self.actDone:
                            break
                        tempLHAct = random.choice(tempLHActList)

                    self.actDone.append(tempLHAct["activity_id"])

                    tempLHAct[start] = currDate
                    tempLHAct[end] = min_date(currDate + relativedelta(days=13, hours=23, minutes=59), endDate)

                    if subscribed == False and (grade_changed == False and focus_changed == False):
                        continue

                    if currDate > currentDate:
                        self.fullActList.append(tempLHAct.copy())
                
    def GenerateQuarterlyActivities(self):
        if grade not in ("N", "Jr", "Sr", "1", "2"):
            tempLHActList = actData.LHActList
            tempLHAct = random.choice(tempLHActList)

            for _ in range(1000):
                if tempLHAct["activity_id"] not in self.actDone and tempLHAct["act_frequency_id"] == 1: # this number should be for quarterly frequency
                    break
                tempLHAct = random.choice(tempLHActList)

            self.actDone.append(tempLHAct["activity_id"])

            tempLHAct[start] = startDate
            tempLHAct[end] = endDate

            if subscribed == False and (grade_changed == False and focus_changed == False):
                return

            self.fullActList.append(tempLHAct.copy())
    
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
        self.GenerateShloks()
    
    def AddExistingActivitiesToExclude(self, activities: list):
        for i in activities:
            self.actDone.append(i["activity_id"])


startDate = datetime.datetime.now() #datetime.datetime(2024, 6, 1)
endDate = startDate + relativedelta(months=3)
dayDifference = (endDate - startDate).days # - 84 # 84 days = 12 weeks

# MAIN INPUT VARIABLES
pin_code = 411038
religion = "Hindu" # jai shree ram
grade_num = int(sys.argv[2])  # 1 -> N, 2 -> Jr etc
grade = ""
focus_area = ["A", "B", "C", "D", "E", "F"]
gender = "MALE"
language = "english"
child_id = sys.argv[1]

quarter = 1

currentDate = datetime.datetime(2024, 6, 1)
subscribed = True
grade_changed = False
focus_changed = False

map_grade = ["N", "Jr", "Sr"] # = [1,2,3] grade_num
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

def authorize(token):
    if token != "":
        raise "dfg"

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

actListRef = []

# with open("table1.csv") as activities_data:  # 1 -> habit up, 2 -> rnt, 4 -> CC  (act_category_id)
#     data = csv.DictReader(activities_data)
#     for i in data:
#         actListRef.append(i)
#     print(actListRef[0])

Conn = Connection()

actListRef = Conn.get_activities(grade_num)
mudras = Conn.get_mudras()
# print(actListRef[0])
# exit()

count = 0
for k in actListRef:
    id = int(k["act_category_id"])
    # print(count)
    count += 1
    if id == 1:
        actData.HUActList.append(k)
    elif id == 2:
        actData.RNTActList.append(k)
    elif id == 3:
        actData.WordleList.append(k)
    elif id == 4:
        actData.CCActList.append(k)
    elif id == 5:
        actData.PGActList.append(k)
    elif id == 6:
        actData.IPGActList.append(k)
    elif id == 7:
        actData.LHActList.append(k)

# Connection = connection()
# print(Connection.get_table_data("child_activity")[0])
# Connection.get_table_data("activity")
wordle_words_list = Conn.get_wordle_words(startDate, endDate, grade_num) #Connection.get_wordle_words(startDate, endDate, grade_num) # get data from wordle_word db
# print(len(wordle_words_list), dayDifference, end='\n')
# print(wordle_words_list[0], end='\n')
# print(wordle_words_list[-1], end='\n')

Generator = GenerateActivities()
Generator.AddExistingActivitiesToExclude(Conn.get_child_activity_table_activities(child_id))#Connection.get_table_data("child_activity"))
# Generator.GenerateDailyActivities()
# Generator.GenerateWeeklyActivities()
# Generator.GenerateMudras()
Generator.GenerateActivities()

#print(Generator.fullActList)

# tempArr = []

# for i in Generator.fullActList:
#     tempArr.append(i)


Conn.dump_data_in_child_activity(fullActList=Generator.fullActList, child_id=child_id)

# tempArr = convert_all_values_to_json_readable(tempArr)

# json.dump(len(tempArr), sys.stdout, indent=4)
# print("\n" + str(grade))
