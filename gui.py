#!/usr/bin/env python3
# coding:utf-8
# INFOS FOR TESTING :
# UUID of jddev : f32958ee-848f-4f90-a830-99446a88afab
# indexInFlag of jddev : 51773
# coordinates of jddev : 136:159
# color of jddev : #10EDB8
# département of jddev : Désert de l'Ouest
import tkinter as tk
import tkinter.messagebox as msg
import math
import re
import webbrowser

import requests

from main import get_index_from_coordinates, get_user_raw_list, get_data_from_index, get_dpt_list

user_raw_list = []
dpt_list = []


def open_webpages(webpages: list[str] = None):
    """
        Opens all webpages of webpages
    :param webpages: list of webpages
    :return: nothing
    """
    if webpages is None:
        webpages = ["https://discord.gg/shF4BCdm"]
    for webpage in webpages:
        webbrowser.open_new_tab(webpage)


def def_user_raw_list():
    """
        Defines user_raw_list variable
    :return: nothing
    """
    global user_raw_list, dpt_list
    try:
        user_raw_list = get_user_raw_list()
        dpt_list = get_dpt_list()
        print("Loaded !")
    except requests.exceptions.ConnectionError:
        print("Failed : requests.exceptions.ConnectionError")
        msg.showerror("Erreur de réseau", "Impossible de charger le drapeau.\n"
                                          "Cela peut être dû à une absence de connexion Internet.\n"
                                          "Détails : requests.exceptions.ConnectionError")
        return

    loadButton.pack_forget()

    reloadButton.pack()
    coordinatesLabel.pack()
    coordinatesEntry.pack()
    getInfoButton.pack()
    coordinatesEntry.focus()


def re_def_user_raw_list():
    global user_raw_list, dpt_list
    try:
        user_raw_list = get_user_raw_list()
        dpt_list = get_dpt_list()
        print("Loaded !")
    except requests.exceptions.ConnectionError:
        print("Failed : requests.exceptions.ConnectionError")
        msg.showerror("Erreur de réseau", "Impossible de charger le drapeau.\n"
                                          "Cela peut être dû à une absence de connexion Internet.\n"
                                          "Détails : requests.exceptions.ConnectionError")
        return

    reloadButton.pack_forget()
    coordinatesLabel.pack_forget()
    coordinatesEntry.pack_forget()
    getInfoButton.pack_forget()
    nameLabel.pack_forget()
    colorLabel.pack_forget()
    indexLabel.pack_forget()
    uuidLabel.pack_forget()
    dptLabel.pack_forget()
    discordLabel.grid_forget()
    discordLinkLabel.grid_forget()
    discordFrame.pack_forget()

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
    dptLabel.pack_forget()
    discordLabel.grid_forget()
    discordLinkLabel.grid_forget()
    discordFrame.pack_forget()
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

    data = get_data_from_index(get_index_from_coordinates(*coordinates), user_raw_list, tuple(coordinates), dpt_list)

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

    dpt_text = "Département du pixel : "
    reg_text = "(Région : "
    discord_list = []
    dpt_list_ = []
    for dpt in data['dpt']:
        if dpt not in dpt_list_:
            dpt_list_.append(dpt)

    for dpt in dpt_list_:
        dpt_text += dpt['name'] + ' / '
        reg_text += dpt['region'] + ' / '
        discord_list.append(dpt['discord'])

    dpt_text = dpt_text[:len(dpt_text) - 3]
    reg_text = reg_text[:len(reg_text) - 3]
    reg_text += ")"
    if reg_text != "(Région : Coeur historique)":
        dpt_text += " " + reg_text
    dptLabel.config(text=dpt_text)

    discord_text = ""
    for discord_link in discord_list:
        discord_link = discord_link.replace("https://discord.com/invite", "discord.gg")
        discord_text += discord_link + ' / '

    discord_text = discord_text[:len(discord_text) - 3]

    discordLabel.config(text="Discord du département :")
    discordLinkLabel.config(text=discord_text, font='Tahoma 12 underline', fg='blue', cursor='hand2')

    indexLabel.config(text=f"Index du pixel : {data['index']}")
    uuidLabel.config(text=f"UUID du pixel : {data['uuid']}")

    nameLabel.pack()
    colorLabel.pack()
    dptLabel.pack()
    discordLabel.grid(row=0)
    discordLinkLabel.grid(column=1, row=0)
    discordLinkLabel.bind("<Button-1>", lambda e: open_webpages(discord_list))
    discordFrame.pack()
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
dptLabel = tk.Label(rootFrame, text='Département du pixel :', font='Tahoma')
discordFrame = tk.Frame(rootFrame)
discordLabel = tk.Label(discordFrame, text='Discord du département :', font='Tahoma')
discordLinkLabel = tk.Label(discordFrame, text='discord.gg/shF4BCdm', font='Tahoma 12 underline', cursor='hand2',
                            fg='blue')
indexLabel = tk.Label(rootFrame, text='Index du pixel :', font='Tahoma')
uuidLabel = tk.Label(rootFrame, text='UUID du pixel :', font='Tahoma')

titleLabel.pack()
loadButton.pack()
rootFrame.pack(expand=tk.YES)

root.mainloop()
