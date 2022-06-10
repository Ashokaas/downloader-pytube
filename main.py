# -- Importation des modules --
from pytube import YouTube
import progressbar as progress
from colorama import init, Fore
# -- Importation des fonctions supplémentaires
from convertions import *



def meilleur_qualite():
    qualite_max = 0
    for stream in yt.streams:
        if stream.resolution != None:
            qualite_video = int(stream.resolution[0:-1])
            if qualite_video > qualite_max:
                qualite_max = qualite_video
    qualite_max = str(qualite_max) + "p"
    video = yt.streams.filter(res=qualite_max)
    return video


def audio():
    qualite_max = 0
    for stream in yt.streams.filter(mime_type="audio/webm"):
        if stream.abr != None:
            qualite_audio = int(stream.abr[0:-4])
            if qualite_audio > qualite_max:
                qualite_max = qualite_audio
    qualite_max = str(qualite_max) + "kbps"
    video = yt.streams.filter(mime_type="audio/webm", abr=qualite_max)
    return video[0]


def valider_telechargement(video):
    liste_video = []
    for stream in video:
        if stream.mime_type != "audio/mp4" and stream.mime_type != "audio/webm":
            liste_video.append({"type": stream.mime_type, "resolution": stream.resolution, "fps": stream.fps, "itag": stream.itag})

    
def telecharger_video(url):

    print(url)

    # -- Barre de Progression -- (non officielle)
    def progress(streams, chunk: bytes, bytes_remaining: int):
        contentsize = video.filesize
        size = contentsize - bytes_remaining

        print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), size, " / ", contentsize, end='')


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
            video = meilleur_qualite()
            valider_telechargement(video)
        case 's':
            video = yt.streams
        case 'a':
            video = audio()
            #video.download(r'C:\Users\antot\Downloads')
        case 'e':
            quit()




    #video.download()

    print("\nDownload Completed")


if __name__ == "__main__":
    telecharger_video("https://www.youtube.com/watch?v=C-FWMpbBHpU")