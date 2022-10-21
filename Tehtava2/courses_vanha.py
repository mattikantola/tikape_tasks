import os
import sqlite3

os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

class Teacher_id:

    id = 0

    def add_teacher():

        Teacher_id.id += 1

class Student_id:

    id = 0

    def add_student():

        Student_id.id += 1

class Course_id:

    id = 0

    def add_course():

        Course_id.id += 1

class Group_id:

    id = 0

    def add_group():

        Group_id.id += 1

def create_tables():

    db.execute("CREATE TABLE Opettajat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Opiskelijat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Kurssit (tunnus INTEGER, nimi TEXT, pisteet INTEGER, \
                opettaja_id INTEGER REFERENCES Opettajat);")
    db.execute("CREATE TABLE Suoritukset (id INTEGER PRIMARY KEY, \
                opiskelija_id INTEGER REFERENCES Opiskelijat, \
                kurssi_id INTEGER REFERENCES Kurssit, paivamaara TEXT, \
                arvosana INTEGER);")
    db.execute("CREATE TABLE Ryhmat (id INTEGER PRIMARY KEY, \
                nimi TEXT, opettaja_id INGEGER REFERENCES Opettajat, \
                opiskelija_id INTEGER REFERENCES Opiskelijat);")


def create_teacher(name: str):

    db.execute(f"INSERT INTO Opettajat (nimi) VALUES ('{name}');")
    Teacher_id.add_teacher()
    return Teacher_id.id


def create_student(name: str):

    db.execute(f"INSERT INTO Opiskelijat (nimi) VALUES ('{name}');")
    Student_id.add_student()
    return Student_id.id

def create_course(name: str, credits: int, teachers: list):

    Course_id.add_course()

    if len(teachers) == 0:

        db.execute(f"INSERT INTO Kurssit (tunnus, nimi, pisteet) VALUES ({Course_id.id}, '{name}', {credits});")

    else:

        for teacher_id in teachers:

            db.execute(f"INSERT INTO Kurssit (tunnus, nimi, pisteet, opettaja_id) VALUES ({Course_id.id}, '{name}', {credits}, {teacher_id});")

    return Course_id.id

def add_credits(student: int, course: int, date: str, grade: int):

    db.execute(f"INSERT INTO Suoritukset (opiskelija_id, kurssi_id, paivamaara, arvosana) VALUES ({student}, {course}, '{date}', {grade});")

def create_group(name: str, teachers: list, students: list):

    for teacher_id in teachers:

        for student_id in students:

            db.execute(f"INSERT INTO Ryhmat (nimi, opettaja_id, opiskelija_id) VALUES ('{name}', {teacher_id}, {student_id});")


def courses_by_teacher(teacher_name: str):

    cursor = db.cursor()
    courses = cursor.execute(f"SELECT K.nimi FROM Kurssit K LEFT JOIN Opettajat O ON K.opettaja_id = O.id WHERE O.nimi = '{teacher_name}' ORDER BY K.nimi;").fetchall()
    return [course[0] for course in courses]


def courses_by_student(student_name: str):

    cursor = db.cursor()
    courses = cursor.execute(f"SELECT DISTINCT K.nimi, S.arvosana FROM Suoritukset S LEFT JOIN Kurssit K ON K.tunnus = S.kurssi_id LEFT JOIN Opiskelijat O ON O.id = S.opiskelija_id WHERE O.nimi = '{student_name}';").fetchall()
    return courses

def credits_by_year(year: int):

    year = str(year)
    cursor = db.cursor()
    credits = cursor.execute(f"SELECT SUM(pojot) FROM (SELECT K.pisteet AS pojot FROM Kurssit K LEFT JOIN Suoritukset S ON S.kurssi_id = K.tunnus WHERE S.paivamaara LIKE '{year}%' GROUP BY S.paivamaara);").fetchall()
    return credits[0][0]

def grade_distribution(course_name: str):

    cursor = db.cursor()
    distribution = cursor.execute(f"SELECT S.arvosana FROM Suoritukset S LEFT JOIN Kurssit K ON S.kurssi_id = K.tunnus WHERE K.nimi = '{course_name}' ORDER BY S.arvosana;").fetchall()


    return distribution

def course_list():

    cursor = db.cursor()
    courselist = cursor.execute("SELECT K.nimi, COUNT(S.opiskelija_id) FROM Kurssit K LEFT JOIN Suoritukset S ON S.kurssi_id = K.tunnus GROUP BY S.kurssi_id;").fetchall()
    return courselist