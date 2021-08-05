import sqlite3

conn = sqlite3.connect('user.db')

c = conn.cursor()

# c.execute("""CREATE TABLE users(
#         username text,
#         password text)""")

# c.execute("INSERT INTO users VALUES('sid86', 'siddharth18')")

c.execute("SELECT * FROM users WHERE username='sid86'")

print(c.fetchone())

conn.commit()
conn.close()
