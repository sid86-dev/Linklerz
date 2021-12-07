import redis
import json

with open('config.json', 'r') as f:
    params = json.load(f)["params"]

r = redis.Redis(host=params['redis_host'], port=params['redis_port'], password=params['redis_password'])


def add_cache_list(userid, list):
    # r.mset({userid:list})
    r.rpush(userid, *list)
    # r.psetex('name', 1000, "siddharth")  # milisecond

    # for item in list:
    #     r.rpush(userid, item)

    # Add more than one value through the tail of the Redis list

    # r.rpush(noSQLList, "Riak", "CouchDB")


def add_cache(userid, code):
    # r.mset({userid:list})
    r.psetex(userid, 60000, code)  # milisecond

def add_authid(userid, authid):
    # r.mset({userid:list})
    r.psetex(authid, 10000, userid)  # milisecond

def get_cache(userid):
    if (r.exists(userid)):
        return r.get(userid)
    else:
        return "Code Expired"

def get_userid(authid):
    if (r.exists(authid)):
        return r.get(authid)
    else:
        return "Code Expired"


def get_cache_list(userid):
    # if (r.exists(userid)):
    #     return r.r(userid)
    # else:
    #     return "cannot find the key"

    # Print the contents of the Redis list
    l = []
    while (r.llen(userid) != 0):
        # l.append(r.rpop(userid))
        l.append(r.rpop(userid))
    return l


if __name__ == '__main__':
    user_id = 'sdc8s44'
    add_cache(user_id, ['applo', 'banana', 'pinaple'])
    id = get_cache(user_id)
    print(id)
