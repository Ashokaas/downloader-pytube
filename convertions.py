from time import strftime, gmtime


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
    if poids*10**-6 < 1000:
        return (str(round(poids*10**-6, 2)) + "mo")
    else:
        return (str(round(poids*10**-9, 2)) + "go")


def formatage_video_name_without_extension(video_name):
    
    video_name_nouv = ""
    for i in range(len(video_name)):
        if 97 <= ord(video_name[i]) <= 122 or ord(video_name[i]) == 32:
            video_name_nouv += video_name[i]
    video_name_nouv = video_name_nouv.split()
    video_name_nouv_nouv = ""
    for e in range(len(video_name_nouv)):
        if e+1 == len(video_name_nouv):
            video_name_nouv_nouv += video_name_nouv[e]
        else:
            video_name_nouv_nouv += video_name_nouv[e] + "_"
    return video_name_nouv_nouv


# -- Rend le nom de la video plus lisible
def formatage_video_name(video_name:str):
    for a in range(len(video_name)):
        if video_name[a] == ".":
            extension = video_name[a:-1] + video_name[-1]
            break
    print(extension)
    video_name = video_name.lower()
    video_name_nouv_nouv = formatage_video_name_without_extension(video_name)

    return video_name_nouv_nouv[0: -len(extension)] + extension


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
    len_mots = 0
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
    #print(nb_vues(4973330999))
    #print(titre_ligne("Rick Astley - Never Gonna Give You Up (Official Music Video)"))
    #titre = "Pourquoi les consoles portables manquent au jeu vidéo | Débat & Opinion"
    #print(titre_ligne(titre))
    print(duree(3660))
