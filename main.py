# J'écrit "vidéo" sans accent dans les commentaires mais L'ORTHOGRAPHE IL A CHANGE

# -- Importation des modules --
from email.policy import default
import re
from pytube import YouTube
import pytube.exceptions
import progressbar as progress
from colorama import init, Fore
import ffmpeg
import os
import subprocess as sp
import sys
from moviepy.config import get_setting
from moviepy.tools import subprocess_call
# -- Importation des fonctions supplémentaires
from convertions import *


# -- Clear python console --
clear = lambda: os.system('cls')


# -- Fusionne l'audio et la video --
def fusionner_video_audio(video, audio, output, vcodec='copy', acodec='copy', ffmpeg_output=False, logger = 'bar'):
    cmd = [get_setting("FFMPEG_BINARY"), "-y", "-i", audio, "-i", video, "-vcodec", vcodec, "-acodec", acodec, output]
    subprocess_call(cmd, logger = logger)


def supprimer_fichier_dossier(dossier):
    for fichier in os.listdir(dossier):
        os.remove(dossier + "/" + fichier)


def select():
    video = yt.streams.filter(mime_type="video/mp4")
    x, liste_video = choix_video(video)
    # Récupération de la video sélectionnée
    video = yt.streams.get_by_itag(liste_video[x]["itag"])
    return video
    

def audio():
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


def best():
    # Définie la qualité maximale video en pixel(hauteur)
    qualite_max = 0
    # Pour chaque flux "stream":
    for stream in yt.streams:
        # S'il est une vidéo
        if stream.resolution != None:
            # Supprimer le "p" pour le garder que le nombre en (int) -- exemple : "1080p" -> 1080
            qualite_video = int(stream.resolution[0:-1])
            # Si elle est supérieur à la qulité précédemment enregistré la remplace
            if qualite_video > qualite_max:
                qualite_max = qualite_video
    # Récupération du/des flux video possédant la meilleure qualité
    qualite_max = str(qualite_max) + "p"
    video = yt.streams.filter(res=qualite_max)
    x, liste_video = choix_video(video)
    # Récupération de la video sélectionnée
    video = yt.streams.get_by_itag(liste_video[x]["itag"])
    return video


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
    print("Liste des flux video :")
    for i in range(len(liste_video)):
        print(             " ID : " + str(i) + 
                    "\n" + "    Type :       " + str(liste_video[i]["type"]) + 
                    "\n" + "    Résolution : " + str(liste_video[i]["resolution"]) + 
                    "\n" + "    FPS :        " + str(liste_video[i]["fps"]) + 
                    "\n" + "    Taille :     " + str(liste_video[i]["taille"]))
    print(" ")
    x = input("ID de la vidéo à télécharger ((e)xit) : ")
    if x.lower() == "e":
        quit()
    else:
        return (int(x), liste_video)


def telechargement(video):
    if video.is_progressive == False:
        audio_for_video = audio()

        file_name = formatage_video_name(audio_for_video.default_filename)
        video_path = 'video/temp/video_temp'
        audio_path = 'video/temp/audio_temp'

        
        print("Téléchargement de l'audio en cours...")
        audio_for_video.download(output_path=audio_path, filename=file_name)
        
        print("Téléchargement de la video en cours...")
        video.download(output_path=video_path, filename=file_name)


        print("Fusion de la video et le l'audio en cours...")
        fusionner_video_audio((video_path + '/' + file_name), (audio_path + '/' + file_name), ('video/video/' + file_name))

        supprimer_fichier_dossier('video/temp/video_temp')
        supprimer_fichier_dossier('video/temp/audio_temp')
    else:
        file_name = formatage_video_name(video.default_filename)
        video_path = 'video/temp/video_temp'
        print("Téléchargement de la video en cours...")
        video.download(output_path=video_path, filename=file_name)
    


    
def telecharger_video(url):

    # -- Barre de Progression --
    def progress(streams, chunk: bytes, bytes_remaining: int):
        contentsize = video.filesize
        size = contentsize - bytes_remaining

        print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), poids_video(size), "/", poids_video(contentsize), end='')


    print("Récupération des informations de la vidéo...")

    global yt
    yt = YouTube(url, on_progress_callback=progress)

    # -- Print tous les flux video
    '''for stream in yt.streams:
        print(stream)
    print(yt.streams.filter(progressive=True))'''

        
    # -- Informations --
    print("")
    print("Titre : " + yt.title)
    print("Chaîne : " + yt.author)
    print("Vues : " + str(yt.views))
    print("Durée : " + duree(yt.length))


    # -- Qualité --
    print("")
    print(Fore.RED + "Téléchargement :")
    print(Fore.GREEN + "(b)est", 
          Fore.YELLOW + "(s)elect", 
          Fore.BLUE + "(a)udio", 
          Fore.WHITE + "(e)xit")
    choix = input("Choix : ")
    choix = choix.lower()

    while choix not in "bsae":
        print("Erreur : Option invalide")
        choix = input("Choix : ")
        choix = choix.lower()  

    # Effectue l'action de la variable "choix"
    match choix:
        case 'b':
            video = best()
            telechargement(video)
        case 's':
            video = select()
            telechargement(video)
        case 'a':
            video = audio()
            video.download(r'video/audio/')
        case 'e':
            quit()
    

    #video.download()


    print("Download Completed")


if __name__ == "__main__":
    clear()
    print("Si la lecture de la video de fonctionne pas utilisez VLC Media Player\nhttps://www.videolan.org/vlc/download-windows.html")
    try:
        url = input("Lien de la video : ")
        telecharger_video(url)
        #https://www.youtube.com/watch?v=H-edzEP5xto
        supprimer_fichier_dossier('video/temp/video_temp')
    except pytube.exceptions.RegexMatchError:
        clear()
        print("Erreur : Lien invalide !")
        