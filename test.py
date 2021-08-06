from typing_extensions import final


lst1 = ['Github', '', '', '', '']
lst2 = ['https://github.com/sid86-86', '', '', '', '']
lst3 = ['', '', '', '', '', '']
lst4 =['', '', '', '', '', '']


def data_processing(lst1, lst2, lst3, lst4):    
    newlst1 = []
    newlst2 = []

    for a in lst1:
        if a != "":
            newlst1.append(a)
    for b in lst2:
        if b != "":
            newlst2.append(b)

    for c in lst3:
        if c != "":
            newlst1.append(c)
        else:
            newlst1.append(c)
    for d in lst4:
        if d != "":
            newlst2.append(d)
        else:
            newlst2.append("")
    length = len(newlst2)

    # print(newlst1)
    # print(newlst2)

    finaldic = {}
    try:
        for y in range(5):
            if newlst1[y] != "":
                if newlst1[y] != "":
                    finaldic[f"link{y+1}"] = f"{newlst1[y]}>{newlst2[y]}"
            else :
                finaldic[f"link{y+1}"] = f""
        print(finaldic)
    except:
        print(WindowsError)
    # length = len(finaldic)
    # final_links = {}
    # # print(finaldic)
    # for items in finaldic:
    #     print(items)
    #     if finaldic[items] == "":

    # print(f"value={finaldic['link3']}")
    # print(newlst2)
    # for items in dic =  
    str = f"INSERT INTO details VALUES('sid86','{finaldic['link1']}', '{finaldic['link2']}', '{finaldic['link3']}', '{finaldic  ['link4']}', '{finaldic['link5']}')"
    # dic = {"apple":"world"}
    # print(dic[lst1[1]])
    return str

process = data_processing(lst1,lst2,lst3,lst4)
print(process)
