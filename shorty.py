import sqlite3

conn = sqlite3.connect('linklerz_.db')

c = conn.cursor()

# c.execute("""CREATE TABLE users(
#         username text,
#         password text)""")

# c.execute("INSERT INTO details VALUES('sid86','Github>https://github.com/sid86-dev', 'Linkedin>https://www.linkedin.com/in/siddhartha-roy-9052771b8/', 'Instagram>https://www.instagram.com/sid86__/', 'Portfolio>https://www.sid86.xyz/', 'Twitter>https://twitter.com/yourboysid_')")

c.execute("SELECT * FROM details WHERE username='sid86'")

data = c.fetchone()
links = 0
for i in data:
    if i == "":
        links -=1
    links +=1
print(links)
conn.commit()
conn.close()
