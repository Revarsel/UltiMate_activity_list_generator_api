from sqlalchemy import create_engine, BigInteger, Boolean, Integer, VARCHAR, Column, TIMESTAMP, and_, Text, select, asc, desc
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

def convert_all_values_to_json_readable(data):
    data_given = data

    for i in data_given:
        for k in range(len(i.keys())):
            value = list(i.values())
            keys = list(i.keys())
            if type(value[k]) == datetime.datetime:
                i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
    
    return data_given

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
    is_favourite = Column(Boolean, default=False)
    is_parent_approved = Column(Boolean, default=False)

class Activity(Base):
    __tablename__ = "activity"

    activity_id = Column(Integer, primary_key=True, autoincrement=True)# SERIAL NOT NULL,
    standard_id = Column(BigInteger)
    title = Column(VARCHAR(50))# character varying(50) NOT NULL,
    gender_id = Column(BigInteger)# bigint NOT NULL,
    difficulty_level_id = Column(BigInteger, nullable=True)# bigint,
    activity_game_type_id = Column(BigInteger, nullable=True)# bigint,
    priority_id = Column(BigInteger)# bigint NOT NULL,
    act_category_id = Column(BigInteger)# bigint NOT NULL,
    parent_desc = Column(Text, nullable=True)# text,
    child_desc = Column(Text)# text NOT NULL,
    purpose_outcome = Column(Text, nullable=True)# text,
    act_frequency_id = Column(BigInteger)# bigint NOT NULL,
    points = Column(Integer)# integer NOT NULL,
    is_foundational = Column(Boolean, nullable=True)#3 boolean,
    #avg_time_minutes = Column(Integer)# integer NOT NULL,
    is_safety_risk = Column(Boolean)# boolean NOT NULL,
    is_festival = Column(Boolean)# boolean NOT NULL,
    festival_id = Column(BigInteger, nullable=True)# bigint,
    is_discrematory = Column(Boolean)# boolean NOT NULL,
    is_external_dependency = Column(Boolean)# boolean NOT NULL,
    is_parent_supervision = Column(Boolean)# boolean NOT NULL,
    is_parent_involment = Column(Boolean)# boolean NOT NULL,
    parent_involment_level_id = Column(BigInteger, nullable=True)# bigint,
    is_screen_time = Column(Boolean)# boolean NOT NULL,
    screen_time_category_id = Column(BigInteger)# bigint,
    is_negative_effects = Column(Boolean)# boolean NOT NULL,
    is_trial = Column(Boolean)# boolean NOT NULL,
    is_premium = Column(Boolean, nullable=True)# boolean,
    is_discussion = Column(Boolean, nullable=True)# boolean,
    cover_image_path = Column(Text, nullable=True)# text,
    ideal_time = Column(VARCHAR(30), nullable=True)# character varying(30),
    ideal_day = Column(VARCHAR(30), nullable=True)# character varying(30),
    benefit = Column(Text, nullable=True)# text,
    who_should_not_do = Column(Text, nullable=True)# text,
    more_info = Column(Text, nullable=True)# text,
    deity = Column(VARCHAR(50), nullable=True)# character varying(50),
    shlok_length_id = Column(Integer, nullable=True)
    narrated_by = Column(VARCHAR(40), nullable=True)
    is_archived = Column(Boolean)# boolean NOT NULL,
    created_by = Column(VARCHAR(35))# character varying(35) NOT NULL,
    updated_by = Column(VARCHAR(35), nullable=True)# character varying(35),
    created_date = Column(TIMESTAMP)# timestamp without time zone NOT NULL,
    updated_date = Column(TIMESTAMP, nullable=True)# timestamp without time zone,
    revision = Column(Integer, default=0)# integer DEFAULT 0

class ActivityStandard(Base):
    __tablename__ = "activity_standard"

    activity_standard_id = Column(Integer, primary_key=True) # SERIAL NOT NULL,
    activity_id = Column(BigInteger) # NOT NULL,
    standard_id = Column(BigInteger) # NOT NULL,
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class WordleWords(Base):
    __tablename__ = "wordle_words"

    wordle_words_id = Column(Integer, primary_key=True, autoincrement=True)
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

    story_id = Column(Integer, primary_key=True, autoincrement=True) #NOT NULL,
    title = Column(Text) #NOT NULL,
    importance = Column(Text)
    is_trial = Column(Boolean)
    is_festival = Column(Boolean, nullable=True)
    festival_id = Column(BigInteger, nullable=True)
    cover_image_path = Column(Text) #NOT NULL
    primary_language_id = Column(BigInteger) #NOT NULL
    primary_file_path = Column(Text, nullable=True)
    primary_audio_file_path = Column(Text, nullable=True)
    primary_question_pdf = Column(Text, nullable=True)
    avg_time_minutes = Column(Integer)
    points = Column(Integer) #NOT NULL
    week_num = Column(Integer) #NOT NULL
    standard_id = Column(BigInteger) #NOT NULL
    narrated_by = Column(VARCHAR(40), nullable=True)
    thumbnail_image_path = Column(Text)
    is_archived = Column(Boolean) #NOT NULL
    created_by = Column(VARCHAR(35)) #NOT NULL
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)  #NOT NULL
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class FocusArea(Base):
    __tablename__ = "focus_area"

    focus_area_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    description = Column(VARCHAR(50), nullable=True)
    standard_id = Column(BigInteger)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)
    mintintcolor = Column(VARCHAR(50), nullable=True)
    maxtintcolor = Column(VARCHAR(50), nullable=True)

class FocusAreaFrequency(Base):
    __tablename__ = "focus_area_frequency"
    focus_area_frequency_id	= Column(Integer, primary_key=True)
    week = Column(BigInteger)
    focus_area_id = Column(BigInteger)
    standard_id = Column(BigInteger)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class ShlokLength(Base):
    __tablename__ = "shlok_length"

    shlok_length_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class Child(Base):
    __tablename__ = "child" 

    child_id = Column(Integer, primary_key=True)
    nick_name = Column(VARCHAR(35)) #NOT NULL,
    first_name = Column(VARCHAR(35), nullable=True)
    last_name = Column(VARCHAR(35), nullable=True)
    contact_number = Column(VARCHAR(15), nullable=True)
    contact_country_code = Column(BigInteger, nullable=True)
    parent_id = Column(BigInteger)
    standard_id = Column(BigInteger)
    birth_year_id = Column(BigInteger)
    user_id = Column(BigInteger, nullable=True)
    gender_id = Column(BigInteger, nullable=True)
    balance_points = Column(Integer, nullable=True)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(20))
    middle_name = Column(VARCHAR(20), nullable=True)
    last_name = Column(VARCHAR(20))
    username = Column(VARCHAR(35))
    contact_number = Column(VARCHAR(15))
    contact_country_code = Column(BigInteger)
    image_path = Column(VARCHAR(200), nullable=True)
    google_email = Column(VARCHAR(35), nullable=True)
    microsoft_email = Column(VARCHAR(35), nullable=True)
    is_active = Column(Boolean, nullable=True)
    is_new_user = Column(Boolean, nullable=True)
    last_logged_in = Column(TIMESTAMP, nullable=True)
    bad_credential_count = Column(Integer, nullable=True)
    locked = Column(TIMESTAMP, nullable=True)
    locked_date = Column(TIMESTAMP, nullable=True)
    password = Column(VARCHAR(100), nullable=True)
    user_type_id = Column(BigInteger)
    otp = Column(VARCHAR(15), nullable=True)
    password_updated = Column(TIMESTAMP, nullable=True)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

class ActFocusArea(Base):
    __tablename__ = "act_focus_area"

    act_focus_area_id = Column(Integer, primary_key=True)
    activity_id = Column(BigInteger)
    focus_area_id = Column(BigInteger)
    is_archived = Column(Boolean)
    created_by = Column(VARCHAR(35))
    updated_by = Column(VARCHAR(35), nullable=True)
    created_date = Column(TIMESTAMP)
    updated_date = Column(TIMESTAMP, nullable=True)
    revision = Column(Integer, default=0, nullable=True)

    """
    story_id = Column(Integer, primary_key=True) #SERIAL NOT NULL,
    title = Column(Text) #text NOT NULL,
    description = Column(Text, nullable=True)# text,
    importance = Column(Text) #text NOT NULL,
    is_festival = Column(Boolean)# boolean,
    festival_id = Column(BigInteger)# bigint,
    cover_image_path = Column(Text) #text NOT NULL,
    thumbnail_image_path = Column(Text)# text NOT NULL,
    primary_language_id = Column(BigInteger)# bigint NOT NULL,
    primary_file_path = Column(Text, nullable=True)# text,
    primary_audio_file_path = Column(Text, nullable=True)# text,
    narrated_by = Column(VARCHAR(40), nullable=True) #character varying(40),
    primary_question_pdf = Column(Text, nullable=True)# text,
    avg_time_minutes = Column(Integer) #integer NOT NULL,
    points = Column(Integer) #integer NOT NULL,
    week_num = Column(Integer) #integer NOT NULL,
    is_trial = Column(Boolean) #boolean NOT NULL,
    is_premium = Column(Boolean, nullable=True)# boolean,
    is_archived = Column(Boolean) #boolean NOT NULL,
    created_by = Column(VARCHAR(35))# character varying(35) NOT NULL,
    updated_by = Column(VARCHAR(35), nullable=True)# character varying(35),
    created_date = Column(TIMESTAMP) #timestamp without time zone NOT NULL,
    updated_date = Column(TIMESTAMP, nullable=True)# timestamp without time zone,
    revision = Column(Integer, default=0)# integer DEFAULT 0,
    """


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
            
            print(len(activityArr))
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
        selected = select(ActivityStandard.standard_id, Activity).select_from(Activity).join(ActivityStandard, ActivityStandard.activity_id==Activity.activity_id).where(ActivityStandard.standard_id==grade)
        # selected = select(Activity).where(Activity.standard_id==grade)

        result = self.session.execute(selected)

        arr = []
        for i in result:
            tempdict: dict = i[1].__dict__.copy()
            key = list(tempdict.keys())

            tempdict.pop(key[0])
            tempdict["standard_id"] = i[0]

            arr.append(tempdict.copy())

        if grade == 1:
            return [arr]
        else:
            selected = select(ActivityStandard.standard_id, Activity).select_from(Activity).join(ActivityStandard, ActivityStandard.activity_id==Activity.activity_id).where(ActivityStandard.standard_id==(int(grade)-1))
            # selected = select(Activity).where(Activity.standard_id==grade)

            result = self.session.execute(selected)
            arr1 = []
            for i in result:
                tempdict: dict = i[1].__dict__.copy()
                key = list(tempdict.keys())

                tempdict.pop(key[0])
                tempdict["standard_id"] = i[0]

                arr1.append(tempdict.copy())
            
            return [arr, arr1]
        

    # actPool = get_activity_pool_activities(activities=activities)

    def dump_data_in_child_activity(self, fullActList: list, child_id):
        for act in fullActList:
            childAct = ChildActivity(
                        activity_id = act["activity_id"],
                        child_id = child_id,
                        start_date = act["start_date"],
                        end_date = act["end_date"],
                        activity_status_id = 1, #act["activity_status_id"],
                        is_archived = act["is_archived"],
                        created_by = act["created_by"],
                        created_date = act["created_date"],
                        is_favourite=False,
                        is_parent_approved=False)
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
                        wordle_words_id = act["wordle_words_id"],
                        is_favourite=False,
                        is_parent_approved=False
                        )
            self.session.add(childAct)
            self.session.commit()
    
    def dump_stories_in_story_table(self, story_list: list):
        for story in story_list:
            story_act = Story(
                            title = story["title"], #NOT NULL,
                            cover_image_path = story["cover_image_path"], #NOT NULL
                            primary_language_id = story["primary_language_id"], #NOT NULL
                            avg_time_minutes = story["avg_time_minutes"],
                            points = story["points"], #NOT NULL
                            week_num = story["week_num"], #NOT NULL
                            standard_id = story["standard_id"], #NOT NULL
                            thumbnail_image_path = story["thumbnail_image_path"],
                            is_archived = story["is_archived"], #NOT NULL
                            created_by = story["created_by"], #NOT NULL
                            created_date = story["created_date"],  #NOT NULL
                            is_trial=False,
                            importance="default"
                            )
            self.session.add(story_act)
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
    
    def get_stories(self): #, week, grade):
        selected = select(Story) #.filter(Story.standard_id==grade).filter(Story.week_num<=week)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]

    def get_stories_only_n(self,n):
        selected = select(Story).limit(n) #.filter(Story.standard_id==grade).filter(Story.week_num<=week)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]
    
    def get_wordle_act(self, grade):
        selected = select(Activity).filter(Activity.act_category_id==3).filter(Activity.standard_id==grade)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0][0]
    
    def get_focus_area(self):
        selected = select(FocusArea).order_by(asc(FocusArea.standard_id))

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]

    def get_focus_area_frequency(self, grade):
        selected = select(FocusAreaFrequency).filter(FocusAreaFrequency.standard_id==grade).order_by(asc(FocusAreaFrequency.week))

        result = self.session.execute(selected)

        arr1 = get_result_as_dict(result)

        arr = []
        for i in arr1[0]:
            arr.append(i["focus_area_id"])

        return arr
    
    def get_mudras(self):
        selected = select(Activity).filter(Activity.act_category_id==2).filter(Activity.activity_game_type_id==5)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]
    
    def get_shloks(self):
        selected = select(Activity).filter(Activity.act_category_id==2).filter(Activity.activity_game_type_id==4)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]
    
    def get_existing_shloks(self, child_id):
        selected = select(ChildActivity.start_date, ChildActivity.end_date, ChildActivity.child_id, ChildActivity.activity_status_id, Activity).select_from(ChildActivity).join(Activity, ChildActivity.activity_id==Activity.activity_id).where(ChildActivity.child_id==child_id).filter(Activity.act_category_id==2).filter(Activity.activity_game_type_id==4).order_by(desc(ChildActivity.start_date))

        result = self.session.execute(selected)

        arr = ["start_date", "end_date", "child_id", "activity_status_id"]

        # result = self.session.execute(selected)
        fullActList = []

        for i in result:
            ActData: dict = i[4].__dict__.copy()

            key = list(ActData.keys())

            ActData.pop(key[0])

            dict1 = {arr[0]: i[0], arr[1]: i[1], arr[2]: i[2], arr[3]: i[3]}

            ActData.update(dict1)

            fullActList.append(ActData.copy())

        return fullActList
    
    def get_activities_only(self):
        selected = select(Activity)

        result = self.session.execute(selected)

        arr = get_result_as_dict(result)

        return arr[0]
    
    def dump_activities_in_activity_standard_table(self, activities):
        for act in activities:
            std_id = int(act["standard_id"])
            if std_id > 12:
                std_id -= 1
            else:
                std_id += 1
            Act = ActivityStandard(
                                activity_id = act["activity_id"],
                                standard_id = std_id,
                                is_archived = False,
                                created_by = "bhuvan",
                                created_date = datetime.datetime.now()
                                )
            self.session.add(Act)
            self.session.commit()
    
    def dump_activities_in_act_focus_area_table(self, activity, focus_id):
        Act = ActFocusArea(
                            activity_id = activity["activity_id"],
                            focus_area_id = focus_id,
                            is_archived = False,
                            created_by = "bhuvan",
                            created_date = datetime.datetime.now()
                            )
        self.session.add(Act)
        self.session.commit()
    
    def get_child_details(self, child_id):
        selected = select(Users.is_new_user, Child).select_from(Users).join(Child, Child.user_id==Users.user_id).where(Child.child_id==child_id)

        result = self.session.execute(selected)

        arr = ["is_new_user"]

        fullActList = []

        for i in result:
            ActData: dict = i[1].__dict__.copy()

            key = list(ActData.keys())

            ActData.pop(key[0])

            dict1 = {arr[0]: i[0]}

            ActData.update(dict1)

            fullActList.append(ActData.copy())

        return fullActList[0]


if __name__ == "__main__":
    conn = Connection()
    print(conn.get_child_details(4))
# print(len(conn.get_focus_area_frequency(1)[:26]))

# startdate = datetime.datetime(2024, 6, 1)
# enddate = startdate + relativedelta(months=3)
# grade = 4

# conn = Connection()
# activities = conn.get_activities(grade)
# print(activities[0])
# print(conn.get_wordle_words(startdate, enddate, grade)[-1]["wordle_words_id"])
