import json

linkdic = {}


def api_conv(linkdic):
    data = []
    for item in linkdic:
        dic = {}
        # print(linkdic[item])
        try:
            dic["link"] = linkdic[item]
            dic["name"] = item
        except:
            pass
        data.append(dic)

    dic = {}
    if len(data) == 5:
        pass
    else:
        for _ in range(5-len(data)):
            dic["link"] = "noarg"
            dic["name"] = "noarg"
            data.append(dic)
    return data

#         var data = [
#     { id: 1, name: "bob" },
#     { id: 2, name: "john" },
#     { id: 3, name: "jake" },
# ];

if __name__ == "__main__":
    data = api_conv(linkdic)
    print(data)
    # print(type(data))
    print(len(data))