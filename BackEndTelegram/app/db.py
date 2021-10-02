import psycopg2
import os


class DataBase:

    def __init__(self):
        self.conn = None

    def connect(self):
        """Connect to database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                        dbname=os.getenv('DB_NAME'), 
                        user=os.getenv('DB_USERNAME'), 
                        password=os.getenv('DB_PASSWORD'), 
                        host='localhost')
            except psycopg2.DatabaseError as e:
                raise e
            finally:
                print('Connection opened successfully')

    def get_schedule(self, major: str, year: int, day: str, option: str):
        """Get schedule for selected group."""
        sql='''SELECT sw.id, sm.name, sg.year, sd.name, sw.option,
        subject1_name, subject1_teacher, subject1_place,
        subject2_name, subject2_teacher, subject2_place,
        subject3_name, subject3_teacher, subject3_place,
        subject4_name, subject4_teacher, subject4_place
        FROM schedule_week sw
        JOIN schedule_group sg on sw.group_id=sg.id
        JOIN schedule_major sm on sg.major_id=sm.id
        JOIN schedule_day sd on sw.day_id = sd.id 
        WHERE sm.name=%s AND sd.name=%s AND sg.year=%s AND sw.option=%s
        '''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (major,day,year, option))
            text = cursor.fetchall()
        return text[0]

    def create_user(self, username: str, telegram_id: int) -> None:
        """Saving user after first use of bot."""
        sql ='''
        INSERT INTO schedule_student(username, telegram_id) 
        VALUES (%s, %s) ON CONFLICT DO NOTHING
        '''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (username, telegram_id))
            self.conn.commit()

    def get_faculty(self) -> list:
        """Get list of faculty."""
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT name FROM schedule_faculty')
            text = cursor.fetchall()
        return text

    def get_major(self, faculty: str) -> list:
        """Get major by faculty."""
        sql = '''SELECT sm.name 
        FROM schedule_major sm 
        JOIN schedule_faculty sf on sm.faculty_id = sf.id 
        WHERE sf.name = %s'''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (faculty,))
            text = cursor.fetchall()
        return text

    def get_group_id(self, year: int, major: str) -> int:
        """Get group id by year and major."""
        sql = '''
        SELECT sg.id FROM schedule_group sg
        JOIN schedule_major sm on sg.major_id=sm.id
        WHERE sg.year=%s AND sm.name=%s
        '''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (year, major))
            text = cursor.fetchall()
        return text[0]

    def save_group(self, user: int, group: int) -> None:
        """Saving user group."""
        sql = '''INSERT INTO schedule_student_major(student_id, group_id) 
        VALUES(%s, %s)'''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (user, group))
            self.conn.commit()

    def get_user_group(self, user: int) -> list:
        """Get list of user groups."""
        sql = '''
        SELECT sm.name, sg.year, sg.id FROM schedule_group sg
        JOIN schedule_major sm on sg.major_id=sm.id
        JOIN schedule_student_major ssm on sg.id = ssm.group_id
        WHERE ssm.student_id = %s
        '''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (user,))
            text = cursor.fetchall()
        return text

    def delete_user_from_group(self, user: int, group: int) -> None:
        """Delete selected user group."""
        sql = '''
        DELETE FROM schedule_student_major
        WHERE student_id = %s AND group_id = %s
        '''
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (user, group))
            self.conn.commit()


