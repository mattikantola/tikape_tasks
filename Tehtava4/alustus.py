import sqlite3

data = sqlite3.connect("testi.db")

data.execute("BEGIN;")
data.execute("CREATE TABLE Testi (x INTEGER);")
data.execute("INSERT INTO Testi (x) VALUES (1);")
data.execute("COMMIT;")
