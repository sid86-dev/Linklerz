import json

linkdic = {"Github":"https://github.com/sid86-dev","Linkedln":"https://www.linkedin.com/in/siddhartha-roy-9052771b8/","Portfolio":"https://www.sid86.xyz/","Store":"https://trelerz.com/","Twitter":"https://twitter.com/yourboysid_"}


def api_conv(linkdic):
    data = []
    for item in linkdic:
        dic = {}
        # print(linkdic[item])
        dic["link"] = linkdic[item]
        dic["name"] = item
        data.append(dic)

    # data = json.dumps(data)
    return data

#         var data = [
#     { id: 1, name: "bob" },
#     { id: 2, name: "john" },
#     { id: 3, name: "jake" },
# ];

if __name__ == "__main__":
    data = api_conv(linkdic)
    print(data)
    print(type(data))