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

    return video_name_nouv_nouv

if __name__ == "__main__":
    print(poids_video(369864896))
    print(formatage_video_name("VOITURES : Bientôt INTERDITES en FRANCE ! 🚗🚫"))