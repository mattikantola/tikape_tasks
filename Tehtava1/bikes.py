import sqlite3

def distance_of_user(user: str):

    data = sqlite3.connect("bikes.db")
    data.isolation_level = None
    cur = data.cursor()
    sum_of_distance = cur.execute(f"SELECT SUM(T.distance) \
                    FROM Users U LEFT JOIN Trips T ON U.id = T.user_id \
                    WHERE U.name = '{user}'").fetchone()
    return sum_of_distance[0]

def speed_of_user(user: str):

    data = sqlite3.connect("bikes.db")
    data.isolation_level = None
    cur = data.cursor()
    sum_of_time, sum_of_distance = cur.execute(f"SELECT SUM(T.duration), SUM(T.distance) \
                                    FROM Users U LEFT JOIN Trips T ON U.id = T.user_id \
                                    WHERE U.name = '{user}'").fetchone()
    return round(60*sum_of_distance/sum_of_time/1000, 2)

def duration_in_each_city(day: str):

    data = sqlite3.connect("bikes.db")
    data.isolation_level = None
    cur = data.cursor()
    city_sum = cur.execute(f"SELECT C.name, SUM(T.duration) \
                            FROM Stops S JOIN Cities C ON S.city_id = C.id \
                            JOIN Trips T ON S.id = T.from_id \
                            WHERE T.day = '{day}' GROUP BY C.id").fetchall()

    return city_sum

def users_in_city(city: str):

    return None

def trips_on_each_day(city: str):

    return None

def most_popular_start(city: str):

    return None