import random
import string
import sqlite3
import os
from time import time

data = sqlite3.connect("testielokuvat.db")

def elokuva(length: int, alkuvuosi: int, loppuvuosi: int):

    return ''.join(random.choices(string.ascii_letters, k=length)), random.randint(alkuvuosi, loppuvuosi)

def ei_indeksia():

    os.remove("testielokuvat.db")

    data = sqlite3.connect("testielokuvat.db")

    data.execute("CREATE TABLE Elokuvat (id INTEGER PRIMARY KEY, nimi TEXT, vuosi INTEGER)")

    lisays_alku = time()

    data.execute("BEGIN")

    for iii in range(10**6):
        
        nimi, vuosi = elokuva(8,1900,2000)
        data.execute(f"INSERT INTO Elokuvat (nimi, vuosi) VALUES ('{nimi}', {vuosi})")

    data.execute("COMMIT")

    lisays_loppu = time()

    kysely_alku = time()

    cur = data.cursor()

    for iii in range(1000):

        julkaisuvuosi = random.randint(1900,2000)

        cur.execute(f"SELECT COUNT(*) FROM Elokuvat WHERE vuosi = {julkaisuvuosi}")

    kysely_loppu = time()

    return lisays_loppu - lisays_alku, kysely_loppu - kysely_alku
    
if __name__ == "__main__":

    print(ei_indeksia())