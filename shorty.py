import sqlite3

conn = sqlite3.connect('user.db')

c = conn.cursor()

# c.execute("""CREATE TABLE details(
#         username text,
#         link text)""")

# c.execute("INSERT INTO details VALUES('raju', 'https://www.instagram.com/raju__/')")

c.execute("SELECT * FROM details WHERE username='raju'")

print(c.fetchone())

conn.commit()
conn.close()
