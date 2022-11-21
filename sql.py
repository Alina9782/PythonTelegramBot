import sqlite3

from bot import user_lastname, user_firstname, user_phone

db = sqlite3.connect('clinic.db')
cursor = db.cursor()

cursor.execute(f"UPDATE schedule SET LastName = ('{user_lastname}') WHERE Time = '01.12 11:00'")
cursor.execute(f"UPDATE schedule SET FirstName = ('{user_firstname}') WHERE Time = '01.12 11:00'")
cursor.execute(f"UPDATE schedule SET Phone = ('{user_phone}') WHERE Time = '01.12 11:00'")
db.commit()
