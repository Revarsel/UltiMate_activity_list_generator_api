import random
import json
import datetime
from dateutil.relativedelta import relativedelta
from connection import Connection, convert_all_values_to_json_readable
import sys

if len(sys.argv) == 1:
    print("Provide A child_id To Fill Activities In")
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
    def __init__(self, start_date=datetime.datetime.now(), end_date=datetime.datetime.now()+relativedelta(months=3), weeks_completed=0) -> None:
        self.startDate = start_date
        self.endDate = end_date
        self.dayDifference = (self.endDate - self.startDate).days # - 84 # 84 days = 12 weeks

        weeks_num = int(self.dayDifference/7) + 1

        focusAreaFrequency = Conn.get_focus_area_frequency(grade_num)
        self.focusAreaWeekly = focusAreaFrequency[weeks_completed:weeks_completed+weeks_num+1] #tempArrWeekly

        # print(weeks_num)
        # print(focusAreaFrequency)
        # print(self.focusAreaWeekly)

        # self.focusArea2PerWeek = tempArr2PerWeek #Conn.get_focus_area_frequency(grade_num)[:weeks_num*2] #tempArr2PerWeek
        self.fullActList = []
        self.monthDays = []
        self.actDone = [] # this stores all activity ids to check for duplicates in the following activity generators
        for j in range(1, 4):
            monthPrev = self.startDate + relativedelta(months=max((j-1), 0))
            monthNext = self.startDate + relativedelta(months=j)
            dayDiff = (monthNext - monthPrev).days
            self.monthDays.append(dayDiff)
    
    def GenerateDailyActivities(self):
        discuss = 0 # 0 = False, 1 = True

        for b in range(self.dayDifference):
            currDate = self.startDate + relativedelta(days=b, second=30)
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
                currDate = self.startDate + relativedelta(months=months, days=currDay, second=30)
                nextDate = currDate + relativedelta(hours=23, minutes=59, seconds=29)  # days=currDay

                actData.HUActList[0][index][start] = currDate   # Habit Up
                actData.HUActList[0][index + 1][start] = currDate

                actData.HUActList[0][index][end] = nextDate
                actData.HUActList[0][index + 1][end] = nextDate

                # actData.RNTActList[index][start] = currDate   # Roots and Traditions
                # actData.RNTActList[index + 1][start] = currDate

                # actData.RNTActList[index][end] = nextDate
                # actData.RNTActList[index + 1][end] = nextDate

                self.fullActList.append(actData.HUActList[0][index].copy())
                self.fullActList.append(actData.HUActList[0][index + 1].copy())

                # self.fullActList.append(actData.RNTActList[index].copy())
                # self.fullActList.append(actData.RNTActList[index + 1].copy())
            index += 2


    def GenerateWeeklyActivities(self):
        weeks = int(self.dayDifference / 7) + 1 # Find num of weeks (give 1 week less so we have to add 1 to it since half a week is taken as 0 week but we want it as 1 week)

        for i in range(weeks): # start to end date number of weeks
            focus = self.focusAreaWeekly[i]
            currDate = self.startDate + relativedelta(weeks=i, seconds=30)
            nextDate = min_date(currDate + relativedelta(days=6, hours=23, minutes=59), self.endDate) # seconds=0

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
                if nextDate == None:
                    print(tempIPGAct)
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

            tempLHAct[start] = self.startDate
            tempLHAct[end] = self.endDate

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
        weeks = int(self.dayDifference / 7) + 1
        currDate = self.startDate
        nextDate = currDate + relativedelta(weeks=2)

        existing_mudras: list = Conn.get_child_activities_with_activity_table(child_id)

        existing_mudras = list(filter(filter_mudra, existing_mudras))

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
            nextDate = min_date(self.endDate, currDate + relativedelta(weeks=2))
            self.fullActList.append(rand_mudra.copy())
    
    def GenerateShloks(self):
        shloks = Conn.get_shloks()

        next_shlok = shloks[0]
        for i in shloks:
            if int(i["sequence"]) == 1:
                next_shlok = i
                next_shlok["start_date"] = self.startDate
                next_shlok["end_date"] = self.startDate + relativedelta(weeks=2)
                break

        self.fullActList.append(next_shlok)

    def GenerateActivities(self):
        self.GenerateDailyActivities()
        self.GenerateWeeklyActivities()
        self.GenerateQuarterlyActivities()
        self.GenerateMudras()
        # if is_new_user:
        self.GenerateShloks()
    
    def AddExistingActivitiesToExclude(self, activities: list):
        for i in activities:
            self.actDone.append(i["activity_id"])

class FilterFunctions:
    def focus_area(list, focus) -> list:
        tempArr = []
        for k in list:
            if k["focus_area_id"] == focus:
                tempArr.append(k)
        return tempArr
        # return list

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


def min_date(date1: datetime.datetime, date2: datetime.datetime):

    if date1 < date2:
        return date1
    else: 
        return date2

    # year1 = date1.year
    # year2 = date2.year
    # if year2 > year1:
    #     return date1
    # elif year2 < year1:
    #     return date2
    
    # month1 = date1.month
    # month2 = date2.month
    # if month2 > month1:
    #     return date1
    # elif month2 < month1:
    #     return date2

    # day1 = date1.day
    # day2 = date2.day
    # if day2 > day1:
    #     return date1
    # elif day2 < day1:
    #     return date2

def is_in_actDone(generator: GenerateActivities, act_id):
    return (act_id in generator.actDone)

def filter_mudra(val):
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

Conn = Connection()

for child_num in range(1, len(sys.argv)):
    print(child_num)

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

    actListBothGrade = Conn.get_activities(grade_num)
    mudras = Conn.get_mudras()
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
