import json
username = 'xuehong'
password = 'ewq'
email = 'xue@hot.com'

with open('user_data.json', mode='r') as file:
    data = json.load(file)
    all_users = data['users']

    for user in all_users:
        _username = list(user.keys())[0]
        _user_data = list(user.values())
        print(_user_data[0]['password'])
        print(_user_data[0]['email'])
        