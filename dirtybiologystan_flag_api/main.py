#!/usr/bin/env python3
# coding:utf-8
# INFOS FOR TESTING :
# UUID of jddev : f32958ee-848f-4f90-a830-99446a88afab
# indexInFlag of jddev : 51773
# coordinates of jddev : 136:159
# color of jddev : #10EDB8
# département of jddev : Désert de l'Ouest (région : La Méridionale)
import json.decoder

import requests
__version__ = "1.3.4"
__author__ = "jd-develop"


def get_user_raw_list(do_i_print: bool = False) -> list[dict]:
    """Return the list of all users.
        The list have the shape :
            [{'entityId', 'author', 'hexColor', 'indexInFlag'}, ...] (for each user)

        entityId is the UUID of the fouloscopie.com user, which the API is private
        author is the UUID of the pixel, which the API is open
        hexColor is a color, but not automatically a hex (because of troll people)
        indexInFlag is a pixel index, but due to website crashes it's not the index in the user_raw_list (for example,
                my indexInFlag is 51773 but my index in user_raw_list is 50063)

        WARNING : execution of this function may take a while !!
        WARNING 2 : it can return the string "404 not found : maybe website is down" when the website is down
                    (it was happening frequently at the beginning of the experience)

        This function fetches https://api-flag.fouloscopie.com/flag

    :param do_i_print: defines if a text have to be printed or not. Optional, by default, False.
    :type do_i_print: bool

    :return: user_raw_list: the list of raw users without usernames.
    :rtype: list[dict]
    """

    if do_i_print:
        print("Fetching https://flag-api.dirtybiology.fouloscopie.com/flag... (it may take a while...)")
    flag_request = requests.get('https://flag-api.dirtybiology.fouloscopie.com/flag')
    if flag_request == '404 page not found':
        return '404 not found : maybe website is down'
    elif flag_request == '{"statusCode":404,"message":"Cannot GET /flag","error":"Not Found"}':
        return '404 not found : maybe website is down'
    user_raw_list = flag_request.json()
    return user_raw_list


def get_dpt_list(do_i_print: bool = False) -> list[dict]:
    """Return the list of all départements.
        The list have the shape :
            [{'min', 'max', 'name', 'region', 'discord'}, ...] (for each département)

        min is the dict {'x', 'y'} of the minimum coordinates of the département
        max is the dict {'x', 'y'} of the maximum coordinates of the département
        name is the name of the département
        region is the name of the région of the département
        discord is the invite link to the Discord Server of the département

        WARNING : execution of this function may take a while !!
        WARNING 2 : it can return strings "404 not found : maybe website is down" or "Bad Gateway" when the website
                    is down (contact CoDaTi on https://github.com/codati if it is the case)

        This function fetches https://api.codati.ovh/departements/

    :param do_i_print: defines if a text have to be printed or not. Optional, by default, False.
    :type do_i_print: bool

    :return: dpt_list: a list of départements
    :type: DptList
    """

    if do_i_print:
        print("Fetching https://api.codati.ovh/departements/... (it may take a while...)")
    dpt_request = requests.get('https://api.codati.ovh/departements/')
    if dpt_request == '404 page not found':
        return '404 not found : maybe website is down'
    elif dpt_request == '':
        return '404 not found : maybe website is down'
    elif dpt_request == 'Bad Gateway':
        return 'Bad Gateway'
    try:
        dpt_list = dpt_request.json()
    except json.decoder.JSONDecodeError:
        return dpt_request
    return dpt_list


def get_index_from_coordinates(x: int = 1, y: int = 1) -> int:
    """Calculates the index in the user_raw_list (get_user_raw_list()) from coordinates.

    :param x: the x of the pixel. By default, 1
    :type x: int
    :param y: the y of the pixel. By default, 1
    :type y: int
    :return: index in user_raw_list (get_user_raw_list())
    :rtype: int
    """

    if x < (2*y - 1):
        return (x + 2 * (y-1)**2) - 1
    else:
        return (y + ((x+1) // 2) * (2*((x+1)//2) - x % 2 - 1)) - 1


def get_data_from_index(index: int = 0, user_raw_list: list[dict] = None, coordinates: tuple = None,
                        dpt_list: list[dict] = None) -> dict:
    """Get the data from the index and the user raw list (get_user_raw_list())

    data is a dict under this shape :
        {
            'uuid' : uuid of the user ('author' in user_raw_list)
            'index': pixel index ('indexInFlag' in user_raw_list, different from the index param!)
            'name' : name of the pixel
            'color': color of the pixel ('hexColor' in user_raw_list)
            'dpt': département name of the pixel
        }
    warning : 'color' is not automatically a hex, due to trolls

    :param index: the index returned by get_index_from_coordinates. By default, 0.
    :type index: int
    :param user_raw_list: the list returned by get_user_raw_list()
    :type user_raw_list: list[dict]
    :param coordinates: coordinates (x, y). By default, (1, 1)
    :type coordinates: tuple[int]
    :param dpt_list: the list returned by get_dpt_list() (départements list)
    :type dpt_list: list[dict]
    :return: data (see above for more info)
    :rtype: dict
    """

    if user_raw_list is None:
        user_raw_list = get_user_raw_list()
    if coordinates is None:
        coordinates = (1, 1)
    if dpt_list is None:
        dpt_list = get_dpt_list()

    try:
        user_raw_data = requests.get(f"https://admin.fouloscopie.com/users/{user_raw_list[index]['author']}").json()
    except IndexError:
        return {
            'uuid': "",
            'index': "",
            'name': "does not exist",
            'color': "",
            'dpt': ""
        }

    try:
        uuid = user_raw_list[index]['author']
        index_ = user_raw_list[index]['indexInFlag']
        name = user_raw_data['data']['last_name']
        color = user_raw_list[index]['hexColor']
        dpt = get_dpt_from_coordinates(coordinates, dpt_list)
        return {
            'uuid': uuid,
            'index': index_,
            'name': name,
            'color': color,
            'dpt': dpt
        }
    except KeyError:
        try:
            uuid = user_raw_list[index]['author']
            index_ = user_raw_list[index]['indexInFlag']
            name = "unattributed"
            color = user_raw_list[index]['hexColor']
            dpt = get_dpt_from_coordinates(coordinates, dpt_list)
            return {
                'uuid': uuid,
                'index': index_,
                'name': name,
                'color': color,
                'dpt': dpt
            }
        except KeyError:
            uuid = user_raw_list[index]['author']
            index_ = user_raw_list[index]['indexInFlag']
            name = "unattributed"
            color = "unattributed"
            dpt = get_dpt_from_coordinates(coordinates, dpt_list)
            return {
                'uuid': uuid,
                'index': index_,
                'name': name,
                'color': color,
                'dpt': dpt
            }


def get_dpt_from_coordinates(coordinates: tuple = (1, 1), dpt_list: list[dict] = None) -> list[dict]:
    """Return the département(s) of a pixel from the coordinates, in a list.

        A département returned have the shape :
            {'min', 'max', 'name', 'region', 'discord'}

        min is the dict {'x', 'y'} of the minimum coordinates of the département
        max is the dict {'x', 'y'} of the maximum coordinates of the département
        name is the name of the département
        region is the name of the région of the département
        discord is the invite link to the Discord Server of the département

    :param coordinates: coordinates of the pixel. By default, (1, 1)
    :type coordinates: tuple(x, y)
    :param dpt_list: the dpt list from get_dpt_list()
    :type dpt_list: list[dict]
    :return: a list of matching départements from the dpt_list
    :rtype: list[dict]
    """

    if dpt_list is None:
        dpt_list = get_dpt_list()

    x = coordinates[0]
    y = coordinates[1]
    matching_dpt_list = []
    for dpt in dpt_list:
        matching = dpt['min']['x'] <= x <= dpt['max']['x'] and dpt['min']['y'] <= y <= dpt['max']['y']
        if matching:
            matching_dpt_list.append(dpt)

    return matching_dpt_list


# thanks for using this API ;)
