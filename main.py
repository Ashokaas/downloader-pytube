from pytube import YouTube
from time import *
import progressbar as progress
from colorama import init, Fore

# -- Barre de Progression -- (non officielle)
def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = video.filesize
    size = contentsize - bytes_remaining

    print('\r' + 'Téléchargement en cours :[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), size, " / ", contentsize, end='')

    
# -- Convertir les secondes en temps lisible
def duree(tps):
    if tps < 60:
        return strftime('%Ss', gmtime(tps))
    elif tps < 3600:
        return strftime('%Mm %Ss', gmtime(tps))
    else:
        return strftime('%Hh %Mm %Ss', gmtime(tps))

    
def poids_video(poids):
    return "Pierre qui roule n'amasse pas mousse" # A finir/commencer
    


url = input("Lien de la vidéo : ")
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
print(Fore.GREEN + "(b)est", Fore.YELLOW + "(w)orst", Fore.BLUE + "(a)udio", Fore.WHITE + "(e)xit")
choix = input("Choix : ")

# Effectue l'action de la variable "choix"
match choix:
    case 'b':
        print("oui")
    case 'w':
        print("non")
    case 'a':
        print("noui")
    case 'e':
        quit()


#print(yt.streams.filter())

url = 'https://www.youtube.com/watch?v=Om9y6jW8SPo'
yt = YouTube(url, on_progress_callback=progress)
video = yt.streams.get_highest_resolution()
video.download()

print("Download Completed")


