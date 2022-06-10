from time import strftime, gmtime


# -- Convertir les secondes en temps lisible
def duree(tps):
    if tps < 60:
        return strftime('%Ss', gmtime(tps))
    elif tps < 3600:
        return strftime('%Mm %Ss', gmtime(tps))
    else:
        return strftime('%Hh %Mm %Ss', gmtime(tps))


def poids_video(poids):
    poids = poids*10**-6
    if poids < 1000:
        return poids
    else:
        return poids*10**-9

if __name__ == "__main__":
    print(poids_video(4875096412))