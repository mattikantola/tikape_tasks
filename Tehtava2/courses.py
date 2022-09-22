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

def create_tables():

    db.execute("CREATE TABLE Opettajat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Opiskelijat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Kurssit (id INTEGER PRIMARY KEY, nimi TEXT, pisteet INTEGER, \
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

    if len(teachers) == 0:

        db.execute(f"INSERT INTO Kurssit (nimi, pisteet) VALUES ('{name}', {credits});")

    else:

        for teacher_id in teachers:

            db.execute(f"INSERT INTO Kurssit (nimi, pisteet, opettaja_id) VALUES ('{name}', {credits}, {teacher_id});")

    Course_id.add_course()
    return Course_id.id

def add_credits(student: int, course: int, date: str, grade: int):

    db.execute(f"INSERT INTO Suoritukset (opiskelija_id, kurssi_id, paivamaara, arvosana) VALUES ({student}, {course}, '{date}', {grade});")

def create_group(name: str, teachers: list, students: list):

    for teacher_id in teachers:

        for student_id in students:

            db.execute(f"INSERT INTO Ryhmat (nimi, opettaja_id, opiskelija_id) VALUES ('{name}', {teacher_id}, {student_id});")

