
list1 = ['instagram',"facebook"]
list2 = ['link1',"link2"]
print(5 - len(list1))
dic = {}
for key in list1:
    for value in list2:
        dic[key] = value
        list2.remove(value)
        break

print (len(dic))
# dic = {"instagram":"link1", "facebook":"link2"}


for i in dic:
    print(i)
    print(dic[i])


