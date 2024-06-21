from pony.orm import *

db = Database()
db.bind(provider="postgres", user="postgress", password="Shubham123", host="62.72.57.120", port="5432", database="ultimatedb")
