import os
import sqlite3

os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

class Teacher_id:

    id = 1

    def add_teacher():

        Teacher_id.id += 1

class Student_id:

    id = 1

    def add_student():

        Student_id.id += 1

class Course_id:

    id = 1

    def add_course():

        Course_id.id += 1

class Group_id:

    id = 1

    def add_group():

        Group_id.id += 1

def create_tables():

    db.execute("CREATE TABLE Opettajat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Opiskelijat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Kurssit (id INTEGER PRIMARY KEY, nimi TEXT, pisteet INTEGER);")
    db.execute("CREATE TABLE Kurssin_opettajat (id INTEGER PRIMARY KEY, kurssi_id INTEGER REFERENCES Kurssit, opettaja_id INTEGER REFERENCES Opettajat);")
    db.execute("CREATE TABLE Suoritukset (id INTEGER PRIMARY KEY, \
                opiskelija_id INTEGER REFERENCES Opiskelijat, \
                kurssi_id INTEGER REFERENCES Kurssit, paivamaara TEXT, \
                arvosana INTEGER);")
    db.execute("CREATE TABLE Ryhmat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Ryhman_jasenet (id INTEGER PRIMARY KEY, ryhma_id INTEGER REFERENCES Ryhmat, opettaja_id REFERENCES Opettajat, opiskelija_id INTEGER REFERENCES Opiskelijat);")


def create_teacher(name: str):

    db.execute(f"INSERT INTO Opettajat (nimi) VALUES ('{name}');")
    Teacher_id.add_teacher()
    return Teacher_id.id - 1


def create_student(name: str):

    db.execute(f"INSERT INTO Opiskelijat (nimi) VALUES ('{name}');")
    Student_id.add_student()
    return Student_id.id - 1

def create_course(name: str, credits: int, teacher_ids: list):

    db.execute(f"INSERT INTO Kurssit (nimi, pisteet) VALUES ('{name}', {credits});")
    for t_id in teacher_ids:
        db.execute(f"INSERT INTO Kurssin_opettajat (kurssi_id, opettaja_id) VALUES ({Course_id.id}, {t_id});")
    Course_id.add_course()
    return Course_id.id - 1

def add_credits(student: int, course: int, date: str, grade: int):

    db.execute(f"INSERT INTO Suoritukset (opiskelija_id, kurssi_id, paivamaara, arvosana) VALUES ({student}, {course}, '{date}', {grade});")

def create_group(name: str, teacher_ids: list, student_ids: list):

    db.execute(f"INSERT INTO Ryhmat (nimi) VALUES ('{name}');")

    for teacher in teacher_ids:

        for student in student_ids:

            db.execute(f"INSERT INTO Ryhman_jasenet (ryhma_id, opettaja_id, opiskelija_id) VALUES ({Group_id.id}, {teacher}, {student})")

    Group_id.add_group()
    return Group_id.id - 1

def courses_by_teacher(teacher_name: str):

    cur = db.cursor()
    courses = cur.execute(f"SELECT K.nimi FROM Kurssit K LEFT JOIN Kurssin_opettajat KO ON K.id = KO.kurssi_id WHERE KO.opettaja_id = (SELECT id FROM Opettajat WHERE nimi = '{teacher_name}') ORDER BY K.nimi;").fetchall()
    return [course[0] for course in courses]

def credits_by_teacher(teacher_name: str):

    cur = db.cursor()
    credits = cur.execute(f"SELECT SUM(K.pisteet) FROM Kurssit K, Suoritukset S, Kurssin_opettajat KO WHERE KO.opettaja_id = (SELECT id FROM Opettajat WHERE nimi = '{teacher_name}') AND S.kurssi_id = K.id AND KO.kurssi_id = K.id;").fetchall()
    return credits[0][0]

def courses_by_student(student_name: str):

    cur = db.cursor()
    courses = cur.execute(f"SELECT K.nimi, S.arvosana FROM Kurssit K LEFT JOIN Suoritukset S ON S.kurssi_id = K.id LEFT JOIN Opiskelijat O ON O.id = S.opiskelija_id WHERE O.nimi = '{student_name}' ORDER BY K.nimi;").fetchall()
    return courses

def credits_by_year(year: int):

    year_str = str(year)
    cur = db.cursor()
    credits = cur.execute(f"SELECT SUM(K.pisteet) FROM Kurssit K LEFT JOIN Suoritukset S ON K.id = S.kurssi_id WHERE S.paivamaara LIKE '{year}%'").fetchone()
    return credits[0]

def grade_distribution(course_name: str):

    cur = db.cursor()
    grades = cur.execute(f"SELECT S.arvosana, IFNULL(COUNT(S.arvosana), 0) FROM Suoritukset S LEFT JOIN Kurssit K ON S.kurssi_id = K.id WHERE K.nimi = '{course_name}' GROUP BY S.arvosana;").fetchall()
    grades_dict = {1:0, 2:0, 3:0, 4:0, 5:0}
    for grade in grades:

        grades_dict[grade[0]] = grade[1]

    return grades_dict

def course_list():

    cur = db.cursor()
    opiskelijat = cur.execute("SELECT K.nimi, IFNULL(COUNT(S.opiskelija_id), 0) FROM Kurssit K LEFT JOIN Suoritukset S ON S.kurssi_id = K.id GROUP BY S.kurssi_id ORDER BY K.nimi;").fetchall()
    opettajat = cur.execute("SELECT K.nimi, IFNULL(COUNT(KO.opettaja_id),0) FROM Kurssit K LEFT JOIN Kurssin_opettajat KO ON K.id = KO.kurssi_id GROUP BY kurssi_id ORDER BY K.nimi;").fetchall()
    
    opettajien_maarat = [ope[1] for ope in opettajat]

    nimet = [opis[0] for opis in opiskelijat]

    opiskelijoiden_maarat = [opis[1] for opis in opiskelijat]

    return list(zip(nimet, opettajien_maarat, opiskelijoiden_maarat))

def teacher_list():

    cursor = db.cursor()

    opettajat = cursor.execute("SELECT O.nimi FROM Opettajat O ORDER BY O.nimi;").fetchall()
    opettajat = [opettaja[0] for opettaja in opettajat]

    data = []

    for opettaja in opettajat:

        cursor2 = db.cursor()
        ope_id = cursor2.execute(f"SELECT id FROM Opettajat WHERE nimi = '{opettaja}';").fetchone()[0]

        cursor2 = db.cursor()
        ryhmat = cursor2.execute(f"SELECT K.nimi FROM Kurssit K LEFT JOIN Kurssin_opettajat KO ON K.id = KO.kurssi_id WHERE KO.opettaja_id = {ope_id} ORDER BY K.nimi;").fetchall()
        ryhmat = [ryhma[0] for ryhma in ryhmat]

        new_data = opettaja, ryhmat
        data.append(new_data)

    return data

def group_people(group_name: str):

    cursor = db.cursor()

    ryhma_id = cursor.execute(f"SELECT id FROM Ryhmat WHERE nimi = '{group_name}'").fetchone()[0]

    cursor = db.cursor()

    opettajat = cursor.execute(f"SELECT DISTINCT O.nimi FROM Opettajat O LEFT JOIN Ryhman_jasenet RJ ON RJ.opettaja_id = O.id WHERE RJ.ryhma_id = {ryhma_id};").fetchall()

    opettajat = [ope[0] for ope in opettajat]

    opiskelijat = cursor.execute(f"SELECT DISTINCT O.nimi FROM Opiskelijat O LEFT JOIN Ryhman_jasenet RJ ON RJ.opiskelija_id = O.id WHERE RJ.ryhma_id = {ryhma_id};").fetchall()

    opiskelijat = [opis[0] for opis in opiskelijat]

    opettajat.extend(opiskelijat)
    opettajat.sort()

    return opettajat

def common_groups(teacher_name: str, student_name: str):

    cur = db.cursor()
    opettajan_ryhmat = cur.execute(f"SELECT DISTINCT J.ryhma_id FROM Ryhman_jasenet J LEFT JOIN Opettajat O ON O.id = J.opettaja_id WHERE O.nimi = '{teacher_name}' ORDER BY J.ryhma_id;").fetchall()
    opiskelijan_ryhmat = cur.execute(f"SELECT DISTINCT J.ryhma_id FROM Ryhman_jasenet J LEFT JOIN Opiskelijat O ON O.id = J.opiskelija_id WHERE O.nimi = '{student_name}' ORDER BY J.ryhma_id").fetchall()
    opettajan_ryhmat = [ope[0] for ope in opettajan_ryhmat]
    opiskelijan_ryhmat = [opis[0] for opis in opiskelijan_ryhmat]

    yhteiset = []
    jjj = 0

    for iii in range(min(len(opiskelijan_ryhmat), len(opettajan_ryhmat))):

        if opettajan_ryhmat[jjj] == opiskelijan_ryhmat[iii]:

            yhteiset.append(opettajan_ryhmat[jjj])

        jjj += 1

    result = []

    for iii in yhteiset:

        ryhma = cur.execute(f"SELECT nimi FROM Ryhmat WHERE id = {iii}").fetchone()

        result.append(ryhma[0])

    return sorted(result)
    