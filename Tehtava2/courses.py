import os
import sqlite3

os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

def create_tables():

    db.execute("CREATE TABLE Opettajat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Opiskelijat (id INTEGER PRIMARY KEY, nimi TEXT);")
    db.execute("CREATE TABLE Kurssit (id INTEGER PRIMARY KEY, nimi TEXT, pisteet INTEGER \
                opettaja_id INTEGER REFERENCES Opettajat);")
    db.execute("CREATE TABLE Suoritukset (id INTEGER PRIMARY KEY, \
                kurssi_id INTEGER REFERENCES Kurssit, paivamaara TEXT, \
                arvosana INTEGER)")
    db.execute("CREATE TABLE Ryhmat (id INTEGER PRIMARY KEY, \
                nimi TEXT, opettaja_id INGEGER REFERENCES Opettajat, \
                opiskelija_id INTEGER REFERENCES Opiskelijat)")


def create_teacher(name: str):

    db.execute(f"INSERT INTO Opettajat (nimi) VALUES ('{name}')")

def create_student(name: str):

    db.execute(f"INSERT INTO Opiskelijat (nimi) VALUES ('{name}')")