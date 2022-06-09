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
    return "Pierre qui roule n'amasse pas mousse" # A finir/commencer