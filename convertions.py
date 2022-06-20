from time import strftime, gmtime


# -- Convertir les secondes en temps lisible
def duree(tps:int):
    if tps < 60:
        return strftime('%Ss', gmtime(tps))
    elif tps < 3600:
        return strftime('%Mm %Ss', gmtime(tps))
    else:
        return strftime('%Hh %Mm %Ss', gmtime(tps))


# -- Convertir les octets en mo/go
def poids_video(poids:int):
    if poids*10**-6 < 1000:
        return (str(round(poids*10**-6, 2)) + "mo")
    else:
        return (str(round(poids*10**-9, 2)) + "go")


# -- Rend le nom de la video plus lisible
def formatage_video_name(video_name:str):
    for a in range(len(video_name)):
        if video_name[a] == ".":
            extension = video_name[a:-1] + video_name[-1]
            break
    print(extension)
    video_name = video_name.lower()
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
    titre_temp = ""
    x = 0
    for i in range(len(titre)):
        if len(titre_return) > 30 and x > 5:
            titre_return += '\n'
            x = 0
        x += 1
        titre_return += titre[i] + " "
        
    return titre_return
        

if __name__ == "__main__":
    print(poids_video(369864896))
    print(formatage_video_name("VOITURES : Bientôt INTERDITES en FRANCE ! 🚗🚫.webm"))
    print(nb_vues(4973330999))
    print(titre_ligne("Rick Astley - Never Gonna Give You Up (Official Music Video)"))
