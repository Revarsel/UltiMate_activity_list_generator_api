import random
import json
import datetime
import csv
from dateutil.relativedelta import relativedelta

class ActivityData:
    data = 1
    def __init__(self) -> None:
        self.HUActList = []
        self.RNTActList = []
        self.CCActList = []
        self.ExpActList = []
        self.FortnightAct = []
        self.WeeklyAct = []
    
    # def AppendHU(self, data_to_append):
    #     self.HUActList.append(data_to_append)
    
    # def AppendRNT(self, data_to_append):
    #     self.RNTActList.append(data_to_append)
    
    # def AppendCC(self, data_to_append):
    #     self.CCActList.append(data_to_append)
    
    # def AppendHU(self, data_to_append):
    #     self.ExpActList.append(data_to_append)

act_data = ActivityData()

class ActivityGeneratorNToSr:
    def __init__(self, focus_areas, start_date) -> None:
        self.FullActList = {}
        self.WeekActList = {}
        self.DayActList = {}
        self.CurrWeek = 1
        self.CurrMonth = 1
        self.focus_index = 0
        self.focus_areas = focus_areas
        self.focus = self.focus_areas[self.focus_index]
        self.focus_next = self.focus_areas[self.focus_index + 1]
        self.focus_num = 0
        self.start_date = start_date
        self.endDate = startDate + relativedelta(months=3)

        diff = endDate - startDate # DAYS DIFFERENCE START DATE AND END DATE
        
        self.difference = diff.days - 84 # 84 = 12 (weeks) X 7 (days)

        self.FortnightAct = {}
        self.WeeklyAct = {}

        self.TempExpAct = {}

        self.index = 1

    def GenerateWeekActivities(self):
        for i in range(1, 8): # 7 DAYS
            self.DayActList["Fortnightly"] = [self.FortnightAct]
            self.DayActList["Weekly"] = [self.WeeklyAct]

            #print(len(act_data.HUActList))

            self.DayActList["Habit Up"] = [act_data.HUActList[2 * (self.CurrMonth-1)]["activity_id"], act_data.HUActList[2 * (self.CurrMonth-1) + 1]["activity_id"]] # habit up

            self.DayActList["Roots And Tradition"] = [act_data.RNTActList[2 * (self.CurrMonth-1)], act_data.RNTActList[2 * (self.CurrMonth-1) + 1]] # roots and tradition

            tempCCAct = random.choice(act_data.CCActList)
            for _ in range(len(act_data.CCActList)):
                if tempCCAct in act_data.CCActList:
                    tempCCAct = random.choice(act_data.CCActList)
                else:
                    break

            self.DayActList["Creative Corner"] = [(tempCCAct + ", Focus : " + self.focus_areas[self.focus_num])] # creative corner

            temparr = []
            for _ in range(self.index):
                b = 0
                temparr.append((self.TempExpAct[b] + ", Focus : " + self.focus))
                temparr.append((self.TempExpAct[b + 1] + ", Focus : " + self.focus_next))
                b += 2
            self.DayActList["Learning Through Exploring"] = temparr #[(self.TempExpAct[0] + ", Focus : " + self.focus), (self.TempExpAct[1] + ", Focus : " + self.focus_next)] # Learning through exploring

            day = "Day " + str(i)

            self.WeekActList[day] = self.DayActList.copy()
            self.DayActList.clear()
    
    def GenerateMonthActivities(self):
        for i in range(1, 5): # 4 WEEKS
            self.FortnightAct = act_data.FortnightAct[int((i-1)/2)]
            
            self.WeeklyAct = act_data.WeeklyAct[i-1]

            if (i-1) % 2 == 0:
                self.focus_num = self.focus_index
            elif (i-1) % 2 == 1:
                self.focus_num = self.focus_index + 1

            self.focus = self.focus_areas[self.focus_index]
            self.focus_next = self.focus_areas[self.focus_index + 1]

            self.index = 1
            if grade in ("1", "2"):
                self.index = 2
            
            for _ in range(self.index):
                b = 0
                self.TempExpAct[b] = random.choice(act_data.ExpActList)
                self.TempExpAct[b + 1] = random.choice(act_data.ExpActList)
                for _ in range(len(act_data.ExpActList)):
                    if self.TempExpAct[b] in act_data.ExpActList:
                        self.TempExpAct[b] = random.choice(act_data.ExpActList)
                    elif self.TempExpAct[b + 1] in act_data.ExpActList and self.TempExpAct[1] != self.TempExpAct[0]:
                        self.TempExpAct[b + 1] = random.choice(act_data.ExpActList)
                    else:
                        break
                b += 2
            
            self.GenerateWeekActivities()

            week = "Week " + str(self.CurrWeek)

            self.FullActList[week] = self.WeekActList.copy()
            self.CurrWeek += 1
        
        self.focus_index += 2
        self.CurrMonth += 1
    
    # def GenerateRemainingActivities(self):
    #     self.focus = self.focus_areas[0]
    #     self.focus_next = self.focus_areas[1]
    #     #print(self.difference)
    #     for d in range(min(self.difference, 7)):
    #         self.FortnightAct = None
    #         self.WeeklyAct = None

    #         self.DayActList["Fortnightly"] = [self.FortnightAct]
    #         self.DayActList["Weekly"] = [self.WeeklyAct]

    #         self.DayActList["Habit Up"] = [act_data.HUActList[0]["activity_id"], act_data.HUActList[1]["activity_id"]]
    #         self.DayActList["Roots And Tradition"] = [act_data.RNTActList[0], act_data.RNTActList[1]]

    #         tempCCAct = random.choice(act_data.CCActList)
    #         for _ in range(len(act_data.CCActList)):
    #             if tempCCAct in act_data.CCActList:
    #                 tempCCAct = random.choice(act_data.CCActList)
    #             else:
    #                 break

    #         self.DayActList["Creative Corner"] = [(tempCCAct + ", Focus : " + self.focus)] # creative corner

    #         self.TempExpAct1 = random.choice(act_data.ExpActList)
    #         self.TempExpAct2 = random.choice(act_data.ExpActList)
    #         for _ in range(len(act_data.ExpActList)):
    #             if self.TempExpAct1 in act_data.ExpActList:
    #                 self.TempExpAct1 = random.choice(act_data.ExpActList)
    #             elif self.TempExpAct2 in ExpActList and self.TempExpAct2 != self.TempExpAct1:
    #                 self.TempExpAct2 = random.choice(act_data.ExpActList)
    #             else:
    #                 break

    #         self.DayActList["Learning Through Exploring"] = [(self.TempExpAct1 + ", Focus : " + self.focus), (self.TempExpAct2 + ", Focus : " + self.focus_next)] # Learning through exploring

    #         day = "Day " + str(d + 1)

    #         week = "Week " + str(self.CurrWeek)

    #         self.WeekActList[day] = self.DayActList.copy()
    #         self.DayActList.clear()

    #     self.FullActList[week] = self.WeekActList.copy()
    #     self.WeekActList.clear()

    #     self.CurrWeek += 1
        
        
    #     if difference > 7:
    #         self.DayActList["Fortnightly"] = [self.FortnightAct]
    #         self.DayActList["Weekly"] = [self.WeeklyAct]

    #         self.DayActList["Habit Up"] = [act_data.HUActList[0]["activity_id"], act_data.HUActList[1]["activity_id"]]
    #         self.DayActList["Roots And Tradition"] = [act_data.RNTActList[0], act_data.RNTActList[1]]

    #         tempCCAct = random.choice(act_data.CCActList)
    #         for _ in range(len(act_data.CCActList)):
    #             if tempCCAct in act_data.CCActList:
    #                 tempCCAct = random.choice(act_data.CCActList)
    #             else:
    #                 break

    #         self.DayActList["Creative Corner"] = [(tempCCAct + ", Focus : " + self.focus_next)] # creative corner

    #         self.TempExpAct1 = random.choice(act_data.ExpActList)
    #         self.TempExpAct2 = random.choice(act_data.ExpActList)
    #         for _ in range(len(act_data.ExpActList)):
    #             if self.TempExpAct1 in act_data.ExpActList:
    #                 self.TempExpAct1 = random.choice(act_data.ExpActList)
    #             elif self.TempExpAct2 in act_data.ExpActList and self.TempExpAct2 != self.TempExpAct1:
    #                 self.TempExpAct2 = random.choice(act_data.ExpActList)
    #             else:
    #                 break

    #         self.DayActList["Learning Through Exploring"] = [(self.TempExpAct1 + ", Focus : " + self.focus), (self.TempExpAct2 + ", Focus : " + self.focus_next)] # Learning through exploring

    #         day = "Day 1"

    #         self.WeekActList[day] = self.DayActList.copy()
    #         self.DayActList.clear()

    #         week = "Week " + str(self.CurrWeek)

    #         self.FullActList[week] = self.WeekActList.copy()
    #         self.WeekActList.clear()
    
    def GenerateActivities(self):
        for _ in range(1, 5): # 4 MONTHS
            self.GenerateMonthActivities()
        #self.GenerateRemainingActivities()

HUActList = [] # ["h act1", "h act2", "h act3", "h act4", "h act5", "h act6"]  
RNTActList = [] # ["rnt act1", "rnt act2", "rnt act3", "rnt act4", "rnt act5", "rnt act6"]
CCActList = [("CC " + str(r)) for r in range(91)]
ExpActList = [("EXP " + str(r)) for r in range(91)]
fortnightly = ["Fort 1", "Fort 2"]
weeklyAct = ["week 1", "week 2", "week 3", "week 4"]

act_data.CCActList = CCActList
act_data.ExpActList = ExpActList
act_data.FortnightAct = fortnightly
act_data.WeeklyAct = weeklyAct

fullActList = {}  # Main huge list
tempActList= {}  # Temporary list for for loop which appends to dailyAct list

startDate = datetime.date(2024, 3, 1) # START DATE

endDate = startDate + relativedelta(months=3)

diff = endDate - startDate # DAYS DIFFERENCE START DATE AND END DATE
difference = diff.days - 84 # 84 = 12 (weeks) X 7 (days)

# MAIN INPUT VARIABLES
pin_code = 411038
religion = "Hindu" # jai shree ram
grade = "N"
focus_area = ["A", "B", "C", "D", "E", "F", "G", "H"]
gender = "MALE"
language = "english"

act_list_ref = []

with open("data-1716973262669.csv") as activities_data:  # 1 -> habit up, 2 -> rnt, 4 -> CC  (act_category_id)
    data = csv.DictReader(activities_data)
    for i in data:
        act_list_ref.append(i)

for k in act_list_ref:
    id = int(k["act_category_id"])
    if id == 1:
        act_data.HUActList.append(k)
    elif id == 2:
        act_data.RNTActList.append(k)
    elif id == 4:
        act_data.CCActList.append(k)

for i in range(1, 9):
    act_data.RNTActList.append("rnt act" + str(i))


def grade_filter(act_info_dict):
    if act_info_dict["standard_id"] == grade:
        return True
    return False

act_data.HUActList = list(filter(grade_filter, act_data.HUActList))

for i in range(1, 9): # PLACEHOLDER
    act_data.HUActList.append({"activity_id" : i})
# RNTActList = list(filter(grade_filter, RNTActList))
# CCActList = list(filter(grade_filter, CCActList))

# focus_index = 0
# for j in range(1, 4): # 3 MONTHS
#     for i in range(1, 5): # FIRST 4 WEEKS
#         loopActList = {}
#         fortnightAct = ""
#         weekAct = ""
#         fortnightAct = fortnightly[int((i-1)/2)]
        
#         weekAct = weeklyAct[i-1]

#         if ((i-1)) % 2 == 0:
#             focus_num = focus_index
#         elif (i-1) % 2 == 1:
#             focus_num = focus_index + 1

#         focus = focus_area[focus_num]
#         focus_next = focus_area[focus_num + 1]

#         tempExpAct1 = random.choice(ExpActList)
#         tempExpAct2 = random.choice(ExpActList)
#         for _ in range(len(ExpActList)):
#             if tempExpAct1 in ExpActList:
#                 tempExpAct1 = random.choice(ExpActList)
#             elif tempExpAct2 in ExpActList and tempExpAct2 != tempExpAct1:
#                 tempExpAct2 = random.choice(ExpActList)
#             else:
#                 break

#         for x in range(1, 8): # 7 DAYS
#             loopActList["Fortnightly"] = fortnightAct
#             loopActList["Weekly"] = weekAct

#             loopActList["Habit Up"] = [HUActList[2 * (j-1)], HUActList[2 * (j-1) + 1]] # habit up

#             loopActList["Roots And Tradition"] = [RNTActList[2 * (j-1)], RNTActList[2 * (j-1) + 1]] # roots and tradition

#             tempCCAct = random.choice(CCActList)
#             for _ in range(len(CCActList)):
#                 if tempCCAct in CCActList:
#                     tempCCAct = random.choice(CCActList)
#                 else:
#                     break

#             loopActList["Creative Corner"] = (tempCCAct + ", Focus : " + focus) # creative corner

#             loopActList["Learning Through Exploring"] = [(tempExpAct1 + ", Focus : " + focus), (tempExpAct2 + ", Focus : " + focus_next)] # Learning through exploring

#             day = "day " + str(x)

#             tempActList[day] = loopActList.copy()
#             loopActList.clear()


#         # once per 14 days

#         week = "week " + str(i + (4 * (j-1)))
#         fullActList[week] = tempActList.copy()

#         tempActList.clear()
#         break
#     focus_index += 2


# focus = focus_area[0]
# focus_next = focus_area[1]

# for d in range(min(difference, 7)):
#     fortnightAct = None
#     weekAct = None

#     loopActList["Fortnightly"] = fortnightAct
#     loopActList["Weekly"] = weekAct

#     loopActList["Habit Up"] = [HUActList[0], HUActList[1]]
#     loopActList["Roots And Tradition"] = [RNTActList[0], RNTActList[1]]

#     tempCCAct = random.choice(CCActList)
#     for _ in range(len(CCActList)):
#         if tempCCAct in CCActList:
#             tempCCAct = random.choice(CCActList)
#         else:
#             break

#     loopActList["Creative Corner"] = (tempCCAct + ", Focus : " + focus) # creative corner

#     tempExpAct1 = random.choice(ExpActList)
#     tempExpAct2 = random.choice(ExpActList)
#     for _ in range(len(ExpActList)):
#         if tempExpAct1 in ExpActList:
#             tempExpAct1 = random.choice(ExpActList)
#         elif tempExpAct2 in ExpActList and tempExpAct2 != tempExpAct1:
#             tempExpAct2 = random.choice(ExpActList)
#         else:
#             break

#     loopActList["Learning Through Exploring"] = [(tempExpAct1 + ", Focus : " + focus), (tempExpAct2 + ", Focus : " + focus_next)] # Learning through exploring

#     day = "day " + str(d + 1)

#     tempActList[day] = loopActList.copy()
#     loopActList.clear()

#     fullActList["week 13"] = tempActList.copy()
#     tempActList.clear()

# focus = focus_area[2]
# focus_next = focus_area[3]

# if difference > 7:
#     fortnightAct = None
#     weekAct = None

#     loopActList["Fortnightly"] = fortnightAct
#     loopActList["Weekly"] = weekAct

#     loopActList["Habit Up"] = [HUActList[0], HUActList[1]]
#     loopActList["Roots And Tradition"] = [RNTActList[0], RNTActList[1]]

#     tempCCAct = random.choice(CCActList)
#     for _ in range(len(CCActList)):
#         if tempCCAct in CCActList:
#             tempCCAct = random.choice(CCActList)
#         else:
#             break

#     loopActList["Creative Corner"] = (tempCCAct + ", Focus : " + focus) # creative corner

#     tempExpAct1 = random.choice(ExpActList)
#     tempExpAct2 = random.choice(ExpActList)
#     for _ in range(len(ExpActList)):
#         if tempExpAct1 in ExpActList:
#             tempExpAct1 = random.choice(ExpActList)
#         elif tempExpAct2 in ExpActList and tempExpAct2 != tempExpAct1:
#             tempExpAct2 = random.choice(ExpActList)
#         else:
#             break

#     loopActList["Learning Through Exploring"] = [(tempExpAct1 + ", Focus : " + focus), (tempExpAct2 + ", Focus : " + focus_next)] # Learning through exploring

#     day = "day 1"

#     tempActList[day] = loopActList.copy()
#     loopActList.clear()

#     fullActList["week 14"] = tempActList.copy()
#     tempActList.clear()

Generator = ActivityGeneratorNToSr(focus_area, startDate)
Generator.GenerateActivities()

fullActList = Generator.FullActList

fields = ["activity_id"]

with open("test.json", "w") as test:
    json.dump(fullActList, test)
    #print("dumped")

# with open("output.csv", 'w') as output:
#     csvwrite = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")

#     csvwrite.writeheader()

#     csvwrite.writerows(fullActList["week 1"]["day 1"]["Habit Up"])
