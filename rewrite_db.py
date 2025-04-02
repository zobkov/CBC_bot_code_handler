from database import Database

db = Database()
db.add_codes_from_csv("codes.csv")
db.add_timed_codes_from_csv("codes_timed.csv")