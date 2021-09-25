import psycopg2
import os
from psycopg2.extras import DictCursor


def database(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USERNAME'), password=os.getenv('DB_PASSWORD'), host='localhost')
        cursor = conn.cursor()
        conn.autocommit=True

        return_value = func(*args, cursor=cursor)

        cursor.close()
        conn.close()
        return return_value
    return wrapper  

@database
def get_schedule(major, day, cursor):

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
    return text[0]

@database
def create_user(username, telegram_id, cursor):
    cursor.execute('INSERT INTO schedule_student(username, telegram_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (username, telegram_id))

@database
def get_faculty(cursor):
    cursor.execute('SELECT name FROM schedule_faculty')
    return cursor.fetchall()

@database
def get_major(faculty, cursor):
    sql = '''SELECT sm.name 
    FROM schedule_major sm 
    JOIN schedule_faculty sf on sm.faculty_id = sf.id 
    WHERE sf.name = %s'''
    cursor.execute(sql, (faculty,))
    return cursor.fetchall()

@database
def get_group_id(year, major, cursor):
    sql= '''SELECT sw.id FROM schedule_week sw
    JOIN schedule_year sy on sw.year_id = sy.id
    JOIN schedule_major sm on sw.major_id=sm.id
    WHERE sy.year=%s AND sm.name=%s
    '''
    cursor.execute(sql, (year, major))
    return cursor.fetchall()[0]

@database
def save_group(user, group, cursor):
    sql = '''INSERT INTO schedule_student_major(student_id, week_id) VALUES(%s, %s)'''
    cursor.execute(sql, (user, group))
