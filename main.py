# =====================================
#      IMPORTATIONS DES LIBRAIRIES 
# =====================================

# Tkinter
from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image

# Pytube
from pytube import YouTube
import pytube.exceptions

# OS
import os

# Montage video et audio
from moviepy.config import get_setting
import subprocess

# Récupérer Miniature
from urllib.request import urlretrieve

# Recupérer Likes et Dislikes
import requests, json

# Convertir et mettre en forme
import convertions

# Ne pas faire crash le programme lors du téléchargement
import threading

# Historique
import csv
from csv import writer

# Notifications
from win10toast import ToastNotifier




# ===================
#      FONCTIONS
# ===================

global sortie, video, liste_widgets
liste_widgets = []

# Importation de la sortie depuis sortie.data
with open("sortie.data", "r") as fichier_sortie:
    sortie = fichier_sortie.readline()



def inserer_texte_console(texte, clear_console=False, root_update=False):
    output_log.configure(state='normal')
    if clear_console == True:
        output_log.delete('0.0', 'end')
    output_log.insert(END, str(texte))
    output_log.configure(state='disabled')
    if root_update == True:
        root.update()



# -- Supprimer le texte de ntry_link --
def clear_entry():
    entry_link.delete(0, 'end')



# -- Copie l'URL dans entry_link si l'utilisateur fait un click droit --
def copy(event):
    lien = str(entry_link.clipboard_get())
    clear_entry()
    entry_link.insert(0, lien)



# -- Fusionne l'audio et la video --
def fusionner_video_audio(video,audio,output, vcodec='copy', acodec='copy', ffmpeg_output=False, logger = 'bar'):
    cmd = [get_setting("FFMPEG_BINARY"), "-y", "-i", audio,"-i", video, "-vcodec", vcodec, "-acodec", acodec, output]
    subprocess.call(cmd)



# -- Enregistre un extrait d'une vidéo 
def ffmpeg_extract_subclip(filename, t1, t2, targetname=None):
    name, ext = os.path.splitext(filename)
    if not targetname:
        T1, T2 = [int(1000*t) for t in [t1, t2]]
        targetname = "%sSUB%d_%d.%s" % (name, T1, T2, ext)
    
    cmd = [get_setting("FFMPEG_BINARY"),"-y",
           "-ss", "%0.2f"%t1,
           "-i", filename,
           "-t", "%0.2f"%(t2-t1),
           "-map", "0", "-vcodec", "copy", "-acodec", "copy", targetname]
    
    subprocess.call(cmd)



# -- Supprime tout les documents d'un fichier
def supprimer_fichier_dossier(dossier):
    for fichier in os.listdir(dossier):
        os.remove(dossier + "/" + fichier)



# -- Permet de garder uniquement l'ID de la vidéo --
def convertir_url(video_url):
    video_ID = video_url.replace("https://youtu.be/", "")
    video_ID = video_ID.replace("https://youtube.com/watch?v=", "")
    video_ID = video_ID.replace("https://www.youtu.be/", "")
    video_ID = video_ID.replace("https://www.youtube.com/watch?v=", "")
    video_ID = video_ID.replace("&feature=share", "")

    return video_ID



# -- Récupère les likes et les dislikes d'une vidéo --
def get_likes_and_dislikes(video_url):
    main_api = "https://returnyoutubedislikeapi.com/votes?videoId="
    video_id = convertir_url(video_url)
    res = requests.get(main_api + video_id)
    response = json.loads(res.text)
    return response["likes"], response["dislikes"], response["likes"]+response["dislikes"]
    


# -- Récupère le fichier audio d'un .webm ou .mp4 possédant la meilleure qualité --
def audio(yt, type):
    # Définie la qualité maximale audio en kbps
    qualite_max = 0
    for stream in yt.streams.filter(mime_type="audio/"+type):
        # S'il est un flux audio
        if stream.abr != None:
            # Supprimer le "kbps" pour le garder que le nombre en (int) -- exemple : "128kbs" -> 128
            qualite_audio = int(stream.abr[0:-4])
            # Si elle est supérieur à la qulité précédemment enregistré la remplace
            if qualite_audio > qualite_max:
                qualite_max = qualite_audio
    # Récupération du flux audio possédant la meilleure qualité
    qualite_max = str(qualite_max) + "kbps"
    audio = yt.streams.filter(mime_type="audio/"+type, abr=qualite_max)
    # On retourne le premier élément de la liste car même s'il n'y a qu'un seul meilleur flux audio, le .filter retourne un liste
    return audio[0]



# -- Affiche tout les flux de la vidéo --
global itag_to_download
def choix_video(streams):
    # Création d'une liste de dictionnaires qui stocke les informations importantes à l'utilisateur ainsi qu'un ID pour choisir la video à télécharger
    liste_video = []
    liste_audio = []
    global liste_widgets

    # Pour chaque flux "stream" dans video:
    for stream in streams:
        type_stream = stream.mime_type.split("/")
        if type_stream[0] == 'video':
            type_stream[0] = 'Vidéo'
        elif type_stream[0] == 'audio':
            type_stream[0] = 'Audio'
        type_stream[1] = '.' + type_stream[1]
        type_stream = {"type": type_stream[0], "extension": type_stream[1]}
        # S'il est une video/n'est pas un audio
        if type_stream['type'] == "Vidéo":
            # Ajout d'un dico contenant des infos cool qur la video
            liste_video.append({"type": type_stream["type"], "extension": type_stream["extension"], "resolution": stream.resolution, "fps": (str(stream.fps) + "fps"), "taille": convertions.poids_video(stream.filesize), "itag": stream.itag})
        elif type_stream['type'] == "Audio":
            liste_audio.append({"type": type_stream["type"], "extension": type_stream["extension"], "kbps": stream.abr, "taille": convertions.poids_video(stream.filesize), "itag": stream.itag})
    # Tri décroissant en fonction : resolution, fps, taille
    liste_video.sort(key=lambda element:(int(element['resolution'][0:-1]), int(element['fps'][0:-3]), float(element['taille'][0:-2])), reverse=True)
    # Affichage des informations pour l'utilisateur sur chaque video et d'un ID pour pouvoir en sélectionner une
    global id
    id = IntVar()
    colonne = 0
    ligne = 0
    x = 2
    y = 2
    
    for i in range(len(liste_video)):
        if i > 12:
            colonne = 6
            ligne = -13
            liste_widgets.append(Label(tab2_video, text='Type'))
            liste_widgets[-1].grid(row=0, column=1+colonne)
            liste_widgets.append(Label(tab2_video, text='Extension'))
            liste_widgets[-1].grid(row=0, column=2+colonne)
            liste_widgets.append(Label(tab2_video, text='Resolution'))
            liste_widgets[-1].grid(row=0, column=3+colonne)
            liste_widgets.append(Label(tab2_video, text='FPS'))
            liste_widgets[-1].grid(row=0, column=4+colonne)
            liste_widgets.append(Label(tab2_video, text='Taille'))
            liste_widgets[-1].grid(row=0, column=5+colonne)
            
        liste_widgets.append(Radiobutton(tab2_video, variable=id, value=liste_video[i]["itag"]))
        liste_widgets[-1].grid(column=0+colonne, row=1+i+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_video, text=liste_video[i]["type"]))
        liste_widgets[-1].grid(column=1+colonne, row=1+i+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_video, text=liste_video[i]["extension"]))
        liste_widgets[-1].grid(column=2+colonne, row=1+i+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_video, text=liste_video[i]["resolution"]))
        liste_widgets[-1].grid(column=3+colonne, row=1+i+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_video, text=liste_video[i]["fps"]))
        liste_widgets[-1].grid(column=4+colonne, row=1+i+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_video, text=liste_video[i]["taille"]))
        liste_widgets[-1].grid(column=5+colonne, row=1+i+ligne, padx=x, pady=y)
    print(liste_audio)
    colonne = 0
    ligne = 0
    x = 2
    y = 2
    
    for e in range(len(liste_audio)):
        if e > 12:
            colonne = 6
            ligne = -13
            liste_widgets.append(Label(tab2_audio, text='Type'))
            liste_widgets[-1].grid(row=0, column=1+colonne)
            liste_widgets.append(Label(tab2_audio, text='Extension'))
            liste_widgets[-1].grid(row=0, column=2+colonne)
            liste_widgets.append(Label(tab2_audio, text='Bitrate'))
            liste_widgets[-1].grid(row=0, column=3+colonne)
            liste_widgets.append(Label(tab2_audio, text='Taille'))
            liste_widgets[-1].grid(row=0, column=4+colonne)

        liste_widgets.append(Radiobutton(tab2_audio, variable=id, value=liste_audio[e]["itag"]))
        liste_widgets[-1].grid(column=0+colonne, row=1+e+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_audio, text=liste_audio[e]["type"]))
        liste_widgets[-1].grid(column=1+colonne, row=1+e+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_audio, text=liste_audio[e]["extension"]))
        liste_widgets[-1].grid(column=2+colonne, row=1+e+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_audio, text=liste_audio[e]["kbps"]))
        liste_widgets[-1].grid(column=3+colonne, row=1+e+ligne, padx=x, pady=y)
        liste_widgets.append(Label(tab2_audio, text=liste_audio[e]["taille"]))
        liste_widgets[-1].grid(column=4+colonne, row=1+e+ligne, padx=x, pady=y)



# -- Affiche l'avancé du téléchargement --
def progress(streams, chunk: bytes, bytes_remaining: int):
    global video, progress_bar, is_video
    # On fait avancer la progress_bar uniquement si le fichier est une vidéo
    if is_video == True:
        # Taille totale du fichier
        contentsize = video.filesize
        # Ce qu'il reste à télécharger
        size = contentsize - bytes_remaining
        # Affichage dans la console
        inserer_texte_console(str(round(size/contentsize*100)) + '%' + '\n' + convertions.poids_video(size) + '/' + convertions.poids_video(contentsize), clear_console=True)
        # Actualisation sur la progress_bar
        progress_bar['value'] = int(round(size/contentsize*100))
        # Actualisation de la fenêtre
        root.update()



# -- Télécharger la vidéo --
def telechargement(yt, id, combobox_debut_h, combobox_debut_min, combobox_debut_sec, combobox_fin_h, combobox_fin_min, combobox_fin_sec, liste_widgets):
    global video, is_video

    # Récupération du flux selectionnée
    video = yt.streams.get_by_itag(id)

    # Récupération du début et de la fin en seconde
    debut = int(combobox_debut_h)*3600 + int(combobox_debut_min)*60 + int(combobox_debut_sec)
    fin =  int(combobox_fin_h)*3600 + int(combobox_fin_min)*60 + int(combobox_fin_sec)

    # Gestion des erreurs sur le début et la fin
    if fin > yt.length:
        inserer_texte_console('La fin est supérieure à la durée totale de la vidéo', clear_console=True, root_update=True)
        return None
    if debut > fin:
        inserer_texte_console('Le début est supérieur à la fin', clear_console=True, root_update=True)
        return None
    if debut == fin:
        inserer_texte_console('Le début est égal à la fin', clear_console=True, root_update=True)
        return None

    # On formate le titre de la vidéo (suppression des : caractères spéciaux, espaces, emojis, etc)
    file_name = convertions.formatage_video_name(video.default_filename)

    # Si le flux ne contient pas l'audio
    if video.is_progressive == False:
        # On télécharge le fichier audio associé à l'extension du fichier vidéo
        audio_for_video = audio(yt, video.mime_type.split('/')[1])

        # On définie la sortie de la video temporaire et de l'audio temporaire
        video_path = 'video/temp/video_temp'
        audio_path = 'video/temp/audio_temp'

        # Téléchargement de l'audio
        is_video = False
        inserer_texte_console("\nTéléchargement de l'audio en cours...", clear_console=True, root_update=True)
        audio_for_video.download(output_path=audio_path, filename=file_name)
                
        # Téléchargement de la vidéo
        is_video = True
        inserer_texte_console("\nTéléchargement de la video en cours...", clear_console=True, root_update=True)
        video.download(output_path=video_path, filename=file_name)

        # Fusion de la vidéo et de l'audio
        inserer_texte_console("\nFusion de la video et de l'audio en cours...", clear_console=True, root_update=True)
        fusionner_video_audio((video_path + '/' + file_name), (audio_path + '/' + file_name), (sortie + '/' + file_name))

        # Suppression de la video temporaire et de l'audio temporaire
        supprimer_fichier_dossier('video/temp/video_temp')
        supprimer_fichier_dossier('video/temp/audio_temp')
    
    # Si le flux contient l'audio
    else:
        # Téléchargement de la vidéo
        inserer_texte_console("Téléchargement de la video en cours...", clear_console=True, root_update=True)
        is_video = True
        video.download(output_path=sortie + '/', filename=file_name)

    # Si l'utilisateur veut télécharger une portion de la vidéo
    if debut != 0 or fin != yt.length:
        ffmpeg_extract_subclip(sortie + '/' + file_name, debut, fin)
        inserer_texte_console("\nSéparation de l'extrait selectionné...", clear_console=True, root_update=True)

    inserer_texte_console("Téléchargement de la video terminé !", clear_console=True, root_update=True)

    print(sortie)

    # Ouverture du dossier contenant la vidéo
    subprocess.Popen(r'explorer /select,"' + sortie.replace('/', '\\') + '\\' + file_name + r'"')
    
    global button_telecharger_video, button_telecharger_miniature
    button_telecharger_miniature.destroy()
    button_telecharger_video.destroy()

    ToastNotifier().show_toast("Numérisateur Original Universel Biochimique", "Le téléchargement de votre vidéo '" + video.title + "' est terminé", icon_path='miniatures_history'+short_url+'jpg')

    

# -- Télécharger la miniature dans la meilleure qualité disponible --
def telecharger_miniature():
    global sortie, short_url
    urlretrieve('http://img.youtube.com/vi/' + short_url + '/maxresdefault.jpg', sortie + '/' + convertions.formatage_video_name_without_extension(yt.title) + '.jpg')



def new_thread_telechargement():
    global yt, liste_widgets
    threading.Thread(target=telechargement, args=(yt, id.get(), combobox_debut_h.get(), combobox_debut_min.get(), combobox_debut_sec.get(), combobox_fin_h.get(), combobox_fin_min.get(), combobox_fin_sec.get(), liste_widgets,)).start()



 # -- Convertir vidéo --
def convertir_video():
    try:
        inserer_texte_console('Convertion en cours...', clear_console=True, root_update=True)
        global url, short_url, yt, img, liste_widgets

        for widget in liste_widgets:
            widget.destroy()


        if '&' in entry_link.get():
            for l in range(len(entry_link.get())):
                if entry_link.get()[l] == '&':
                    lien_temp = entry_link.get()[0:l]
                    clear_entry()
                    entry_link.insert(0, lien_temp)
                    root.update()
                    break
    

        # URL de la vidéo
        url = str(entry_link.get())

        # ID de la vidéo
        short_url = convertir_url(str(entry_link.get()))
        print(short_url)

        # Convertion de la vidéo
        yt = YouTube(entry_link.get(), on_progress_callback=progress)


        
        nouvelle_video_history = [entry_link.get(), yt.views, yt.author, yt.length]
        with open('history.csv', 'a', newline='') as file:
            writer_object = writer(file, delimiter=";")
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(nouvelle_video_history)  
            # Close the file object
            file.close()


        # MINIATURE
            # Téléchargement de la miniature
        urlretrieve('http://img.youtube.com/vi/' + short_url + '/maxresdefault.jpg', 'miniatures_history/' + short_url + '.jpg')
            # Redimensionnement de la miniature
        img = ImageTk.PhotoImage(Image.open('miniatures_history/' + short_url + '.jpg').resize((16*15, 9*15)))
            # Affichage de la miniature
        miniature["image"] = img

        

        # TITRE 
        label_titre["text"] = "Titre : " + convertions.titre_ligne(yt.title)

        # CHAINE
        label_chaine["text"] = "Chaîne : " + yt.author

        # VUES
        label_vues["text"] = "Vues : " + convertions.nb_vues(yt.views)

        # DUREE
        h, min, sec = convertions.duree(yt.length)
            # Si durée est inferieur à 1 minutes
        if yt.length < 60:
            label_duree["text"] = "Durée : " + str(sec) + "s"
            # Sinon si la durée est inferieur à  1 heure
        elif yt.length < 3600:
            label_duree["text"] = "Durée : " + str(min) + "m " + str(sec) + "s"
            # Si la durée est supérieure à 1 heure
        else:
            label_duree["text"] = "Durée : " + str(h) + "h " + str(min) + "m " + str(sec) + "s"
        
        # LIKES / DISLIKES
            # Récupération des données
        likes, dislikes, somme = get_likes_and_dislikes(entry_link.get())
            # Ligne pour faire le rapport
        ratio.create_line(0, 0, likes/somme*200, 0, fill="blue", width=7)
        ratio.create_line(likes/somme*200, 0, (likes/somme)*200+(dislikes/somme)*200, 0, fill="red", width=7)
            # LIKES
                # Likes
        label_likes["fg"] = 'blue'
        label_likes["text"] = '👍' + convertions.nb_vues(likes)
                # Pourcentage likes
        label_pourcentages_likes["text"] = str(round(likes/somme*100)) + '%'
        label_pourcentages_likes["fg"] = 'blue'
            # DISLIKES
                # Dislikes
        label_dislikes["fg"] = 'red'
        label_dislikes["text"] = convertions.nb_vues(dislikes) + '👎'
                # Pourcentage Dislikes
        label_pourcentages_dislikes["text"] = str(round(dislikes/somme*100)) + '%'
        label_pourcentages_dislikes["fg"] = 'red'

        # Affichage de tout les flux
        choix_video(yt.streams)


        global button_telecharger_video, button_telecharger_miniature
        # Bouton Télécharger Vidéo
        button_telecharger_video = Button(information, text='Télécharger', command=new_thread_telechargement, pady=4, padx=9)
        button_telecharger_video.pack(pady=(20, 0))

        # Bouton Télécharger miniature
        button_telecharger_miniature = Button(information, text='Télécharger la miniature', command=telecharger_miniature)
        button_telecharger_miniature.pack(pady=(20, 0))


        combobox_fin_h.current(h)
        combobox_fin_min.current(min)
        combobox_fin_sec.current(sec)


        # Afficher automatiquement le deuxième onglet
        tabControl.select(tab2)

        inserer_texte_console('\nConvertion effectuée !', clear_console=True)


    except pytube.exceptions.RegexMatchError:
        inserer_texte_console('Erreur de lien', clear_console=True)



# -- Permet à l'utilisateur de choisir la sortie par défaut
def dialogue_chemin():
    global sortie
    # Selection de la sortie par l'utilisateur
    sortie = filedialog.askdirectory()
    # Ecriture de la sortie dans sortie.data
    with open ('sortie.data', "w") as fichier_sortie:
        fichier_sortie.write(sortie)
    # Ecriture de la sortie dans entry_chemin_destination
    entry_chemin_destination.delete(0, len(entry_chemin_destination.get()))
    entry_chemin_destination.insert(0, sortie)



# -- Permet à l'utilisateur de choisir le Burean en tant que sortie par défaut
def select_desktop():
    global sortie
    # Affecte le Bureau comme sortie par défaut
    sortie = os.path.expanduser('~') + r"\Desktop"
    # Ecriture de la sortie dans entry_chemin_destination
    entry_chemin_destination.delete(0, len(entry_chemin_destination.get()))
    entry_chemin_destination.insert(0, sortie)
    # Ecriture de la sortie dans sortie.data
    with open('sortie.data', 'w') as fichier_sortie:
        fichier_sortie.write(sortie)




# =======================
#         TKINTER
# =======================



# -- Configuration de la fenêtre
root = Tk()
root.title("Numérisateur Original Universel Biochimique 2") 
root.iconbitmap('images/youtube.ico')

root.resizable(False, False)

hauteur = 600
largeur = 850
root.geometry(str(largeur) + 'x' + str(hauteur))



# -- Configuration de tabControl_et_Console
tabControl_et_Console = Frame(root)
tabControl_et_Console.pack(expand = 1, fill ="both", side=LEFT)



# -- Configuration de TabControl
tabControl = ttk.Notebook(tabControl_et_Console, height=497)

tab1 = Frame(tabControl)
tab2 = Frame(tabControl)
tab3 = Frame(tabControl)
tab4 = Frame(tabControl)

style_menu = ttk.Style()
style_menu.configure('TNotebook.Tab', font='Calibri 11')

tabControl.add(tab1, text='Convertion')
tabControl.add(tab2, text='Options de téléchargement')
tabControl.add(tab3, text='Paramètres')
tabControl.add(tab4, text='Historique')

tabControl.pack(fill ="both")

tabControl.select(tab1)



# -- Convertion

label_link = Label(tab1, text='Lien de la vidéo :', pady=20)
label_link.grid(column=0, row=0, columnspan=2)

entry_link = Entry(tab1, width=50)
entry_link.grid(column=0, row=1, columnspan=2)
entry_link.bind("<Button - 3>", copy)

photo = PhotoImage(file = r"images/delete.png").subsample(20, 20) 

button_delete = Button(tab1, command=clear_entry, image=photo)
button_delete.grid(column=1, row=1, padx=(0, 103))

button_link = Button(tab1, text="Convertir", command=convertir_video, padx=15, pady=6)
button_link.grid(column=0, row=2, pady=15, columnspan=2)

tab1.columnconfigure(0, weight=1)

def touche_entree(event):
    if tabControl.index("current") == 0:
        convertir_video()
    if tabControl.index("current") == 1:
        new_thread_telechargement()

root.bind('<Return>', touche_entree)



# -- Options de téléchargement --
tab_2_Control = ttk.Notebook(tab2)

tab2_video = Frame(tab_2_Control, height=380)
tab2_audio = Frame(tab_2_Control, height=380)

tab_2_Control.add(tab2_video, text='Vidéo')
tab_2_Control.add(tab2_audio, text='Audio')

tab_2_Control.pack(expand=False, fill="x", side=TOP)



# -- Paramètres --
label_chemin_destination = Label(tab3, text='Destination par défaut :')
label_chemin_destination.grid(column=0, row=0, padx=(10, 0), pady=(10, 0))

entry_chemin_destination = Entry(tab3, width=0)
entry_chemin_destination.grid(column=1, row=0, padx=(10, 5), pady=(10, 0))
entry_chemin_destination.insert(0, sortie)

selec_chemin_destination = Button(tab3, text="Parcourir", command=dialogue_chemin)
selec_chemin_destination.grid(column=2, row=0, pady=(10, 0), padx=(10, 0))

button_desktop = Button(tab3, text='Par défault (Bureau)', command=select_desktop)
button_desktop.grid(column=3, row=0, pady=(10, 0), padx=(10, 0))



# -- Information --
information = Frame(root)
information.config(width=270)
information.pack_propagate(False)
information.pack(side=RIGHT, fill="y")

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
label_pourcentages_likes.pack(side='left', anchor='n', padx=(5, 30))
        # Dislikes
            # Dislikes
label_dislikes = Label(frame_ratio, text=None)
label_dislikes.pack(side='right', anchor='n', padx=(0, 35))
            # Pourcentage Dislikes
label_pourcentages_dislikes = Label(frame_ratio, text=None)
label_pourcentages_dislikes.pack(side='right', anchor='n', padx=(30, 5))



# -- Console --
frame_console = Frame(tabControl_et_Console)
frame_console.pack(fill="both", expand=1)
frame_console.pack_propagate(False)

global progress_bar
progress_bar = ttk.Progressbar(frame_console, orient='horizontal', length=450, mode='determinate')
progress_bar.pack()

output_log = Text(frame_console, state='disabled')
output_log.pack()






label_video_type_1 = Label(tab2_video, text='Type')
label_video_type_1.grid(row=0, column=1)
label_video_extension_1 = Label(tab2_video, text='Extension')
label_video_extension_1.grid(row=0, column=2)
label_video_resolution_1 = Label(tab2_video, text='Resolution')
label_video_resolution_1.grid(row=0, column=3)
label_video_fps_1 = Label(tab2_video, text='FPS')
label_video_fps_1.grid(row=0, column=4)
label_video_taille_1 = Label(tab2_video, text='Taille')
label_video_taille_1.grid(row=0, column=5)

Label(tab2_audio, text='Type').grid(row=0, column=1)
Label(tab2_audio, text='Extension').grid(row=0, column=2)
Label(tab2_audio, text='Bitrate').grid(row=0, column=3)
Label(tab2_audio, text='Taille').grid(row=0, column=4)




# FRAME : Choisir durée de la vidéo à télécharger
global combobox_debut_h, combobox_debut_min, combobox_debut_sec, combobox_fin_h, combobox_fin_min, combobox_fin_sec, select_time
select_time = Frame(tab2)
select_time.pack(expand=1)
pady_select_time = 5
    # DEBUT
        # Label début
label_debut = Label(select_time, text='Début : ')
label_debut.grid(column=0, row=0, sticky=E, pady=pady_select_time)
        # Heure
            # Combobox heure
combobox_debut_h = ttk.Combobox(select_time, values=[i for i in range(24)], width=2, justify='center', state='readonly')
combobox_debut_h.current(0)
combobox_debut_h.grid(column=1, row=0, pady=pady_select_time)
            # Label heure 
label_debut_h = Label(select_time, text='h')
label_debut_h.grid(column=2, row=0, pady=pady_select_time)
        # Minute
            # Combobox minute
combobox_debut_min = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
combobox_debut_min.current(0)
combobox_debut_min.grid(column=3, row=0, pady=pady_select_time)
            # Label min
label_debut_min = Label(select_time, text='m')
label_debut_min.grid(column=4, row=0, pady=pady_select_time)
        # Seconde
            # Combobox sec
combobox_debut_sec = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
combobox_debut_sec.current(0)
combobox_debut_sec.grid(column=5, row=0, pady=pady_select_time)
            # Label sec
label_debut_sec = Label(select_time, text='s')
label_debut_sec.grid(column=6, row=0, pady=pady_select_time)

    # FIN
        # Label fin
label_fin = Label(select_time, text='Fin : ')
label_fin.grid(column=0, row=1, sticky=E, pady=pady_select_time)
        # Heure
            # Combobox heure
combobox_fin_h = ttk.Combobox(select_time, values=[i for i in range(24)], width=2, justify='center', state='readonly')
combobox_fin_h.current(0)
combobox_fin_h.grid(column=1, row=1, pady=pady_select_time)
            # Label heure
label_fin_h = Label(select_time, text='h')
label_fin_h.grid(column=2, row=1, pady=pady_select_time)
        # Minute
            # Combobox minute
combobox_fin_min = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
combobox_fin_min.current(0)
combobox_fin_min.grid(column=3, row=1, pady=pady_select_time)
            # Label minutes
label_fin_min = Label(select_time, text='m')
label_fin_min.grid(column=4, row=1, pady=pady_select_time)
        # Secondes
            # Combobox seconde
combobox_fin_sec = ttk.Combobox(select_time, values=[i for i in range(60)], width=2, justify='center', state='readonly')
combobox_fin_sec.current(0)
combobox_fin_sec.grid(column=5, row=1, pady=pady_select_time)
            # Label seconde
label_fin_sec = Label(select_time, text='s')
label_fin_sec.grid(column=6, row=1, pady=pady_select_time)



historique = []
with open('history.csv', newline='') as history_file:
    reader = csv.DictReader(history_file, delimiter=';')
    for row in reader:
        historique.append(row)

historique = historique[::-1][0:min(len(historique), 6)]
print(historique)



label_history_minia = Label(tab4, text='Miniature')
label_history_minia.grid(column=0, row=0)

label_history_minia = Label(tab4, text='Titre')
label_history_minia.grid(column=1, row=0)

label_history_minia = Label(tab4, text='Vues')
label_history_minia.grid(column=2, row=0)

label_history_minia = Label(tab4, text='Chaîne')
label_history_minia.grid(column=3, row=0)

label_history_minia = Label(tab4, text='Durée')
label_history_minia.grid(column=4, row=0)

widgets_historique = []
for r in range(min(len(historique), 5)):
    widgets_historique.append(Label(tab4, image=None))
    widgets_historique[-1].grid(column=0, row=r+1, padx=6, pady=5)
    widgets_historique.append(ImageTk.PhotoImage(Image.open('miniatures_history/' + convertir_url(historique[r]['url']) + '.jpg').resize((16*6, 9*6))))
    widgets_historique[-2]['image'] = widgets_historique[-1]
    widgets_historique.append(Label(tab4, text=convertions.titre_ligne(YouTube(historique[r]['url']).title), font=("TkDefaultFont", 7)))
    widgets_historique[-1].grid(column=1, row=r+1)
    widgets_historique.append(Label(tab4, text=convertions.nb_vues(historique[r]['vues']), font=("TkDefaultFont", 7)))
    widgets_historique[-1].grid(column=2, row=r+1)
    widgets_historique.append(Label(tab4, text=historique[r]['chaine'], font=("TkDefaultFont", 7)))
    widgets_historique[-1].grid(column=3, row=r+1)

    h_oui, m_oui, s_oui = convertions.duree(int(historique[r]['duree']))
        # Si durée est inferieur à 1 minutes
    if int(historique[r]['duree']) < 60:
        oui = str(s_oui) + "s"
        # Sinon si la durée est inferieur à  1 heure
    elif int(historique[r]['duree']) < 3600:
       oui = str(m_oui) + "m" + str(s_oui) + "s"
        # Si la durée est supérieure à 1 heure
    else:
        oui = str(h_oui) + "h" + str(m_oui) + "m" + str(s_oui) + "s"
    
    widgets_historique.append(Label(tab4, text=oui, font=("TkDefaultFont", 7)))
    widgets_historique[-1].grid(column=4, row=r+1)


# Affichage de la fenêtre
if __name__ == "__main__":
    root.mainloop()
# https://www.youtube.com/watch?v=bBkH4mQK050
# https://www.youtube.com/watch?v=hgrUj1qMNHk
    
    