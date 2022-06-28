import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from pytube import YouTube
from urllib.request import urlretrieve
import pytube.exceptions
# import progressbar as progress
from colorama import init, Fore
import os
import subprocess as sp
from moviepy.config import get_setting
from subprocess import call
# -- Importation des fonctions supplémentaires
from convertions import *


# == FONCTIONS ==



sortie = os.path.expanduser('~') + r"\Desktop"
print(sortie)


# J'écrit "vidéo" sans accent dans les commentaires mais L'ORTHOGRAPHE IL A CHANGE




# -- Clear python console --
clear = lambda: os.system('cls')

def clear_entry():
    entry_link.delete(0, 'end')

def copy(event):
    lien = str(entry_link.clipboard_get())
    if "youtube" in lien:
        clear_entry()
        entry_link.insert(0, lien)


# -- Fusionne l'audio et la video --
def fusionner_video_audio(video,audio,output, vcodec='copy',
                             acodec='copy', ffmpeg_output=False,
                             logger = 'bar'):
    """ merges video file ``video`` and audio file ``audio`` into one
        movie file ``output``. """
    cmd = [get_setting("FFMPEG_BINARY"), "-y", "-i", audio,"-i", video,
             "-vcodec", vcodec, "-acodec", acodec, output]
             
    call(cmd)




def supprimer_fichier_dossier(dossier):
    for fichier in os.listdir(dossier):
        os.remove(dossier + "/" + fichier)



    

def audio(yt):
    # Définie la qualité maximale audio en kbps
    qualite_max = 0
    for stream in yt.streams.filter(mime_type="audio/webm"):
        # S'il est un flux audio
        if stream.abr != None:
            # Supprimer le "kbps" pour le garder que le nombre en (int) -- exemple : "128kbs" -> 128
            qualite_audio = int(stream.abr[0:-4])
            # Si elle est supérieur à la qulité précédemment enregistré la remplace
            if qualite_audio > qualite_max:
                qualite_max = qualite_audio
    # Récupération du flux audio possédant la meilleure qualité
    qualite_max = str(qualite_max) + "kbps"
    video = yt.streams.filter(mime_type="audio/webm", abr=qualite_max)
    # On retourne le premier élément de la liste car même s'il n'y a qu'un seul meilleur flux audio, le .filter retourne un liste
    return video[0]



global itag_to_download
def choix_video(video):
    # Création d'une liste de dictionnaires qui stocke les informations importantes à l'utilisateur ainsi qu'un ID pour choisir la video à télécharger
    liste_video = []
    # Pour chaque flux "stream" dans video:
    for stream in video:
        # S'il est une video/n'est pas un audio
        if stream.mime_type != "audio/mp4" and stream.mime_type != "audio/webm":
            # Ajout d'un dico contenant des infos cool qur la video
            liste_video.append({"type": stream.mime_type, "resolution": stream.resolution, "fps": (str(stream.fps) + "fps"), "taille": poids_video(stream.filesize), "itag": stream.itag})
    # Tri décroissant en fonction : resolution, fps, taille
    liste_video.sort(key=lambda element:(int(element['resolution'][0:-1]), int(element['fps'][0:-3]), float(element['taille'][0:-2])), reverse=True)
    # Affichage des informations pour l'utilisateur sur chaque video et d'un ID pour pouvoir en sélectionner une
    global id
    id = IntVar()
    colonne = 0
    ligne = 0
    print(len(liste_video))
    for i in range(len(liste_video)):
        if i > 12:
            colonne = 6
            ligne = -13
        Label(tab2, text=("ID" + str(i))).grid(column=0+colonne, row=i+ligne)
        Label(tab2, text=liste_video[i]["type"]).grid(column=1+colonne, row=i+ligne)
        Label(tab2, text=liste_video[i]["resolution"]).grid(column=2+colonne, row=i+ligne)
        Label(tab2, text=liste_video[i]["fps"]).grid(column=3+colonne, row=i+ligne)
        Label(tab2, text=liste_video[i]["taille"]).grid(column=4+colonne, row=i+ligne)
        Radiobutton(tab2, variable=id, value=liste_video[i]["itag"]).grid(column=5+colonne, row=i+ligne)

    return liste_video, i
    





def telechargement(video):


    def progress(streams, chunk: bytes, bytes_remaining: int):
        contentsize = video.filesize
        size = contentsize - bytes_remaining
        print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), poids_video(size), "/", poids_video(contentsize), end='')


    if video.is_progressive == False:
        audio_for_video = audio(yt)
        print(audio_for_video)

        file_name = formatage_video_name(audio_for_video.default_filename)
        video_path = 'video/temp/video_temp'
        audio_path = 'video/temp/audio_temp'

        print("Téléchargement de l'audio en cours...")
        audio_for_video.download(output_path=audio_path, filename=file_name)

        print("Téléchargement de la video en cours...")
        video.download(output_path=video_path, filename=file_name)

        print("Fusion de la video et de l'audio en cours...")
        fusionner_video_audio((video_path + '/' + file_name), (audio_path + '/' + file_name), (sortie + '/' + file_name))

        supprimer_fichier_dossier('video/temp/video_temp')
        supprimer_fichier_dossier('video/temp/audio_temp')
    else:
        file_name = formatage_video_name(video.default_filename)
        video_path = 'video/temp/video_temp'
        print("Téléchargement de la video en cours...")
        video.download(output_path=sortie + '/', filename=file_name)

    print(sortie)
    subprocess.Popen(r'explorer /select,"' + sortie.replace('/', '\\') + '\\' + file_name + r'"')
    



    
 # -- Convertir vidéo --
def convertir_video():

    def telecharger():
        global sortie
        sortie = entry_chemin_destination.get()
        telechargement(yt.streams.get_by_itag(id.get()))

    global yt
    

    if "youtube" not in entry_link.get():
        clear_entry()
        return print("Erreur de lien")

    yt = YouTube(entry_link.get())

    for stream in yt.streams:
        print(stream)

    urlretrieve(yt.thumbnail_url, 'video/temp/minia_temp/img.jpg')
    global img
    img = ImageTk.PhotoImage(Image.open('video/temp/minia_temp/img.jpg').resize((4*38, 3*38)))
    miniature["image"] = img
    label_titre["text"] = "Titre : " + titre_ligne(yt.title)
    label_chaine["text"] = "Chaîne : " + yt.author
    label_vues["text"] = "Vues : " + nb_vues(yt.views)
    label_duree["text"] = "Durée : " + duree(yt.length)

    video = yt.streams
    liste_video, i = choix_video(video)

    button_id = Button(tab2, text='Télécharger', command=telecharger)
    button_id.grid(column=1, row=i+1)

    tabControl.select(tab2)

def dialogue_chemin():
    global sortie
    sortie = filedialog.askdirectory()
    entry_chemin_destination.delete(0, len(entry_chemin_destination.get()))
    entry_chemin_destination.insert(0, sortie)


    


# == FIN FONCTIONS ==




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
tab3 = Frame(tabControl)

style_menu = ttk.Style()
style_menu.configure('TNotebook.Tab', font='Calibri 11')

tabControl.add(tab1, text ='Vidéo')
tabControl.add(tab2, text ='Options de téléchargement')
tabControl.add(tab3, text = 'Paramètres')

tabControl.pack(expand = 1, fill ="both", side=LEFT)

tabControl.select(tab1)



# -- Frame : tab1 -> root

label_link = Label(tab1, text='Lien de la vidéo :', pady=20)
label_link.grid(column=0, row=0)

entry_link = Entry(tab1, width=50)
entry_link.grid(column=0, row=1)
entry_link.bind("<Button - 3>", copy)

button_delete = Button(tab1, text="❌", command=clear_entry)
button_delete.grid(column=1, row=1, sticky="w")

button_link = Button(tab1, text="Convertir", command=convertir_video)
button_link.grid(column=0, row=2)

label_erreur = Label(tab1, text="Erreur : ")

# tab1.columnconfigure(0, weight=1)


# -- Frame : information --
information = Frame(root)
information.config(width=270)
information.pack_propagate(False)
information.pack(side=RIGHT, fill="both")

    # Label Info
label_info = Label(information, text="Informations de la vidéo :", pady=15)
label_info.pack()
    # Miniature
miniature = Label(information, image=None)
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


# -- Frame: Paramètres --
entry_chemin_destination = Entry(tab3, width=0)
entry_chemin_destination.grid(column=0, row=0, padx=(10, 5), pady=(10, 0))
entry_chemin_destination.insert(0, sortie)

selec_chemin_destination = Button(tab3, text="Parcourir", command=dialogue_chemin)
selec_chemin_destination.grid(column=1, row=0, pady=(10, 0))




# Affichage de la fenêtre
root.mainloop()