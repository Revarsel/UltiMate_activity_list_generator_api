import datetime
from connection import Connection
from dateutil.relativedelta import relativedelta
import random

start = "start_date" # one var for the key "Start Date"
end = "end_date" # one var for the key "End Date"
focus_string = "focus" # one var for the key "focus"

def filter_mudra(val):
    if val["act_category_id"] == 2 and val["activity_game_type_id"] == 5:
        return True
    return False

def min_date(date1: datetime.datetime, date2: datetime.datetime):

    if date1 < date2:
        return date1
    else: 
        return date2

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

class FilterFunctions:
    def focus_area(list, focus) -> list:
        # tempArr = []
        # for k in list:
        #     if k["focus_area_id"] == focus:
        #         tempArr.append(k)
        # return tempArr
        return list

class GenerateActivities:
    def __init__(self, child_id, Conn: Connection, trial: bool) -> None:
        self.actData = ActivityData()

        self.Conn = Conn

        self.child_id = child_id
        child_details = self.Conn.get_child_details(child_id)
        self.user_id = int(child_details["user_id"])
        self.grade_num = int(child_details["standard_id"])  # 1 -> N, 2 -> Jr etc

        self.grade = ""

        map_grade = ["N", "Jr", "Sr"] # = [1,2,3] grade_num
        if self.grade_num - 3 < 0:
            self.grade = map_grade[self.grade_num]
        else:
            self.grade = str(self.grade_num-3)
        
        self.shloks = []
        if self.grade_num >= 3:
            self.shloks = self.Conn.get_shloks(3)
        elif self.grade_num < 3:
            self.shloks = self.Conn.get_shloks(1)
        
        subscription = []
        if trial == False:
            subscription = self.Conn.get_subscription_from_child_id(self.child_id) # returns all subscriptions of the user in descending order
            if len(subscription) == 0:
                raise Exception("No subscription found!")
        
            start_date: datetime.datetime = subscription[0]["start_date"]
            end_date: datetime.datetime = subscription[0]["end_date"]
        else:
            start_date: datetime.datetime = datetime.datetime.now()
            end_date: datetime.datetime = datetime.datetime.now() + relativedelta(days=7)

        weeks_completed_already = 0
        if trial == True:
            if len(subscription) > 1:
                for index, value in enumerate(subscription[1:]):
                    weeks = 0
                    sub_start: datetime.datetime = value["start_date"]
                    sub_end: datetime.datetime = value["end_date"]
                    weeks = int(((sub_end-sub_start).days)/7)
                    weeks_completed_already += weeks
        
        # start_date = datetime.datetime.now()
        # end_date = datetime.datetime.now() + relativedelta(months=3)

        if trial:
            actListBothGrade = self.Conn.get_trial_activities(self.grade_num)
            self.mudras = self.Conn.get_trial_mudras()
        else:
            actListBothGrade = self.Conn.get_activities(self.grade_num)
            self.mudras = self.Conn.get_mudras()

        actListRefCurrGrade = actListBothGrade[0]
        actListRefPrevGrade = actListBothGrade[1]

        for k in actListRefCurrGrade:
            id = int(k["act_category_id"])

            if id == 1:
                self.actData.HUActList[0].append(k)
            elif id == 2:
                self.actData.RNTActList[0].append(k)
            elif id == 3:
                self.actData.WordleList[0].append(k)
            elif id == 4:
                self.actData.CCActList[0].append(k)
            elif id == 5:
                self.actData.PGActList[0].append(k)
            elif id == 6:
                self.actData.IPGActList[0].append(k)
            elif id == 7:
                self.actData.LHActList[0].append(k)

        for k in actListRefPrevGrade:
            id = int(k["act_category_id"])

            if id == 1:
                self.actData.HUActList[1].append(k)
            elif id == 2:
                self.actData.RNTActList[1].append(k)
            elif id == 3:
                self.actData.WordleList[1].append(k)
            elif id == 4:
                self.actData.CCActList[1].append(k)
            elif id == 5:
                self.actData.PGActList[1].append(k)
            elif id == 6:
                self.actData.IPGActList[1].append(k)
            elif id == 7:
                self.actData.LHActList[1].append(k)

        self.startDate = start_date
        self.endDate = end_date
        self.dayDifference = (self.endDate - self.startDate).days

        weeks_num = int(self.dayDifference/7) + 1

        focusAreaFrequency = Conn.get_focus_area_frequency(self.grade_num)
        self.focusAreaWeekly = focusAreaFrequency[weeks_completed_already:weeks_completed_already+weeks_num] #tempArrWeekly

        # print(weeks_num)
        # print(focusAreaFrequency)
        # print(self.focusAreaWeekly)

        # self.focusArea2PerWeek = tempArr2PerWeek #Conn.get_focus_area_frequency(grade_num)[:weeks_num*2] #tempArr2PerWeek
        self.fullActList = []
        self.actDone = [] # this stores all activity ids to check for duplicates in the following activity generators
        self.monthDays = []
        if trial:
            self.monthDays.append(7)
        else:
            for j in range(1, (weeks_num%4)):
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

            if self.grade in ("N", "Jr", "Sr", "1", "2"): # Creative Corner
                tempCCList = []
                prev = True
                if len(self.actData.CCActList[1]) == 0: # previous self.grade activities are empty
                    prev = False
                    tempCCList = FilterFunctions.focus_area(self.actData.CCActList[0], focus)
                else:
                    tempCCList = FilterFunctions.focus_area(self.actData.CCActList[1], focus)
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
                    self.actData.CCActList[1] = custom_remove(self.actData.CCActList[1], tempCCAct)
                else:
                    self.actData.CCActList[0] = custom_remove(self.actData.CCActList[0], tempCCAct)
            
            elif self.grade in ("3", "4", "5", "6", "7"): # Personal Growth
                tempPGList = []
                prev = True
                if len(self.actData.PGActList[1]) == 0: # previous self.grade activities are empty
                    prev = False
                    tempPGList = FilterFunctions.focus_area(self.actData.PGActList[0], focus)
                else:
                    tempPGList = FilterFunctions.focus_area(self.actData.PGActList[1], focus)
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
                    self.actData.PGActList[1] = custom_remove(self.actData.PGActList[1], tempPGAct)
                else:
                    self.actData.PGActList[0] = custom_remove(self.actData.PGActList[0], tempPGAct)
        
        index = 0
        for months in range(len(self.monthDays)):
            for currDay in range(self.monthDays[months]):
                currDate = self.startDate + relativedelta(months=months, days=currDay, second=30)
                nextDate = currDate + relativedelta(hours=23, minutes=59, seconds=29)  # days=currDay
                print(self.actData.HUActList)

                self.actData.HUActList[0][index][start] = currDate   # Habit Up
                self.actData.HUActList[0][index + 1][start] = currDate

                self.actData.HUActList[0][index][end] = nextDate
                self.actData.HUActList[0][index + 1][end] = nextDate

                # self.actData.RNTActList[index][start] = currDate   # Roots and Traditions
                # self.actData.RNTActList[index + 1][start] = currDate

                # self.actData.RNTActList[index][end] = nextDate
                # self.actData.RNTActList[index + 1][end] = nextDate

                self.fullActList.append(self.actData.HUActList[0][index].copy())
                self.fullActList.append(self.actData.HUActList[0][index + 1].copy())

                # self.fullActList.append(self.actData.RNTActList[index].copy())
                # self.fullActList.append(self.actData.RNTActList[index + 1].copy())
            index += 2


    def GenerateWeeklyActivities(self):
        weeks = int(self.dayDifference / 7) + 1 # Find num of weeks (give 1 week less so we have to add 1 to it since half a week is taken as 0 week but we want it as 1 week)

        for i in range(weeks): # start to end date number of weeks
            focus = self.focusAreaWeekly[i]
            currDate = self.startDate + relativedelta(weeks=i, seconds=30)
            nextDate = min_date(currDate + relativedelta(days=6, hours=23, minutes=59), self.endDate) # seconds=0

            if self.grade in ("3", "4", "5"): # Interpersonal Growth (once a week)
                tempIPGList = []
                prev = True
                if len(self.actData.IPGActList[1]) == 0: # previous self.grade activities are empty
                    prev = False
                    tempIPGList = FilterFunctions.focus_area(self.actData.IPGActList[0], focus)
                else:
                    tempIPGList = FilterFunctions.focus_area(self.actData.IPGActList[1], focus)
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
                    self.actData.IPGActList[1] = custom_remove(self.actData.IPGActList[1], tempIPGAct)
                else:
                    self.actData.IPGActList[0] = custom_remove(self.actData.IPGActList[0], tempIPGAct)
            
            elif self.grade in ("6", "7", "8", "9"): # (once every 2 weeks)
                if i % 2 == 0:
                    tempIPGList = []
                    prev = True
                    if len(self.actData.IPGActList[1]) == 0: # previous self.grade activities are empty
                        prev = False
                        tempIPGList = FilterFunctions.focus_area(self.actData.IPGActList[0], focus)
                    else:
                        tempIPGList = FilterFunctions.focus_area(self.actData.IPGActList[1], focus)
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
                        self.actData.IPGActList[1] = custom_remove(self.actData.IPGActList[1], tempIPGAct)
                    else:
                        self.actData.IPGActList[0] = custom_remove(self.actData.IPGActList[0], tempIPGAct)
            
            if self.grade in ("8", "9"): # Personal Growth
                tempPGList = []
                prev = True
                if len(self.actData.PGActList[1]) == 0: # previous self.grade activities are empty
                    prev = False
                    tempPGList = FilterFunctions.focus_area(self.actData.PGActList[0], focus)
                else:
                    tempPGList = FilterFunctions.focus_area(self.actData.PGActList[1], focus)
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
                    self.actData.PGActList[1] = custom_remove(self.actData.PGActList[1], tempPGAct)
                else:
                    self.actData.PGActList[0] = custom_remove(self.actData.PGActList[0], tempPGAct)

            if self.grade in ("8", "9"): # life hacks (once a week)
                tempLHList = []
                prev = True
                if len(self.actData.LHActList[1]) == 0: # previous self.grade activities are empty
                    prev = False
                    tempLHList = FilterFunctions.focus_area(self.actData.LHActList[0], focus)
                else:
                    tempLHList = FilterFunctions.focus_area(self.actData.LHActList[1], focus)
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
                    self.actData.LHActList[1] = custom_remove(self.actData.LHActList[1], tempLHAct)
                else:
                    self.actData.LHActList[0] = custom_remove(self.actData.LHActList[0], tempLHAct)
            
            elif self.grade in ("3", "4", "5", "6", "7"): # (once every 2 weeks)
                if i % 2 == 0:
                    tempLHList = []
                    prev = True
                    if len(self.actData.LHActList[1]) == 0: # previous self.grade activities are empty
                        prev = False
                        tempLHList = FilterFunctions.focus_area(self.actData.LHActList[0], focus)
                    else:
                        tempLHList = FilterFunctions.focus_area(self.actData.LHActList[1], focus)
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
                        self.actData.LHActList[1] = custom_remove(self.actData.LHActList[1], tempLHAct)
                    else:
                        self.actData.LHActList[0] = custom_remove(self.actData.LHActList[0], tempLHAct)
                
    def GenerateQuarterlyActivities(self):
        if self.grade not in ("N", "Jr", "Sr", "1", "2"):
            focus = self.focusAreaWeekly[0]
            tempLHList = []
            prev = True
            if len(self.actData.LHActList[1]) == 0: # previous self.grade activities are empty
                prev = False
                tempLHList = FilterFunctions.focus_area(self.actData.LHActList[0], focus)
            else:
                tempLHList = FilterFunctions.focus_area(self.actData.LHActList[1], focus)
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
                self.actData.LHActList[1] = custom_remove(self.actData.LHActList[1], tempLHAct)
            else:
                self.actData.LHActList[0] = custom_remove(self.actData.LHActList[0], tempLHAct)
            
            ################################################

            # tempLHActList = self.actData.LHActList
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

        existing_mudras: list = self.Conn.get_child_activities_with_activity_table(self.child_id)

        existing_mudras = list(filter(filter_mudra, existing_mudras))

        for i in range(weeks):
            if i % 2 == 1:
                continue
            rand_mudra = random.choice(self.mudras)
            for _ in range(1000):
                if rand_mudra["activity_id"] not in self.actDone:
                    break
                rand_mudra = random.choice(self.mudras)
            
            rand_mudra["start_date"] = currDate
            rand_mudra["end_date"] = nextDate
            currDate = nextDate
            nextDate = min_date(self.endDate, currDate + relativedelta(weeks=2))
            self.fullActList.append(rand_mudra.copy())
    
    def GenerateShloks(self):
        next_shlok = self.shloks[0]
        for i in self.shloks:
            if int(i["sequence"]) == 1:
                next_shlok = i
                next_shlok["start_date"] = self.startDate
                next_shlok["end_date"] = self.startDate + relativedelta(weeks=2)
                break

        self.fullActList.append(next_shlok)

    def GenerateActivities(self):
        # self.AddExistingActivitiesToExclude()
        self.GenerateDailyActivities()
        self.GenerateWeeklyActivities()
        self.GenerateQuarterlyActivities()
        self.GenerateMudras()
        # if is_new_user:
        self.GenerateShloks()
    
    def AddExistingActivitiesToExclude(self):
        activities = self.Conn.get_child_activity_table_activities(self.child_id)
        for i in activities:
            self.actDone.append(i["activity_id"])