from sqlalchemy import create_engine, BigInteger, Boolean, Integer, VARCHAR, Column, TIMESTAMP, and_, Text, select
from sqlalchemy.orm import sessionmaker, declarative_base
from dateutil.relativedelta import relativedelta
import datetime

Base = declarative_base()

child_id_num = 1

user = "postgress"
passwd = "Shubham123"
host = "62.72.57.120"
port = "5432"
database = "ultimatedb"

class ChildActivity(Base):
    __tablename__ = "child_activity"

    child_activity_id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(BigInteger)
    child_id = Column(BigInteger)
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)
    activity_status_id = Column(BigInteger)
    act_start_time = Column(TIMESTAMP, nullable=True)
    act_completion_time = Column(TIMESTAMP, nullable=True)
    reassign_count = Column(Integer, nullable=True)
    activity_time_minutes = Column(Integer, nullable=True)
    wordle_words_id = Column(BigInteger, nullable=True)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, nullable=True, default=0)

class Activity(Base):
    __tablename__ = "activity"

    activity_id = Column(Integer, primary_key=True) #NOT NULL,
    title = Column(VARCHAR(50)) #NOT NULL,
    standard_id = Column(BigInteger) #NOT NULL,
    gender_id = Column(BigInteger) #NOT NULL,
    difficulty_level_id = Column(BigInteger, nullable=True)
    activity_game_type_id = Column(BigInteger, nullable=True)
    priority_id = Column(BigInteger) #NOT NULL,
    act_category_id = Column(BigInteger) #NOT NULL,
    parent_desc = Column(Text) #NOT NULL,
    child_desc = Column(Text, nullable=True)
    purpose_outcome = Column(Text, nullable=True)
    act_frequency_id = Column(BigInteger) #NOT NULL,
    points = Column(Integer) #NOT NULL,
    is_foundational = Column(Boolean) #NOT NULL,
    min_time_minutes = Column(Integer) #NOT NULL,
    max_time_minutes = Column(Integer) #NOT NULL,
    is_safety_risk = Column(Boolean) #NOT NULL,
    is_festival = Column(Boolean) #NOT NULL,
    festival_id = Column(BigInteger, nullable=True)
    is_discrematory = Column(Boolean) #NOT NULL,
    is_external_dependency = Column(Boolean) #NOT NULL,
    is_parent_supervision = Column(Boolean) #NOT NULL,
    is_parent_involment = Column(Boolean) #NOT NULL,
    parent_involment_level_id = Column(BigInteger, nullable=True)
    is_screen_time = Column(Boolean) #NOT NULL,
    screen_time_category_id = Column(BigInteger, nullable=True)
    is_negative_effects = Column(Boolean) #NOT NULL,
    is_free = Column(Boolean) #NOT NULL,
    is_archived = Column(Boolean) #NOT NULL,
    created_by = Column(VARCHAR(35)) #NOT NULL,
    updated_by = Column(VARCHAR(35), nullable=True) 
    created_date = Column(TIMESTAMP) #NOT NULL,
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class WordleWords(Base):
    __tablename__ = "wordle_words"

    wordle_words_id = Column(Integer, primary_key=True)
    word = Column(VARCHAR(5))
    standard_id = Column(BigInteger)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)
    word_show_date = Column(TIMESTAMP)

class Story(Base):
    __tablename__ = "story"

    story_id = Column(Integer, primary_key=True) #NOT NULL,
    title = Column(Text) #NOT NULL,
    is_festival = Column(Boolean, nullable=True)
    festival_id = Column(BigInteger, nullable=True)
    cover_image_path = Column(Text) #NOT NULL
    primary_language_id = Column(BigInteger) #NOT NULL
    primary_file_path = Column(Text, nullable=True)
    primary_audio_file_path = Column(Text, nullable=True)
    primary_question_pdf = Column(Text, nullable=True)
    min_time_minutes = Column(Integer) #NOT NULL
    max_time_minutes = Column(Integer) #NOT NULL
    points = Column(Integer) #NOT NULL
    week_num = Column(Integer) #NOT NULL
    standard_id = Column(BigInteger) #NOT NULL
    is_archived = Column(Boolean) #NOT NULL
    created_by = Column(VARCHAR(35)) #NOT NULL
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)  #NOT NULL
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

def convert_to_json_readable(data) -> dict:
    tempDict = {"DATA": []}

    for i in data:
        tempDict["DATA"].append(i)
    
    return tempDict

def get_result_as_dict(result):
    count = 0
    arr = []

    for i in result:
        count += 1
        tempdict: dict = i[0].__dict__.copy()
        key = list(tempdict.keys())

        tempdict.pop(key[0])

        arr.append(tempdict.copy())
    
    return (arr, count)

class Connection:
    def __init__(self) -> None:
        self.session = self.get_session()

    def get_engine(self):
        url = f"postgresql://{user}:{passwd}@{host}:{port}/{database}"
        # print(url)
        engine = create_engine(url, echo=False)
        return engine

    def get_session(self):
        session = sessionmaker(bind=self.get_engine())()
        return session

    def get_activity_pool_activities(self, activities, date):
        # date = datetime.datetime(2024, 7, 21)
        currDate = date
        CC = []
        daily = []
        weekly = []
        fortnightly = []
        activity_pool = []

        for i in activities:
            if i["act_category_id"] == 4:
                CC.append(i)

        # for i in activities:
        #     if i["start_date"] + relativedelta(days=1) > i["end_date"] and currDate > i["start_date"]: # get all daily activities
        #         daily.append(i)
        #     elif i["start_date"] + relativedelta(weeks=1) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
        #         weekly.append(i)
        #     elif i["start_date"] + relativedelta(weeks=2) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
        #         fortnightly.append(i)
            # else:
            #     print("not weekly or daily")
        
        for i in CC: # CC is daily
            if i["end_date"] < currDate and i["activity_status_id"] != 3: # 3 is completed ( and i["end_date"] > currDate - relativedelta(days=2) , i["start_date"] <= currDate)
                activity_pool.append(i)

        # for i in daily:
        #     if i["start_date"] + relativedelta(days=3) < currDate and i["activity_status_id"] != 3:
        #         activity_pool.append(i)

        # for i in weekly:
        #     if i["start_date"] + relativedelta(weeks=2) < currDate and i["activity_status_id"] != 3:
        #         activity_pool.append(i)
        
        # for i in fortnightly:
        #     if i["start_date"] + relativedelta(weeks=4) < currDate and i["activity_status_id"] != 3:
        #         activity_pool.append(i)

        # for i in activity_pool:
        #     print(i["activity_id"], end='\n')
        
        return activity_pool

    def get_current_date_activities(self, activities, currDate):
            daily = []
            weekly = []
            fortnightly = []
            activityArr = []

            # for i in activities:
            #     if i["act_category_id"] == 4:
            #         CC.append(i)

            for i in activities:
                if i["start_date"] + relativedelta(days=1) > i["end_date"] and currDate > i["start_date"]: # get all daily activities
                    daily.append(i)
                elif i["start_date"] + relativedelta(weeks=1) > i["end_date"] and currDate > i["start_date"]: # get all weekly activities
                    weekly.append(i)
                elif i["start_date"] + relativedelta(weeks=2) > i["end_date"] and currDate > i["start_date"]: # get all fortnightly activities
                    fortnightly.append(i)
                # else:
                #     print("not weekly or daily")
            
            # for i in CC: # CC is daily
            #     if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3: # 3 is completed
            #         activityArr.append(i)

            for i in daily:
                if (i["act_category_id"] == 1 or i["act_category_id"] == 2 or i["act_category_id"] == 3) and i["end_date"] < currDate:
                    # print(i["act_category_id"])
                    continue

                if i["start_date"] <= currDate and i["end_date"] > currDate - relativedelta(days=2) and i["activity_status_id"] != 3:
                    activityArr.append(i)

            for i in weekly:
                if i["start_date"] < currDate and i["end_date"] > currDate - relativedelta(weeks=1) and i["activity_status_id"] != 3:
                    activityArr.append(i)
            
            for i in fortnightly:
                if i["start_date"] < currDate and i["end_date"] > currDate - relativedelta(weeks=3) and i["activity_status_id"] != 3:
                    activityArr.append(i)

            # for i in activityArr:
            #     print(i["activity_id"], end='\n')
            
            return activityArr

    def get_child_activities_with_activity_table(self, child_id):
        selected = select(ChildActivity.start_date, ChildActivity.end_date, ChildActivity.child_id, ChildActivity.activity_status_id, Activity).select_from(ChildActivity).join(Activity, ChildActivity.activity_id==Activity.activity_id).where(ChildActivity.child_id==child_id)

        arr = ["start_date", "end_date", "child_id", "activity_status_id"]

        result = self.session.execute(selected)
        fullActList = []

        # count = 0
        for i in result:
            # print(i)
            # count += 1

            ActData: dict = i[4].__dict__.copy()
            # childActData: dict = i[0].__dict__.copy()

            key = list(ActData.keys())

            ActData.pop(key[0])
            # childActData.pop(key[0])

            dict1 = {arr[0]: i[0], arr[1]: i[1], arr[2]: i[2], arr[3]: i[3]}

            ActData.update(dict1)
            # childActData.update(actData)
            fullActList.append(ActData.copy())

        # print(fullActList[-1])
        # print(count)
        return fullActList
    
    def get_activities(self, grade):
        selected = select(Activity).where(Activity.standard_id==grade)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)
            
        return arr[0]
        

    # actPool = get_activity_pool_activities(activities=activities)

    def dump_data_in_child_activity(self, fullActList: list, child_id):
        for act in fullActList:
            # print(act)
            childAct = ChildActivity(
                        activity_id = act["activity_id"],
                        child_id = child_id,
                        start_date = act["start_date"],
                        end_date = act["end_date"],
                        activity_status_id = 1, #act["activity_status_id"],
                        is_archived = act["is_archived"],
                        created_by = act["created_by"],
                        created_date = act["created_date"])
            self.session.add(childAct)
            self.session.commit()
            # break
    
    def dump_wordle_in_child_activity(self, wordle_act_list: list, child_id):
        for act in wordle_act_list:
            # print(act)
            childAct = ChildActivity(
                        activity_id = act["activity_id"],
                        child_id = child_id,
                        start_date = act["start_date"],
                        end_date = act["end_date"],
                        activity_status_id = 1, #act["activity_status_id"],
                        is_archived = act["is_archived"],
                        created_by = act["created_by"],
                        created_date = act["created_date"],
                        wordle_words_id = act["wordle_words_id"])
            self.session.add(childAct)
            self.session.commit()
    
    def get_child_activity_table_activities(self, child_id):
        selected = select(ChildActivity).where(ChildActivity.child_id==child_id)

        result = self.session.execute(selected)

        fullActList = get_result_as_dict(result)

        return fullActList[0]
    
    def get_wordle_words(self, startdate, enddate, grade):
        selected = select(WordleWords).filter(WordleWords.word_show_date >= startdate).filter(WordleWords.word_show_date < enddate).filter(WordleWords.standard_id == grade)
        
        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        # for i in result:
        #     tempdict: dict = i[0].__dict__
        #     key = list(tempdict.keys())

        #     tempdict.pop(key[0])

        #     arr.append(tempdict.copy())

        return arr[0]
    
    def get_stories(self, week, grade):
        selected = select(Story).filter(Story.standard_id==grade).filter(Story.week_num<=week)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]

    def get_wordle_act(self, grade):
        selected = select(Activity).filter(Activity.act_category_id==3).filter(Activity.standard_id==grade)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0][0]

    

# startdate = datetime.datetime(2024, 6, 1)
# enddate = startdate + relativedelta(months=3)
# grade = 4

# conn = Connection()
# activities = conn.get_activities(grade)
# print(activities[0])
# print(conn.get_wordle_words(startdate, enddate, grade)[-1]["wordle_words_id"])
