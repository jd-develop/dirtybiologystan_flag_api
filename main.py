#!/usr/bin/env python3
# coding:utf-8
# INFOS FOR TESTING :
# UUID of jddev : f32958ee-848f-4f90-a830-99446a88afab
# indexInFlag of jddev : 51773
# coordinates of jddev : 136:159
# color of jddev : #10EDB8
"""
Welcome ! This is a Python API for the flag of DirtyBiologyStan available here : https://fouloscopie.com/experiment/7
Don't forget to read the doc :)
"""
import requests
__version__ = "1.0"
__author__ = "jd-develop"


def get_user_raw_list() -> list[dict]:
    """
        It returns the list of all users.

        entityId is the UUID of the fouloscopie.com user, which the API is private
        author is the UUID of the pixel, which the API is open
        hexColor is a color, but not automatically a hex (because of troll people)
        indexInFlag is a pixel index, but due to website crashes it's not the index in the user_raw_list (for example,
                my indexInFlag is 51773 but my index in user_raw_list is 50063.

    :return: user_raw_list: list[dict{'entityId', 'author', 'hexColor', 'indexInFlag'}]
    """
    print("Fetching https://api-flag.fouloscopie.com/flag...")
    flag_request = requests.get('https://api-flag.fouloscopie.com/flag')
    user_raw_list = flag_request.json()
    return user_raw_list


def get_index_from_coordinates(x: int = 1, y: int = 1):
    """
        Calculates the index of user_raw_list (get_user_raw_list()) from coordinates.

    :param x: int = 1
    :param y: int = 1
    :return: index in user_raw_list (get_user_raw_list())
    """
    if x < (2*y - 1):
        return (x + 2 * (y-1)**2) - 1
    else:
        return (y + ((x+1) // 2) * (2*((x+1)//2) - x % 2 - 1)) - 1


def get_data_from_index(index: int = 0, user_raw_list: list[dict] = None):
    """
        Get the data from the index and the user raw list (get_user_raw_list())

        data is a dict under this shape :
            {
                'uuid' : uuid of the user ('author' in an element of the user_raw_list)
                'index': pixel index ('indexInFlag' in an element of the user_raw_list, different from the index param!)
                'name' : username ('last_name' in key 'data' of the user from https://admin.fouloscopie.com/users/(uuid)
                'color': color of the pixel ('hexColor' in an element of the user_raw_list)
            }
        warning : 'color' is not automatically an hex, due to trolls

    :param index: int = 0
    :param user_raw_list: user_raw_list: list[dict] = get_user_raw_list()
    :return: data: dict
    """
    if user_raw_list is None:
        user_raw_list = get_user_raw_list()

    user_raw_data = requests.get(f"https://admin.fouloscopie.com/users/{user_raw_list[index]['author']}").json()

    uuid = user_raw_list[index]['author']
    index_ = user_raw_list[index]['indexInFlag']
    name = user_raw_data['data']['last_name']
    color = user_raw_list[index]['hexColor']
    return {
        'uuid': uuid,
        'index': index_,
        'name': name,
        'color': color

    }

# thanks for using this API ;)
