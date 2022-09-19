import courses

courses.create_tables()

t1 = courses.create_teacher("Antti Laaksonen")
t2 = courses.create_teacher("Erkki Kaila")

print(t1.nimi)