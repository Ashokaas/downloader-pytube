from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from main import informations_video
from pytube import YouTube
from urllib.request import urlretrieve


# == FONCTIONS ==
def info_video():
    
    dico = informations_video(YouTube(entry_link.get()))

    urlretrieve(dico['url_minia'], 'video/temp/minia_temp/img.jpg')
    global img
    img = ImageTk.PhotoImage(Image.open('video/temp/minia_temp/img.jpg').resize((4*38, 3*38)))
    miniature["image"] = img

    label_titre["text"] = dico["titre"]

    label_chaine["text"] = dico["chaine"]

    label_vues["text"] = dico["vues"]

    label_duree["text"] = dico["duree"]



# -- Configuration de la fenêtre
root = Tk()
root.title("Numérisateur Original Universel Biochimique 2")  

root.resizable(False, False)

hauteur = 400
largeur = 800
root.geometry(str(largeur) + 'x' + str(hauteur))



# -- Configuration des onglets Video et Options de téléchargement
tabControl = ttk.Notebook(root)

tab1 = Frame(tabControl)
tab2 = Frame(tabControl)

style_menu = ttk.Style()
style_menu.configure('TNotebook.Tab', font='Calibri 11')

tabControl.add(tab1, text ='Vidéo')
tabControl.add(tab2, text ='Options de téléchargement')
tabControl.pack(expand = 1, fill ="both", side=LEFT)



# -- Frame : tab1 -> root

label_link = Label(tab1, text='Lien de la vidéo :', pady=20)
label_link.pack()

entry_link = Entry(tab1, width=50)
entry_link.pack()

button_link = Button(tab1, text="Convertir", command=info_video)
button_link.pack()



# -- Frame : information --
information = Frame(root)
information.pack(side=RIGHT, fill="both")


miniature = Label(information, image=None, pady=20)
miniature.pack()

label_titre = Label(information, text=("Titre : "))
label_titre.pack()

label_chaine = Label(information, text=("Chaîne : "))
label_chaine.pack()

label_vues = Label(information, text=("Vues : "))
label_vues.pack()

label_duree = Label(information, text=("Durée : "))
label_duree.pack()


# Affichage de la fenêtre
root.mainloop()
