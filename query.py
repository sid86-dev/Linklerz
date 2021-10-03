import sqlite3

conn = sqlite3.connect('user.db')

c = conn.cursor()

# c.execute("""CREATE TABLE users(
#         username text,
#         password text)""")


# c.execute(f"INSERT INTO users VALUES('sid00','jjjjij', 'sod@gmail.com', 'free')")


c.execute("SELECT * FROM users WHERE email='sid86harth@gmail.com'")
data = c.fetchone() 
c.execute("DELETE FROM users WHERE email='sid86harth@gmail.com'")

password = data[1]
username = data[0]
email = data[2]
c.execute(f"INSERT INTO users VALUES('{username}','{password}', '{email}', 'free', 'yes')")

# print(data)
conn.commit()
conn.close()
