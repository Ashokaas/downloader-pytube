import re


# -- Convertir les secondes en temps lisible
def duree(tps:int):
    h = tps//3600
    tps -= 3600*h
    min = tps//60
    tps -= 60*min
    sec = tps
    return h, min, sec


# -- Convertir les octets en mo/go
def poids_video(poids:int):
    # Si en convertissant le poids en mo il est inférieur à 1000mo alors on l'envoie en mo
    # Sinon on l'envoie en go
    if poids*10**-6 < 1000:
        return (str(round(poids*10**-6, 2)) + "mo")
    else:
        return (str(round(poids*10**-9, 2)) + "go")




# -- Rend le nom de la video plus lisible
def formatage_video_name(video_name:str, video_extension:bool):
    # Si l'extension est incluse dans le nom de la vidéo
    if video_extension == True:
        # On inverse le nom de la vidéo afin de récupérer le premier "." du nom
        video_name_extension = video_name[::-1]
        # Pour chaque caractère du nom de la vidéo
        for a in range(len(video_name_extension)):
            # Si le caractère est "."
            if video_name_extension[a] == ".":
                # Alors l'extension est égale à tous les caractères jusqu'au "."
                extension = video_name_extension[0:a] + video_name_extension[a]
                # Comme on a inversé le titre on doit le réinverser pour avoir la vrai extension ("4pm. -> .mp4")
                extension = extension[::-1]
                # On supprime l'extension du nom de la vidéo
                video_name = video_name[0:len(video_name)-len(extension)]
                break
        
    # On garde uniquement les caractères allant de : 'A' -> 'Z', de 'a' -> 'z' et l'espace ' '
    # On remplace les espaces par des '_'
    # On met tout en minuscule
    video_name = re.sub(r"[^a-zA-Z0-9- ]","",video_name).replace(" ", "_").lower()

    # Si l'extension est incluse on la rajoute car on l'a supprimé avant
    if video_extension == True:
        return video_name, extension
    else:
        return video_name




def nb_vues(vues):
    vues = str(vues)[::-1]
    vues_return = ""
    x = 0
    for i in range(len(vues)):
        if i % 3 == 0 and i != 0:
            vues_return += " "
        vues_return += vues[i]

    vues_return = vues_return[::-1]
    return vues_return


def titre_ligne(titre):
    titre = titre.split()
    titre_return = ""
    x = 0
    for i in range(len(titre)):
        if len(titre_return) > 25 and x > 3:
            titre_return += '\n'
            x = 0
            len_mots = 0
        x += 1
        len_mots = 0
        titre_return += titre[i] + " "
        
    return titre_return



        

if __name__ == "__main__":
    #print(poids_video(369864896))
    #print(formatage_video_name("https://www.youtube.com/watch?v=bBkH4mQK050"))
    #print(nb_vues(4973330999)[-1])
    #print(titre_ligne("Rick Astley - Never Gonna Give You Up (Official Music Video)"))
    #titre = "Pourquoi les consoles portables manquent au jeu vidéo | Débat & Opinion"
    #print(titre_ligne(titre))
    #print(duree(3660))
    #print(formatage_video_name_without_extension("La SCIENCE des EMBOUTEILLAGES"))
    print(formatage_video_name("Hey! What's up bro?.mp4", True))

