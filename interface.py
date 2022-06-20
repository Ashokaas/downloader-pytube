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

    label_titre["text"] = "Titre : " + dico["titre"]

    label_chaine["text"] = "Chaîne : " + dico["chaine"]

    label_vues["text"] = "Vues : " + dico["vues"]

    label_duree["text"] = "Durée : " + dico["duree"]



def clear_entry():
    entry_link.delete(0, 'end')



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

button = Button(tab1, text="❌", command=clear_entry)
button.pack()

button_link = Button(tab1, text="Convertir", command=info_video)
button_link.pack()



# -- Frame : information --
information = Frame(root)
information.config(width=270)
information.pack_propagate(False)
information.pack(side=RIGHT, fill="both")

    # Label Info
label_info = Label(information, text="Informations de la vidéo :", pady=15)
label_info.pack()
    # Miniature
miniature = Label(information, image=None, pady=20)
miniature.pack()
    # Titre
label_titre = Label(information, text=None, pady=6)
label_titre.pack()
    # Chaine
label_chaine = Label(information, text=None, pady=6)
label_chaine.pack()
    #Vues
label_vues = Label(information, text=None, pady=6)
label_vues.pack()
    # Duree
label_duree = Label(information, text=None, pady=6)
label_duree.pack()



# Affichage de la fenêtre
root.mainloop()
