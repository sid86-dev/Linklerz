data = {
    'name': 'SidDharth',
    'username': 'sid999'
}

import random

print(data['name'])

for item in data:
    data[item] = data[item].lower()


def createUsername(get_fullname):
    num = random.randint(11, 500)

    punctions = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

    fullname = ''

    for letter in get_fullname:
        if letter not in punctions:
            fullname += letter

    fullname.replace(" ", "")

    username = f"{fullname[:4]}{fullname[-3:]}{num}"

    return username


print(createUsername('sidd%$harth    Ro**y'))
