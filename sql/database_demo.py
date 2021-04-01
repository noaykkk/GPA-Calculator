import sqlite3

conn = sqlite3.connect('course.db')

c = conn.cursor()

# c.execute("""CREATE TABLE Course (
#                  id integer primary key,
#                  course_id string(20),
#                  credit_hours float,
#                  grade string(3),
#                  quality_points float
#                   )""")

#c.execute("INSERT INTO Course VALUES(1,'ECE',3,'A',12)")

#c.execute("SELECT * FROM Course WHERE id=1")

#print(c.fetchone())

#c.execute("""UPDATE Course SET course_id='Math' WHERE  id=1""")

#c.execute("DELETE from Course WHERE id=1")

conn.commit()

conn.close()