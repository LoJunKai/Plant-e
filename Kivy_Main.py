import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import database

user, db = database.setup("plant-e")

class MainWindow(Screen):
    def water(self):
        print("water!!")
        
    def data(self):

        # TODO
        plant = "100"
        day = 9
        hourcount = 23

        moisture = db.child("Plant-e").child(plant).child("day " + str(day)).child(hourcount).child("moisture").get(user['idToken']).val()
        light = db.child("Plant-e").child(plant).child("day " + str(day)).child(hourcount).child("light").get(user['idToken']).val()

        return moisture, light

class StatWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ProgBar(BoxLayout):
    pass

class PlantE(App):
    #no need for init cos App has an init itself

    def build(self):
        return Builder.load_file("Kivy_Home.kv")

if __name__ == '__main__':
    PlantE().run()                    #.run is from App from kivy.app