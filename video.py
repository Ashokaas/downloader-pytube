from tkinter import *
from pytube import YouTube
from convertions import *

def info_video():
    
    dico = informations_video(YouTube(entry_link.get()))

    urlretrieve(dico['url_minia'], 'video/temp/minia_temp/img.jpg')
    global img
    format = [4, 3]
    zoom = 38
    img = ImageTk.PhotoImage(Image.open('video/temp/minia_temp/img.jpg').resize((format[0]*zoom, format[1]*zoom)))
    miniature = Label(information, image=img, width=330, pady=20)
    miniature.pack()

    label_titre = Label(information, text=("Titre : " + (dico["titre"])))
    label_titre.pack()

    label_chaine = Label(information, text=("Chaîne : " + dico["chaine"]))
    label_chaine.pack()

    label_vues = Label(information, text=("Vues : " + dico["vues"]))
    label_vues.pack()

    label_duree = Label(information, text=("Durée : " + dico["duree"]))
    label_duree.pack()