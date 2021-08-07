from os import name
import sqlite3

def delete_data(delete_name):
    conn = sqlite3.connect('linklerz_.db')

    c = conn.cursor()

    c.execute("SELECT * FROM details WHERE username='sid86'")

    data = c.fetchone()


    # print(data)
    length = len(data)

    names = []
    links = []

    lst  = []

    for i in range(1,length):
        lst.append(data[i])

    my_dic = {}

    # print(lst)

    for i in range(len(lst)):
        if ">" in lst[i]:
            item = lst[i]
            seperate = item.split('>')
            # print(seperate)
            my_dic[seperate[0]] = seperate[1]
        else:
            my_dic[""] = ""
       

    my_dic.pop(delete_name)

    # print(my_dic)

    final_lst = []
    for item in my_dic:
        if item != "":
            final_lst.append(f"{item}>{my_dic[item]}")

    return final_lst

lst = delete_data("Github")

if len(lst) < 5:
    for i in range(5-len(lst)):
        lst.append("")

str = f"INSERT INTO details VALUES('sid86','{lst[0]}', '{lst[1]}', '{lst[2]}', '{lst[3]}', '{lst[4]}')"

# print(lst)

print(str)


