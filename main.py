# -- Importation des modules --
from turtle import st
from pytube import YouTube
import progressbar as progress
from colorama import init, Fore
import ffmpeg
import os
# -- Importation des fonctions supplémentaires
from convertions import *


def combine_audio(video_name, audio_name, out_name):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(video_name)
    audio_background = mpe.AudioFileClip(audio_name)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(out_name)


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


def valider_telechargement():
    qualite_max = 0
    for stream in yt.streams:
        if stream.resolution != None:
            qualite_video = int(stream.resolution[0:-1])
            if qualite_video > qualite_max:
                qualite_max = qualite_video
    qualite_max = str(qualite_max) + "p"
    video = yt.streams.filter(res=qualite_max)
    liste_video = []
    for stream in video:
        if stream.mime_type != "audio/mp4" and stream.mime_type != "audio/webm":
            liste_video.append({"type": stream.mime_type, "resolution": stream.resolution, "fps": (str(stream.fps) + "fps"), "taille": poids_video(stream.filesize), "itag": stream.itag})
    print(liste_video)
    for i in range(len(liste_video)):
        print("Voulez vous télécharger : " +
                    "\n" + "  ID : " + str(i) + 
                    "\n" + "    Type :       " + str(liste_video[i]["type"]) + 
                    "\n" + "    Résolution : " + str(liste_video[i]["resolution"]) + 
                    "\n" + "    FPS :        " + str(liste_video[i]["fps"]) + 
                    "\n" + "    Taille :     " + str(liste_video[i]["taille"]))
    x = int(input("ID de la vidéo à télécharger : "))
    
    video = yt.streams.get_by_itag(liste_video[x]["itag"])

    return video
    


    
def telecharger_video(url):

    print(url)

    # -- Barre de Progression -- (non officielle)
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
    choix = input("Choix : ")



    # Effectue l'action de la variable "choix"
    match choix:
        case 'b':
            video = valider_telechargement()
        case 's':
            print("oui")
        case 'a':
            audio_for_video = audio()
            #video.download(r'C:\Users\antot\Downloads')
        case 'e':
            quit()


    name = video.title.lower()
    print(name)
    for caractere in name:
        print("oui")


    print("Téléchargement en cours...")
    if video.subtype == "webm":
        '''video.download(r'video\video')
        audio_for_video = audio()
        audio_for_video.download(r'video\audio')
        name = video.title'''
        
        video_place = r'video/video/' + video.title + '.webm'
        audio_place = r'video/audio/' + video.title + '.webm'
        output_place = r'video/output/' + video.title + '.mp4'
        print(audio_place, video_place, output_place)

        combine_audio(video_place, audio_place, output_place)
        

    #video.download()


    print("\nDownload Completed")


if __name__ == "__main__":
    url = input("Lien de la video : ")
    telecharger_video(url)
    #https://www.youtube.com/watch?v=H-edzEP5xto
    print(ord('A'))