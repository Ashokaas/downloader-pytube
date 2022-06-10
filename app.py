from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from main import *
# -- Importation des modules --
from pytube import YouTube
import progressbar as progress
from colorama import init, Fore
from time import strftime, gmtime
# -- Importation des fonctions supplémentaires
from convertions import *
from main import *

class SayHello(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        #add widgets to window

        #image widget
        self.window.add_widget(Image(source="logo.jpg"))

        #label widget
        self.greeting = Label(text="Lien de la vidéo :", font_size = 18, color='#00FFCE')
        self.window.add_widget(self.greeting)

        #text input
        self.user = TextInput(multiline=False, padding_y = (0, 0), size_hint = (1, 0.2))
        self.window.add_widget(self.user)

        #button widget
        self.button = Button(text="Télécharger", size_hint = (0.3 , 0.3), bold = True, background_color = '#00FFCE')
        self.button.bind(on_press=self.transfert_lien)
        self.window.add_widget(self.button)
    

        return self.window


    def transfert_lien(self, instance):
        print(self.user.text)
        telecharger_video(self.user.text)

    
    



if __name__ == "__main__":
    SayHello().run()