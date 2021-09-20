import psycopg2
import os
from psycopg2.extras import DictCursor


conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USERNAME'), password=os.getenv('DB_PASSWORD'), host='localhost')

cursor= conn.cursor()

cursor.execute('SELECT sw.id, sm.name, sy.year, sd.name, so.option,sw.subject1_name, sw.subject1_teacher, sw.subject2_name, sw.subject2_teacher, subject3_name, subject3_teacher, subject4_name, subject4_teacher FROM schedule_week sw JOIN schedule_year sy on sw.year_id=sy.id JOIN schedule_major sm on sw.major_id=sm.id JOIN schedule_day sd on sw.day_id = sd.id JOIN schedule_option so on sw.option_id = so.id')
record = cursor.fetchall()
print(record)
cursor.close()
conn.close()