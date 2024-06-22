from sqlalchemy import create_engine, BigInteger, Boolean, Integer, VARCHAR, Column, TIMESTAMP, and_, Text, select
from sqlalchemy.orm import sessionmaker, declarative_base
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


def get_engine():
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{database}"
    # print(url)
    engine = create_engine(url, echo=False)
    return engine

def get_session():
    session = sessionmaker(bind=get_engine())()
    return session

session = get_session()
# child_act = session.query(ChildActivity).all()

# act_date = session.query(ChildActivity).filter(ChildActivity.start_date < datetime.datetime(2024, 6, 5)).all()

# activity_pool = session.query(Activity, ChildActivity.child_id, ChildActivity.start_date, ChildActivity.end_date)\
#     .join(Activity, and_(ChildActivity.activity_id == Activity.activity_id, ChildActivity.child_id==child_id_num))

activity_pool = session.query(Activity, ChildActivity.child_id, ChildActivity.start_date, ChildActivity.end_date).select_from(Activity)\
                .outerjoin(ChildActivity, ChildActivity.activity_id==Activity.activity_id) #.child_id, ChildActivity.start_date, ChildActivity.end_date)\

# pool = select([Activity, ChildActivity]).select_from(activity_pool)

# for i in activity_pool:
    # print(i.activity_id)

arr = ["child_id", "start_date", "end_date"]

def get_activity(activity_pool):
    act_dict = []
    count = 0
    for i in activity_pool:
        tempdict = {}
        count += 1
        # for k in range(len(i)-1):
        #         tempdict[arr[k]] = i[k+1]
        for b in range(1):
            tempdict = {}
            act: dict = i[b].__dict__.copy()
            # print(list(act.keys()).__len__())
            # act.pop("_sa_instance_state")

            for k in range(len(act)):
                # print(list(act.keys()))
                key = list(act.keys())
                tempdict[key[k]] = act[key[k]]
        
            act_dict.append(tempdict.copy())
    
    # print(count)
    return (act_dict, count)

values = get_activity(activity_pool=activity_pool)

# print(values[0])
for i in values[0]:
    print(i["activity_id"])

print(values[1])

# dictionary = activity_pool[0][0].__dict__

# # for i in dictionary:
# #     print(dictionary[i])

# print(activity_pool[0][1])