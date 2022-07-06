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
from RangeSlider.RangeSlider import RangeSliderH, RangeSliderV
# likes dislikes
import requests
import json
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


def convertir_url(video_url):
    _video_ID = video_url.replace("https://youtu.be/", "")
    _video_ID = _video_ID.replace("https://youtube.com/watch?v=", "")
    _video_ID = _video_ID.replace("https://www.youtu.be/", "")
    _video_ID = _video_ID.replace("https://www.youtube.com/watch?v=", "")
    _video_ID = _video_ID.replace("&feature=share", "")

    return _video_ID

def get_likes_and_dislikes(video_url):
    main_api = "https://returnyoutubedislikeapi.com/votes?videoId="
    video_id = convertir_url(video_url)
    res = requests.get(main_api + video_id)
    response = json.loads(res.text)
    return response["likes"], response["dislikes"], response["likes"]+response["dislikes"]
    

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
    



def ffmpeg_extract_subclip(filename, t1, t2, targetname=None):
    """ Makes a new video file playing video file ``filename`` between
        the times ``t1`` and ``t2``. """
    name, ext = os.path.splitext(filename)
    if not targetname:
        T1, T2 = [int(1000*t) for t in [t1, t2]]
        targetname = "%sSUB%d_%d.%s" % (name, T1, T2, ext)
    
    cmd = [get_setting("FFMPEG_BINARY"),"-y",
           "-ss", "%0.2f"%t1,
           "-i", filename,
           "-t", "%0.2f"%(t2-t1),
           "-map", "0", "-vcodec", "copy", "-acodec", "copy", targetname]
    
    call(cmd)




def telechargement(video):


    def progress(streams, chunk: bytes, bytes_remaining: int):
        contentsize = video.filesize
        size = contentsize - bytes_remaining
        print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), poids_video(size), "/", poids_video(contentsize), end='')



    debut = int(combobox_debut_h.get())*3600 + int(combobox_debut_min.get())*60 + int(combobox_debut_sec.get())
    fin =  int(combobox_fin_h.get())*3600 + int(combobox_fin_min.get())*60 + int(combobox_fin_sec.get())

    if fin > yt.length or debut > fin or debut == fin:
        return "Erreur Non"

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


    if debut != 0 or fin != yt.length:
        ffmpeg_extract_subclip(sortie + '/' + file_name, debut, fin)

    print(sortie)
    subprocess.Popen(r'explorer /select,"' + sortie.replace('/', '\\') + '\\' + file_name + r'"')
    


def telecharger_miniature():
    global sortie, short_url
    urlretrieve('http://img.youtube.com/vi/' + short_url + '/maxresdefault.jpg', sortie + '/' + formatage_video_name_without_extension(yt.title) + '.jpg')


    
 # -- Convertir vidéo --
def convertir_video():

    try:
        global url
        url = str(entry_link.get())

        global short_url
        short_url = convertir_url(str(entry_link.get()))
        
        def telecharger():
            global sortie
            sortie = entry_chemin_destination.get()
            telechargement(yt.streams.get_by_itag(id.get()))

        global yt
        

        yt = YouTube(entry_link.get())



        global img

        urlretrieve('http://img.youtube.com/vi/' + short_url + '/maxresdefault.jpg', 'video/temp/minia_temp/img.jpg')

        img = ImageTk.PhotoImage(Image.open('video/temp/minia_temp/img.jpg').resize((16*15, 9*15)))

        miniature["image"] = img
        supprimer_fichier_dossier('video/temp/minia_temp')
        label_titre["text"] = "Titre : " + titre_ligne(yt.title)
        label_chaine["text"] = "Chaîne : " + yt.author
        label_vues["text"] = "Vues : " + nb_vues(yt.views)
        h, min, sec = duree(yt.length)
        label_duree["text"] = "Durée : " + str(h) + 'h' + str(min) + 'm' + str(sec) + 's'
        
        # LIKES / DISLIKES
            # Récupération des données
        likes, dislikes, somme = get_likes_and_dislikes(entry_link.get())
            # Ligne pour faire le rapport
        ratio.create_line(0, 0, likes/somme*200, 0, fill="blue", width=7)
        ratio.create_line(likes/somme*200, 0, (likes/somme)*200+(dislikes/somme)*200, 0, fill="red", width=7)
            # Likes
        label_likes["fg"] = 'blue'
        label_likes["text"] = str(likes) + '👍'
            
        label_pourcentages_likes["text"] = str(round(likes/somme*100)) + '%'
        label_pourcentages_likes["fg"] = 'blue'
        
        label_dislikes["fg"] = 'red'
        label_dislikes["text"] = str(dislikes) + '👎'

        label_pourcentages_dislikes["text"] = str(round(dislikes/somme*100)) + '%'
        label_pourcentages_dislikes["fg"] = 'red'

        video = yt.streams
        liste_video, i = choix_video(video)

        button_telecharger_video = Button(information, text='Télécharger', command=telecharger, pady=4, padx=9)
        button_telecharger_video.pack(pady=(20, 0))

        button_telecharger_miniature = Button(information, text='Télécharger la miniature', command=telecharger_miniature)
        button_telecharger_miniature.pack(pady=(20, 0))




        # Frame : Choisir durée de la vidéo à télécharger
        global combobox_debut_h, combobox_debut_min, combobox_debut_sec, combobox_fin_h, combobox_fin_min, combobox_fin_sec
        select_time = Frame(tab2)
        select_time.grid(column=0, row=i+1, columnspan=(i//12+1)*12, pady=30)

            # DEBUT
                # Lael début
        label_debut = Label(select_time, text='Début : ')
        label_debut.grid(column=0, row=0, sticky=E)
                # Heure
                    # Combobox heure
        combobox_debut_h = ttk.Combobox(select_time, values=[i for i in range(24)], width=2, justify='center', state='readonly')
        combobox_debut_h.current(0)
        combobox_debut_h.grid(column=1, row=0)
                    # Label heure 
        label_debut_h = Label(select_time, text='h')
        label_debut_h.grid(column=2, row=0)
                # Minute
                    # Combobox minute
        combobox_debut_min = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
        combobox_debut_min.current(0)
        combobox_debut_min.grid(column=3, row=0)
                    # Label min
        label_debut_min = Label(select_time, text='m')
        label_debut_min.grid(column=4, row=0)
                # Seconde
                    # Combobox sec
        combobox_debut_sec = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
        combobox_debut_sec.current(0)
        combobox_debut_sec.grid(column=5, row=0)
                    # Label sec
        label_debut_sec = Label(select_time, text='s')
        label_debut_sec.grid(column=6, row=0)

            # FIN
                # Label fin
        label_fin = Label(select_time, text='Fin : ')
        label_fin.grid(column=0, row=1, sticky=E)
                # Heure
                    # Combobox heure
        combobox_fin_h = ttk.Combobox(select_time, values=[i for i in range(24)], width=2, justify='center', state='readonly')
        combobox_fin_h.current(h)
        combobox_fin_h.grid(column=1, row=1)
                    # Label heure
        label_fin_h = Label(select_time, text='h')
        label_fin_h.grid(column=2, row=1)
                # Minute
                    # Combobox minute
        combobox_fin_min = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
        combobox_fin_min.current(min)
        combobox_fin_min.grid(column=3, row=1)
                    # Label minutes
        label_fin_min = Label(select_time, text='m')
        label_fin_min.grid(column=4, row=1)
                # Secondes
                    # Combobox seconde
        combobox_fin_sec = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
        combobox_fin_sec.current(sec)
        combobox_fin_sec.grid(column=5, row=1)
                    # Label seconde
        label_fin_sec = Label(select_time, text='s')
        label_fin_sec.grid(column=6, row=1)


        # Afficher automatiquement le deuxième onglet
        tabControl.select(tab2)


    except pytube.exceptions.RegexMatchError:
        label_erreur["text"] = 'Erreur de lien'
        print("oui")




def dialogue_chemin():
    global sortie
    sortie = filedialog.askdirectory()
    entry_chemin_destination.delete(0, len(entry_chemin_destination.get()))
    entry_chemin_destination.insert(0, sortie)


    


# == FIN FONCTIONS ==




# -- Configuration de la fenêtre
root = Tk()
root.title("Numérisateur Original Universel Biochimique 2") 
root.iconbitmap('images/youtube.ico')

root.resizable(False, False)

hauteur = 550
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

def touche_convertir(event):
    convertir_video()

root.bind('<Return>', touche_convertir)



# -- Frame : tab1 -> root

label_link = Label(tab1, text='Lien de la vidéo :', pady=20)
label_link.grid(column=0, row=0, columnspan=2)

entry_link = Entry(tab1, width=50)
entry_link.grid(column=0, row=1, columnspan=2)
entry_link.bind("<Button - 3>", copy)

photo = PhotoImage(file = r"images/delete.png").subsample(20, 20) 

button_delete = Button(tab1, command=clear_entry, image=photo)
button_delete.grid(column=1, row=1, padx=(0, 75))

button_link = Button(tab1, text="Convertir", command=convertir_video, padx=15, pady=6)
button_link.grid(column=0, row=2, pady=15, columnspan=2)

label_erreur = Label(tab1, text=None, fg='red')
label_erreur.grid(column=0, row=3, columnspan=2)

tab1.columnconfigure(0, weight=1)


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
miniature.pack(pady=10)
    # Titre
label_titre = Label(information, text=None)
label_titre.pack(pady=5)
    # Chaine
label_chaine = Label(information, text=None)
label_chaine.pack(pady=5)
    #Vues
label_vues = Label(information, text=None)
label_vues.pack(pady=5)
    # Duree
label_duree = Label(information, text=None)
label_duree.pack(pady=5)
    # Pouces bleus/rouges
frame_ratio = Frame(information)
frame_ratio.pack()
ratio = Canvas(frame_ratio, width=200, height=3.5, bd=0, highlightthickness=0)
ratio.pack(pady=10)
    # Likes / Dislikes
        # Likes
            # Likes
label_likes = Label(frame_ratio, text=None)
label_likes.pack(side='left', anchor='n', padx=(35, 0))
            # Pourcentage Likes
label_pourcentages_likes = Label(frame_ratio, text=None)
label_pourcentages_likes.pack(side='left', anchor='n', padx=(0, 30))
        # Dislikes
            # Dislikes
label_dislikes = Label(frame_ratio, text=None)
label_dislikes.pack(side='right', anchor='n', padx=(0, 35))
            # Pourcentage Dislikes
label_pourcentages_dislikes = Label(frame_ratio, text=None)
label_pourcentages_dislikes.pack(side='right', anchor='n', padx=(30, 0))



# -- Frame: Paramètres --
label_chemin_destination = Label(tab3, text='Destination par défaut :')
label_chemin_destination.grid(column=0, row=0, padx=(10, 0), pady=(10, 0))

entry_chemin_destination = Entry(tab3, width=0)
entry_chemin_destination.grid(column=1, row=0, padx=(10, 5), pady=(10, 0))
entry_chemin_destination.insert(0, sortie)

selec_chemin_destination = Button(tab3, text="Parcourir", command=dialogue_chemin)
selec_chemin_destination.grid(column=2, row=0, pady=(10, 0), padx=(10, 0))




# Affichage de la fenêtre
if __name__ == "__main__":
    root.mainloop()

# https://www.youtube.com/watch?v=bBkH4mQK050
    
