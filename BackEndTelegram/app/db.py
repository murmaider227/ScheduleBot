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
def get_schedule(major, year, day, cursor):
    '''
    Получение расписания по для выбраной пользователем группы
    '''
    sql='''SELECT sw.id, sm.name, sg.year, sd.name, so.option,
    subject1_name, subject1_teacher, subject1_place,
    subject2_name, subject2_teacher, subject2_place,
    subject3_name, subject3_teacher, subject3_place,
    subject4_name, subject4_teacher, subject4_place
    FROM schedule_week sw
    JOIN schedule_group sg on sw.group_id=sg.id
    JOIN schedule_major sm on sg.major_id=sm.id
    JOIN schedule_day sd on sw.day_id = sd.id 
    JOIN schedule_option so on sw.option_id = so.id
    WHERE sm.name=%s AND sd.name=%s AND sg.year=%s'''
    cursor.execute(sql, (major,day,year))
    text = cursor.fetchall()
    return text[0]

@database
def create_user(username, telegram_id, cursor):
    '''
    Сохранения пользователя при первом использовании бота
    '''
    cursor.execute('INSERT INTO schedule_student(username, telegram_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (username, telegram_id))

@database
def get_faculty(cursor):
    '''
    Получение списка факультетов
    '''
    cursor.execute('SELECT name FROM schedule_faculty')
    return cursor.fetchall()

@database
def get_major(faculty, cursor):
    '''
    Получение списка специальностей по заданому факультету
    '''
    sql = '''SELECT sm.name 
    FROM schedule_major sm 
    JOIN schedule_faculty sf on sm.faculty_id = sf.id 
    WHERE sf.name = %s'''
    cursor.execute(sql, (faculty,))
    return cursor.fetchall()

@database
def get_group_id(year, major, cursor):
    '''
    Получение ид группы по заданной специальности и курсу
    '''
    sql = '''
    SELECT sg.id FROM schedule_group sg
    JOIN schedule_major sm on sg.major_id=sm.id
    WHERE sg.year=%s AND sm.name=%s
    '''
    cursor.execute(sql, (year, major))
    return cursor.fetchall()[0]

@database
def save_group(user, group, cursor):
    '''
    Сохранение группы пользователя
    '''
    sql = '''INSERT INTO schedule_student_major(student_id, group_id) VALUES(%s, %s)'''
    cursor.execute(sql, (user, group))

@database
def get_user_group(user, cursor):
    '''
    Получение списка груп пользователя
    '''
    sql = '''
    SELECT sm.name, sg.year, sg.id FROM schedule_group sg
    JOIN schedule_major sm on sg.major_id=sm.id
    JOIN schedule_student_major ssm on sg.id = ssm.group_id
    WHERE ssm.student_id = %s
    '''
    cursor.execute(sql, (user,))
    return cursor.fetchall()

@database
def delete_user_from_group(user, group, cursor):
    '''
    Для удаления групы у пользователя
    '''
    sql = '''
    DELETE FROM schedule_student_major
    WHERE student_id = %s AND group_id = %s
    '''
    cursor.execute(sql, (user, group))
