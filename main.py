#!/usr/bin/env python3
# coding:utf-8

import requests

flagRequest = requests.get('https://api-flag.fouloscopie.com/flag')
print(flagRequest.headers['content-type'])

user_raw_list = flagRequest.json()
cityzen_list: list[dict] = []  # dict('flag_index', 'color', 'name')

for user in user_raw_list:
    user_data = requests.get(f"https://admin.fouloscopie.com/users/{user['author']}").json()['data']
    cityzen_list.append(
        {
            'flag_index': user['indexInFlag'],
            'color': user['hexColor'],
            'name': user_data['last_name']
        }
    )
    print(cityzen_list[len(cityzen_list) - 1])
