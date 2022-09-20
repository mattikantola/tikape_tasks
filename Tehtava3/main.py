import random
import string
import sqlite3
import os
from timeit import timeit

data = sqlite3.connect("testielokuvat.db")

def elokuva(length: int, alkuvuosi: int, loppuvuosi: int):

    return ''.join(random.choices(string.ascii_letters, k=length)), random.randint(alkuvuosi, loppuvuosi)

def ei_indeksia():

    os.remove("testielokuvat.db")

    data = sqlite3.connect("testielokuvat.db")

    lisays_alku = timeit()
