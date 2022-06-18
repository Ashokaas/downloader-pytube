from tkinter import * 

window = Tk()


background_color = '#191919'
text_color = '#FFF'

# -- Parametres de la fenetre
window.title("Numérisateur Original Universel Biochimique")
window.geometry("720x480")
window.resizable(width=False, height=False)
window.config(background=background_color)
window.iconbitmap('youtube.ico')


frame_link = Frame(window, bg=background_color, bd=1, relief=SUNKEN)

from main import *
def oui():
    telecharger_video(input_link.get())
    

# -- Frame Lien video
label_link = Label(frame_link, text="Lien de la vidéo :", font=("Roboto", 15), bg=background_color, fg=text_color)
label_link.pack()

button_link = Button(frame_link, text="Convertir", font=("Roboto", 15), bg='white', fg=background_color, command=oui)
button_link.pack(pady=25, fill=X)

input_link = Entry(frame_link)
input_link.pack()

frame_link.pack()



frame_bottom = Frame(window, bg='#E0E0E0', height=250)
frame_bottom.grid(column=0, columnspan=2, row=1, padx=5, pady=5)
frame_bottom.pack_propagate(False)
# ==== Setup de l'output log ====
# Ajouter du texte facilement car il faut autoriser la modification dans le widget avant de pouvoir insérer du texte



# -- Frame pour chaque source video
#for i in range(len(liste video))



# -- Affichage de la fenêtre
window.mainloop()