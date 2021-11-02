#!/usr/bin/env python3
# coding:utf-8
# INFOS FOR TESTING :
# UUID of jddev : f32958ee-848f-4f90-a830-99446a88afab
# flagindex of jddev : 51773
# coordinates of jddev : 136:159
# color of jddev : #10EDB8
import requests

mode = input("Mode :\n"
             "Récupérer le nom d'un pixel depuis son UUID (entrer r)\n"
             "Récupérer la liste de tous les pixels (entrer l)\n"
             "Entrer choix : ")  # on récup le mode

if mode == 'r':  # on récupère depuis l'UUID
    uuid = input("Entrez UUID : ")
    user_data = requests.get(f"https://admin.fouloscopie.com/users/{uuid}").json()

    data = {
            'flag_index': user_data['indexInFlag'],
            'color': user_data['hexColor'],
            'name': user_data['data']['last_name']
            }
    print(requests.get(f"https://admin.fouloscopie.com/users/{data}").json()['data'])
elif mode == 'l':
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
