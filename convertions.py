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
    if poids*10**-6 < 1000:
        return (str(round(poids*10**-6, 2)) + "mo")
    else:
        return (str(round(poids*10**-9, 2)) + "go")

if __name__ == "__main__":
    print(poids_video(369864896))