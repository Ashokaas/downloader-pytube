# ! (code internet) Signifie que le morceau de code est du copier-coller d'internet et qu'il m'est donc difficile d'expliquer comment il fonctionne
# J'écrit "vidéo" sans accent dans les commentaires mais L'ORTHOGRAPHE IL A CHANGE

# -- Importation des modules --
from turtle import st
from pytube import YouTube
import progressbar as progress
from colorama import init, Fore
import ffmpeg
import os
# -- Importation des fonctions supplémentaires
from convertions import *


# -- Combine l'audio et la video des fichiers >1080p
def combiner_audio(video_name, audio_name, out_name):
    # Importation du module nécessaire
    import moviepy.editor as mpe
    # Importe la video et l'audio
    my_clip = mpe.VideoFileClip(video_name)
    audio_background = mpe.AudioFileClip(audio_name)
    # Ajoute l'audio à la vidéo
    final_clip = my_clip.set_audio(audio_background)
    # Enregistre la vidéo et l'audio dans le même fichier
    final_clip.write_videofile(out_name)


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


def valider_telechargement():
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
    print(liste_video)
    # Affichage des informations pour l'utilisateur sur chaque video et d'un ID pour pouvoir en sélectionner une
    for i in range(len(liste_video)):
        print("Voulez vous télécharger : " +
                    "\n" + "  ID : " + str(i) + 
                    "\n" + "    Type :       " + str(liste_video[i]["type"]) + 
                    "\n" + "    Résolution : " + str(liste_video[i]["resolution"]) + 
                    "\n" + "    FPS :        " + str(liste_video[i]["fps"]) + 
                    "\n" + "    Taille :     " + str(liste_video[i]["taille"]))
    x = int(input("ID de la vidéo à télécharger : "))
    return (x, liste_video)
    


    
def telecharger_video(url):

    print(url)

    # -- Barre de Progression -- (principalement code internet)
    def progress(streams, chunk: bytes, bytes_remaining: int):
        contentsize = video.filesize
        size = contentsize - bytes_remaining

        print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), poids_video(size), "/", poids_video(contentsize), end='')


    print("Récupération des informations de la vidéo...")

    global yt
    yt = YouTube(url, on_progress_callback=progress)

    # -- Print tous les flux video
    for stream in yt.streams:
        print(stream)

        
    # -- Informations --
    print("Titre : " + yt.title)
    print("Chaîne : " + yt.author)
    print("Vues : " + str(yt.views))
    print("Durée : " + duree(yt.length))


    # -- Qualité --
    print(Fore.RED + "Téléchargement :")
    print(Fore.GREEN + "(b)est", 
          Fore.YELLOW + "(s)elect", 
          Fore.BLUE + "(a)udio", 
          Fore.WHITE + "(e)xit")
    print("'(b)est' est déconseillé s'il s'agit d'une vidéo 2k ou plus car il faut télécharger l'audio, la vidéo, puis combiner les 2.\nVous pouvez quand même le faire, sachez juste que c'est beacoup plus long et que le problème ne vient pas du développeur.")
    choix = input("Choix : ")



    # Effectue l'action de la variable "choix"
    match choix:
        case 'b':
            video = valider_telechargement()
        case 's':
            video = select()
        case 'a':
            audio_for_video = audio()
        case 'e':
            quit()



    # -- Combine l'audio et la vidéo des fichiers .webm (+1080p), on est obligé de faire ça car Pytube est PAS TRES TRES GENTIL
    # C'est Très TRES long
    print("Téléchargement en cours...")
    if video.subtype == "webm":
        video_place = r'video/video/' + formatage_video_name(video.title) + '.webm'
        audio_place = r'video/audio/' + formatage_video_name(video.title) + '.webm'
        output_place = r'video/output/' + formatage_video_name(video.title) + '.mp4'
        print(audio_place + '\n' + video_place + '\n' + output_place)
        '''
        video.download(video_place)
        audio_for_video = audio()
        audio_for_video.download(audio_place)'''
        

        #combiner_audio(video_place, audio_place, output_place)
        

    #video.download()


    print("\nDownload Completed")


if __name__ == "__main__":
    url = input("Lien de la video : ")
    telecharger_video(url)
    #https://www.youtube.com/watch?v=H-edzEP5xto