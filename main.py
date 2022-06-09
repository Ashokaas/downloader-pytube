# -- Importation des modules --
from pytube import YouTube
import progressbar as progress
from colorama import init, Fore
# -- Importation des fonctions supplémentaires
from convertions import *



def meilleur_ou_pire_qualite(reverse=False):
    qualites = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p", "8640p"]
    if reverse == True:
        qualites.reverse()
    video = []
    for i in range(len(qualites)):
        video = yt.streams.filter(res=qualites[i])
        if len(video) != 0:
            break
    return video

    
def telecharger_video():

    # -- Barre de Progression -- (non officielle)
    def progress(streams, chunk: bytes, bytes_remaining: int):
        contentsize = video.filesize
        size = contentsize - bytes_remaining

        print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), size, " / ", contentsize, end='')


    url = "https://www.youtube.com/watch?v=p1xBsY6ovxo" #input("Lien de la vidéo : ")
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
    choix = input("Choix : ")



    # Effectue l'action de la variable "choix"
    match choix:
        case 'b':
            video = meilleur_ou_pire_qualite(True)
        case 's':
            video = meilleur_ou_pire_qualite()
        case 'a':
            print("noui")
        case 'e':
            quit()


    print(video)


    
    #video.download()

    print("\nDownload Completed")


telecharger_video()