import psycopg2
import os
from psycopg2.extras import DictCursor

def get_schedule(major, day):
    conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USERNAME'), password=os.getenv('DB_PASSWORD'), host='localhost')

    cursor= conn.cursor()
    sql='''SELECT sw.id, sm.name, sy.year, sd.name, so.option,
    subject1_name, subject1_teacher, subject1_place,
    subject2_name, subject2_teacher, subject2_place,
    subject3_name, subject3_teacher, subject3_place,
    subject4_name, subject4_teacher, subject4_place
    FROM schedule_week sw 
    JOIN schedule_year sy on sw.year_id=sy.id
    JOIN schedule_major sm on sw.major_id=sm.id
    JOIN schedule_day sd on sw.day_id = sd.id 
    JOIN schedule_option so on sw.option_id = so.id
    WHERE sm.name=%s AND sd.name=%s'''
    cursor.execute(sql, (major,day))
    text = cursor.fetchall()
    cursor.close()
    conn.close()
    return text[0]

def create_user(telegram_id):
    pass
