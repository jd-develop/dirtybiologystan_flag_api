#!/usr/bin/env python3
# coding:utf-8
# INFOS FOR TESTING :
# UUID of jddev : f32958ee-848f-4f90-a830-99446a88afab
# indexInFlag of jddev : 51773
# coordinates of jddev : 136:159
# color of jddev : #10EDB8
import tkinter as tk
import math
import re
from main import get_index_from_coordinates, get_user_raw_list, get_data_from_index

user_raw_list_ = []


def def_user_raw_list():
    """
        Defines user_raw_list variable
    :return: nothing
    """
    global user_raw_list_
    user_raw_list_ = get_user_raw_list()

    loadButton.pack_forget()

    reloadButton.pack()
    coordinatesLabel.pack()
    coordinatesEntry.pack()
    getInfoButton.pack()
    coordinatesEntry.focus()


def re_def_user_raw_list():
    global user_raw_list_

    user_raw_list_ = get_user_raw_list()

    reloadButton.pack_forget()
    coordinatesLabel.pack_forget()
    coordinatesEntry.pack_forget()
    getInfoButton.pack_forget()
    nameLabel.pack_forget()
    colorLabel.pack_forget()
    indexLabel.pack_forget()
    uuidLabel.pack_forget()

    reloadButton.pack()
    coordinatesLabel.pack()
    coordinatesEntry.pack()
    coordinatesEntry.focus()
    getInfoButton.pack()


def get_info():
    """
        Récupère les infos d'un Pixel
    :return: nothing
    """
    nameLabel.pack_forget()
    colorLabel.pack_forget()
    indexLabel.pack_forget()
    uuidLabel.pack_forget()
    try:
        if ':' in coordinatesEntry.get():
            coordinates = coordinatesEntry.get().strip('[').strip(']').split(':')
            if isinstance(coordinates, list):
                if len(coordinates) == 2:
                    coordinates[0] = int(coordinates[0])
                    coordinates[1] = int(coordinates[1])
                    if coordinates[0] <= 0 or coordinates[1] <= 0:
                        nameLabel.config(text="Désolé, ce pixel n'a pas l'air d'exister...")
                        nameLabel.pack()
                        return
                else:
                    nameLabel.config(text="Désolé, ce pixel n'a pas l'air d'exister...")
                    nameLabel.pack()
                    return
            else:
                nameLabel.config(text="Désolé, ce pixel n'a pas l'air d'exister...")
                nameLabel.pack()
                return
        else:
            nameLabel.config(text="Désolé, ce pixel n'a pas l'air d'exister...")
            nameLabel.pack()
            return
    except Exception:
        nameLabel.config(text="Désolé, ce pixel n'a pas l'air d'exister...")
        nameLabel.pack()
        return

    data = get_data_from_index(get_index_from_coordinates(*coordinates), user_raw_list_)

    if data['name'] == "does not exist":
        nameLabel.config(text="Désolé, ce pixel n'a pas l'air d'exister...")
        nameLabel.pack()
        return

    if data['name'] == "unattributed" and data['color'] == "unattributed":
        nameLabel.config(text="Désolé, ce pixel existe, mais il n'est pas attribué.")
        colorLabel.config(text="Peut être est-il dans un crash ¯\\_(ツ)_/¯", bg="whitesmoke", fg="black")
    else:
        nameLabel.config(text=f"Nom du pixel : {data['name']}")
        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', data['color']):  # la couleur est vraiment une couleur
            # convertir l'hexadécimal en RGB :
            (r, g, b) = tuple(int(data['color'].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

            # calculer l'indice de luminosité :
            darkness_index = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
            if darkness_index > 127.5:  # la couleur est clair, on met du noir
                colorLabel.config(text=f"Couleur du pixel : {data['color']}", bg=data['color'], fg="black")
            else:  # elle est claire, on met du noir
                colorLabel.config(text=f"Couleur du pixel : {data['color']}", bg=data['color'], fg="white")
        else:
            colorLabel.config(text=f"Couleur du pixel : {data['color']}", bg="white", fg="black")
    indexLabel.config(text=f"Index du pixel : {data['index']}")
    uuidLabel.config(text=f"UUID du pixel : {data['uuid']}")

    nameLabel.pack()
    colorLabel.pack()
    indexLabel.pack()
    uuidLabel.pack()


root = tk.Tk()
root.title("Interface graphique de l'API du drapeau du DirtyBiologyStan")
root.minsize(800, 400)

rootFrame = tk.Frame(root)

titleLabel = tk.Label(rootFrame, text="Drapeau du DirtyBiologyStan", font=('Tahoma',  15))
loadButton = tk.Button(rootFrame, text="Charger le drapeau", font="Tahoma", command=lambda: def_user_raw_list())
reloadButton = tk.Button(rootFrame, text="Recharger le drapeau", font="Tahoma", command=lambda: re_def_user_raw_list())

coordinatesLabel = tk.Label(rootFrame, text="Entrez des coordonnées sous la forme x:y :", font='Tahoma')
coordinatesEntry = tk.Entry(rootFrame)
getInfoButton = tk.Button(rootFrame, text="Obtenir les informations du pixel", font="Tahoma",
                          command=lambda: get_info())

nameLabel = tk.Label(rootFrame, text='Nom du pixel :', font='Tahoma')
colorLabel = tk.Label(rootFrame, text='Couleur du pixel :', font='Tahoma')
uuidLabel = tk.Label(rootFrame, text='UUID du pixel :', font='Tahoma')
indexLabel = tk.Label(rootFrame, text='index du pixel :', font='Tahoma')

titleLabel.pack()
loadButton.pack()
rootFrame.pack(expand=tk.YES)

root.mainloop()
