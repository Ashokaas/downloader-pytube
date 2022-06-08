from pytube import YouTube
from time import *
import progressbar as progress
from colorama import init, Fore


def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = video.filesize
    size = contentsize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), end='')


def duree(tps):
    if tps < 60:
        return strftime('%Ss', gmtime(tps))
    elif tps < 3600:
        return strftime('%Mm %Ss', gmtime(tps))
    else:
        return strftime('%Hh %Mm %Ss', gmtime(tps))


url = input("Lien de la vidéo : ")
yt = YouTube(url, on_progress_callback=progress)

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

match choix:
    case 'b':
        print("oui")
    case 'w':
        print("non")
    case 'a':
        print("noui")
    case 'e':
        quit()

for stream in yt.streams:
    print(stream)

#print(yt.streams.filter())

video = yt.streams.get_highest_resolution()
print(video)

print(str(round(video.filesize/1000000)) + " MO")


#video.download()

print("Download Completed")